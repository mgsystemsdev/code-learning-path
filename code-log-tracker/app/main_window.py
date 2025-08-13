# app/main_window.py
"""
MainWindow for Smart Learning Tracker.

Responsibilities:
- Build table + input form UI
- Connect to DB layer (app.db)
- Provide add/save/delete/export actions
- Inline editing with delegates and points recompute
- Smart suggestions via language packs and recent items
"""

from __future__ import annotations

import csv
from typing import Dict, Any, List, Tuple

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QComboBox,
    QDoubleSpinBox,
    QLineEdit,
    QMessageBox,
    QFileDialog,
    QDateEdit,
    QAbstractItemView,
    QHeaderView,
    QGroupBox,
)
from PySide6.QtCore import Qt, QDate

from app.dialogs import (
    SuggestionDialog,
    TargetTimeDialog,
    DateDelegate,
    HoursDelegate,
    ComboDelegate,
)
from app.db import (
    init_db,
    get_languages,
    find_or_create_item,
    insert_or_update_session,
    list_sessions,
    get_config,
    search_items,
    get_item_by_id,
    load_language_pack,
)

# ---------- Column Definitions ----------
HEADERS: List[str] = [
    "ID",
    "Date",
    "Language",
    "Type",
    "Work Item Name",
    "Target Time",
    "Status",
    "Hours",
    "Notes",
    "Tags",
    "Difficulty",
    "Topic",
    "Points",
    "Progress %",
]

# KEYS are the row payload names we use to talk to the DB/service layer
KEYS: List[str] = [
    "id",  # 0
    "date",
    "language_code",
    "type",
    "canonical_name",
    "target_hours",
    "status",
    "hours_spent",
    "notes",
    "tags",
    "difficulty",
    "topic",
    "points_awarded",
    "progress_pct",  # 13
]

# Editable columns in the table
EDITABLE_COLS = {
    "Date",
    "Status",
    "Hours",
    "Notes",
    "Tags",
    "Difficulty",
    "Topic",
}

# ---------- Main Window ----------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Learning Tracker")
        self.resize(1400, 800)

        self.reloading = False
        self.updating_template = False
        self.current_language_pack: Dict[str, Any] = {}
        self.editing_session_id = None  # used during form-based save

        # Initialize DB
        init_db()
        self.config = get_config() or {}

        self._build_ui()
        self.reload_table()

    # ===== UI Construction =====
    def _build_ui(self):
        # Table
        self.table = QTableWidget(0, len(HEADERS))
        self.table.setHorizontalHeaderLabels(HEADERS)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setWordWrap(False)
        self.table.setEditTriggers(
            QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked
        )
        self.table.setStyleSheet(
            """
            QTableWidget::item:selected { background: #dbeafe; color: black; }
            QTableWidget { gridline-color: #e5e7eb; selection-background-color: #dbeafe; }
            """
        )

        hdr = self.table.horizontalHeader()
        hdr.setSectionResizeMode(QHeaderView.Interactive)
        hdr.setStretchLastSection(True)
        column_widths = [60, 110, 120, 90, 260, 100, 120, 80, 220, 150, 120, 160, 90, 110]
        for i, w in enumerate(column_widths):
            hdr.resizeSection(i, w)

        # Delegates
        self._install_delegates()

        # Signals
        self.table.itemChanged.connect(self.on_cell_changed)

        # Toolbar
        self._build_toolbar()

        # Input form
        self._build_input_form()

        # Layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.toolbar_layout)
        main_layout.addWidget(self.table, 1)
        main_layout.addWidget(self.input_group)

        cw = QWidget()
        cw.setLayout(main_layout)
        self.setCentralWidget(cw)

    def _build_toolbar(self):
        self.toolbar_layout = QHBoxLayout()

        self.add_btn = QPushButton("Add Entry")
        self.save_btn = QPushButton("Save Entry")
        self.del_btn = QPushButton("Delete Entry")
        self.export_btn = QPushButton("Export CSV")

        style = """
            QPushButton { padding: 8px 16px; font-weight: bold; border-radius: 4px; }
            QPushButton:hover { background-color: #f0f9ff; }
        """
        for b in (self.add_btn, self.save_btn, self.del_btn, self.export_btn):
            b.setStyleSheet(style)

        self.add_btn.clicked.connect(self.add_entry)
        self.save_btn.clicked.connect(self.save_entry)
        self.del_btn.clicked.connect(self.delete_entry)
        self.export_btn.clicked.connect(self.export_csv)

        self.toolbar_layout.addWidget(self.add_btn)
        self.toolbar_layout.addWidget(self.save_btn)
        self.toolbar_layout.addWidget(self.del_btn)
        self.toolbar_layout.addStretch()
        self.toolbar_layout.addWidget(self.export_btn)

    def _build_input_form(self):
        self.input_group = QGroupBox("Add New Learning Entry")
        form = QVBoxLayout()

        row1 = QHBoxLayout()
        row2 = QHBoxLayout()

        self.inputs: Dict[str, Any] = {}

        # Date
        date_box = QVBoxLayout()
        date_box.addWidget(QLabel("Date *"))
        self.inputs["date"] = QDateEdit()
        self.inputs["date"].setCalendarPopup(True)
        self.inputs["date"].setDate(QDate.currentDate())
        self.inputs["date"].setMinimumWidth(120)
        date_box.addWidget(self.inputs["date"])
        row1.addLayout(date_box)

        # Language
        lang_box = QVBoxLayout()
        lang_box.addWidget(QLabel("Language *"))
        self.inputs["language"] = QComboBox()
        self.inputs["language"].setMinimumWidth(160)
        self._load_languages()
        self.inputs["language"].currentTextChanged.connect(self.on_language_changed)
        lang_box.addWidget(self.inputs["language"])
        row1.addLayout(lang_box)

        # Type
        type_box = QVBoxLayout()
        type_box.addWidget(QLabel("Type *"))
        self.inputs["type"] = QComboBox()
        self.inputs["type"].addItems(["", "Exercise", "Project"])
        self.inputs["type"].setMinimumWidth(110)
        type_box.addWidget(self.inputs["type"])
        row1.addLayout(type_box)

        # Work Item
        item_box = QVBoxLayout()
        item_box.addWidget(QLabel("Work Item Name *"))
        self.inputs["work_item"] = QComboBox()
        self.inputs["work_item"].setEditable(True)
        self.inputs["work_item"].setMinimumWidth(280)
        self.inputs["work_item"].lineEdit().textChanged.connect(self.on_work_item_changed)
        item_box.addWidget(self.inputs["work_item"])
        row1.addLayout(item_box)

        # Hours
        hours_box = QVBoxLayout()
        hours_box.addWidget(QLabel("Hours *"))
        self.inputs["hours"] = QDoubleSpinBox()
        self.inputs["hours"].setRange(0, 24)
        self.inputs["hours"].setSingleStep(0.25)
        self.inputs["hours"].setDecimals(2)
        self.inputs["hours"].setMinimumWidth(90)
        hours_box.addWidget(self.inputs["hours"])
        row1.addLayout(hours_box)

        # Status
        status_box = QVBoxLayout()
        status_box.addWidget(QLabel("Status"))
        self.inputs["status"] = QComboBox()
        self.inputs["status"].addItems(["", "Planned", "In Progress", "Completed", "Blocked"])
        self.inputs["status"].setCurrentText("In Progress")
        self.inputs["status"].setMinimumWidth(140)
        status_box.addWidget(self.inputs["status"])
        row2.addLayout(status_box)

        # Difficulty
        diff_box = QVBoxLayout()
        diff_box.addWidget(QLabel("Difficulty"))
        self.inputs["difficulty"] = QComboBox()
        self.inputs["difficulty"].addItems(["", "Beginner", "Intermediate", "Advanced", "Expert"])
        self.inputs["difficulty"].setMinimumWidth(140)
        diff_box.addWidget(self.inputs["difficulty"])
        row2.addLayout(diff_box)

        # Topic
        topic_box = QVBoxLayout()
        topic_box.addWidget(QLabel("Topic"))
        self.inputs["topic"] = QComboBox()
        self.inputs["topic"].setEditable(True)
        self.inputs["topic"].setMinimumWidth(180)
        topic_box.addWidget(self.inputs["topic"])
        row2.addLayout(topic_box)

        # Notes
        notes_box = QVBoxLayout()
        notes_box.addWidget(QLabel("Notes"))
        self.inputs["notes"] = QLineEdit()
        self.inputs["notes"].setPlaceholderText("What did you do?")
        self.inputs["notes"].setMinimumWidth(260)
        self.inputs["notes"].textChanged.connect(self.auto_fill_from_text)
        notes_box.addWidget(self.inputs["notes"])
        row2.addLayout(notes_box)

        # Tags
        tags_box = QVBoxLayout()
        tags_box.addWidget(QLabel("Tags"))
        self.inputs["tags"] = QLineEdit()
        self.inputs["tags"].setPlaceholderText("comma, separated, tags")
        self.inputs["tags"].setMinimumWidth(180)
        tags_box.addWidget(self.inputs["tags"])
        row2.addLayout(tags_box)

        form.addLayout(row1)
        form.addLayout(row2)

        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #666; font-style: italic; padding: 4px;")
        form.addWidget(self.status_label)

        self.input_group.setLayout(form)

    def _install_delegates(self):
        col_map = {h: i for i, h in enumerate(HEADERS)}
        if "Date" in col_map:
            self.table.setItemDelegateForColumn(col_map["Date"], DateDelegate(self.table))
        if "Status" in col_map:
            self.table.setItemDelegateForColumn(
                col_map["Status"],
                ComboDelegate(lambda: ["Planned", "In Progress", "Completed", "Blocked"], parent=self.table),
            )
        if "Difficulty" in col_map:
            self.table.setItemDelegateForColumn(
                col_map["Difficulty"],
                ComboDelegate(lambda: ["Beginner", "Intermediate", "Advanced", "Expert"], parent=self.table),
            )
        if "Hours" in col_map:
            self.table.setItemDelegateForColumn(col_map["Hours"], HoursDelegate(self.table))

    # ===== Data/Config Helpers =====
    def _load_languages(self):
        try:
            languages: List[Tuple[str, str, str]] = get_languages() or []
            self.inputs["language"].clear()
            self.inputs["language"].addItem("")
            for code, name, _color in languages:
                self.inputs["language"].addItem(name, code)
        except Exception as e:
            print(f"Warning: Failed to load languages: {e}")

    def on_language_changed(self):
        if self.updating_template:
            return
        code = self.inputs["language"].currentData()
        if not code:
            return
        try:
            self.current_language_pack = load_language_pack(code) or {}
            self._update_topic_suggestions()
            self._update_work_item_suggestions()
        except Exception as e:
            print(f"Warning: Failed to load language pack: {e}")

    def _update_topic_suggestions(self):
        topics = list(self.current_language_pack.get("topics", {}).keys())
        self.inputs["topic"].clear()
        self.inputs["topic"].addItem("")
        if topics:
            self.inputs["topic"].addItems(topics)

    def _update_work_item_suggestions(self):
        language_code = self.inputs["language"].currentData()
        item_type = self.inputs["type"].currentText().strip()
        if not language_code or not item_type:
            return
        try:
            items = search_items(language_code, item_type, limit=20) or []
            self.inputs["work_item"].clear()
            self.inputs["work_item"].addItem("")
            for it in items:
                txt = f"{it['name']}"
                if (it.get("total_hours") or 0) > 0:
                    txt += f" ({it['total_hours']:.1f}h logged)"
                self.inputs["work_item"].addItem(txt, it.get("id"))
        except Exception as e:
            print(f"Warning: Failed to update work item suggestions: {e}")

    def on_work_item_changed(self):
        if self.updating_template:
            return
        current_id = self.inputs["work_item"].currentData()
        if current_id:
            try:
                item = get_item_by_id(current_id)
                if item:
                    self.inputs["difficulty"].setCurrentText(item.get("default_difficulty") or "")
                    self.inputs["topic"].setCurrentText(item.get("default_topic") or "")
                    self._update_status_display(item)
                    return
            except Exception as e:
                print(f"Warning: Failed to get item details: {e}")
        self.auto_fill_from_text()

    def auto_fill_from_text(self):
        if self.updating_template:
            return
        try:
            text = " ".join(
                [self.inputs["work_item"].currentText(), self.inputs["notes"].text()]
            ).lower()
            if not text.strip():
                return

            best_topic = ""
            best_difficulty = ""
            best_score = 0

            for topic, topic_info in self.current_language_pack.get("topics", {}).items():
                score = 0
                if topic.lower() in text:
                    score += 10
                if score > best_score:
                    best_score = score
                    best_topic = topic
                    best_difficulty = topic_info.get("default_difficulty", "Beginner")

            for skill_name, skill_info in self.current_language_pack.get("skills", {}).items():
                score = 0
                for kw in skill_info.get("keywords", []):
                    if kw.lower() in text:
                        score += 5
                if skill_name.lower() in text:
                    score += 15
                if score > best_score:
                    best_score = score
                    best_difficulty = skill_info.get("difficulty", best_difficulty)

            if best_topic and best_score > 0:
                self.inputs["topic"].setCurrentText(best_topic)
            if best_difficulty and best_score > 0:
                self.inputs["difficulty"].setCurrentText(best_difficulty)
        except Exception as e:
            print(f"Warning: Auto-fill failed: {e}")

    def _update_status_display(self, item=None):
        if not item:
            self.status_label.setText("")
            return
        try:
            parts = []
            total_hours = item.get("total_hours") or 0.0
            target_hours = item.get("target_hours") or 0.0
            if total_hours > 0:
                parts.append(f"Logged: {total_hours:.1f}h")
            if target_hours > 0:
                progress = min(100.0, (total_hours / target_hours) * 100.0)
                parts.append(f"Progress: {progress:.1f}%")
            streak = item.get("current_streak_days") or 0
            if streak > 0:
                parts.append(f"Streak: {streak} days")
            eta = item.get("projected_finish_date")
            if eta:
                parts.append(f"ETA: {eta.split('T')[0] if isinstance(eta, str) else eta}")
            self.status_label.setText(" | ".join(parts))
        except Exception as e:
            print(f"Warning: Failed to update status display: {e}")

    # ===== Form Actions =====
    def clear_form(self):
        self.updating_template = True
        try:
            self.inputs["date"].setDate(QDate.currentDate())
            self.inputs["hours"].setValue(0.0)
            self.inputs["notes"].clear()
            self.inputs["tags"].clear()
            self.inputs["status"].setCurrentText("In Progress")
            for f in ["language", "type", "work_item", "difficulty", "topic"]:
                self.inputs[f].setCurrentIndex(0)
            self.status_label.setText("")
            self.editing_session_id = None
        finally:
            self.updating_template = False

    def add_entry(self):
        self.clear_form()
def save_entry(self):
    """
    Insert a new session row using the form values.
    Handles suggestion dialog for similar items and computes points.
    """
    import traceback

    def fail(stage: str, err: Exception):
        tb = traceback.format_exc()
        # Also print to console for dev visibility
        print(f"[save_entry:{stage}] {err}\n{tb}")
        QMessageBox.critical(self, "Error", f"[{stage}] {err}")

    # 1) Read & validate form inputs
    try:
        language_code = self.inputs["language"].currentData()
        item_type = self.inputs["type"].currentText().strip()
        work_item = self.inputs["work_item"].currentText().strip()
        date_str = self.inputs["date"].date().toString("yyyy-MM-dd")
        hours = float(self.inputs["hours"].value())
        notes = self.inputs["notes"].text().strip()
        tags = self.inputs["tags"].text().strip()
        difficulty = self.inputs["difficulty"].currentText() or "Beginner"
        topic = self.inputs["topic"].currentText().strip()
        status = self.inputs["status"].currentText() or "In Progress"

        if not language_code:
            QMessageBox.warning(self, "Validation", "Please select a language.")
            return
        if not work_item:
            QMessageBox.warning(self, "Validation", "Please enter the exercise or project name.")
            return
        if item_type not in {"Exercise", "Project"}:
            QMessageBox.warning(self, "Validation", "Please choose a Type: Exercise or Project.")
            return
    except Exception as e:
        fail("read_form", e); return

    # 2) Resolve/confirm item_id (similarity dialog path)
    try:
        item_id, _is_new, suggestions = find_or_create_item(language_code, item_type, work_item)
        if suggestions:
            dlg = SuggestionDialog(suggestions, work_item, self)
            if dlg.exec():
                if dlg.create_new:
                    item_id, _, _ = find_or_create_item(language_code, item_type, work_item)
                else:
                    item_id = dlg.selected_item_id or item_id
    except Exception as e:
        fail("find_or_create_item", e); return

    # 3) Compute points from config
    try:
        cfg = get_config() or {}
        diff_w = (cfg.get("difficulty_weights") or {}).get(difficulty, 1.0)
        status_m = (cfg.get("status_multipliers") or {}).get(status, 1.0)
        points = hours * float(diff_w) * float(status_m)
    except Exception as e:
        fail("compute_points", e); return

    # 4) Persist
    try:
        row_data = {
            "item_id": item_id,
            "date": date_str,
            "status": status,
            "hours_spent": hours,
            "notes": notes,
            "tags": tags,
            "difficulty": difficulty,
            "topic": topic,
            "points_awarded": points,
        }
        if getattr(self, "editing_session_id", None):
            row_data["id"] = self.editing_session_id

        insert_or_update_session(row_data)
    except Exception as e:
        fail("insert_or_update_session", e); return

    # 5) Refresh UI
    try:
        self.reload_table()
        self.clear_form()
        QMessageBox.information(self, "Success", "Entry saved successfully!")
    except Exception as e:
        fail("reload_table", e); return

    def delete_entry(self):
        """Delete the selected session row (by ID) and refresh."""
        try:
            r = self.table.currentRow()
            if r < 0:
                QMessageBox.information(self, "Info", "Please select a row to delete.")
                return
            id_item = self.table.item(r, 0)
            if not id_item:
                return
            session_id = id_item.text().strip()
            if not session_id:
                return

            reply = QMessageBox.question(
                self,
                "Confirm Delete",
                f"Are you sure you want to delete session {session_id}?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if reply != QMessageBox.Yes:
                return

            # Delete and update summaries via db helpers
            from app.db import connect, update_item_summaries

            with connect() as con:
                cur = con.cursor()
                cur.execute("SELECT item_id FROM sessions WHERE id=?", (session_id,))
                row = cur.fetchone()
                item_id = row[0] if row else None

                cur.execute("DELETE FROM sessions WHERE id=?", (session_id,))
                con.commit()

                if item_id is not None:
                    update_item_summaries(item_id)

            self.reload_table()
            QMessageBox.information(self, "Success", "Entry deleted successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete entry: {e}")

    def export_csv(self):
        """Export visible session data to CSV using list_sessions()."""
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Export CSV", "learning_sessions.csv", "CSV Files (*.csv)"
            )
            if not file_path:
                return

            sessions = list_sessions(100000) or []
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(HEADERS)
                for s in sessions:
                    # Expected tuple layout from list_sessions:
                    # (id, date, language, type, name, status, hours, notes, tags, difficulty, topic, points, progress)
                    row = [
                        s[0],           # ID
                        s[1],           # Date
                        s[2],           # Language
                        s[3],           # Type
                        s[4],           # Work Item Name
                        "",             # Target Time (separate query if needed)
                        s[5],           # Status
                        s[6],           # Hours
                        s[7],           # Notes
                        s[8],           # Tags
                        s[9],           # Difficulty
                        s[10],          # Topic
                        s[11],          # Points
                        s[12],          # Progress %
                    ]
                    w.writerow(row)

            QMessageBox.information(self, "Export", f"Exported {len(sessions)} sessions to {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export CSV: {e}")

    # ===== Table Reload/Edits =====
    def reload_table(self):
        """Reload table from list_sessions()."""
        self.reloading = True
        try:
            sessions = list_sessions(1000) or []
            self.table.setRowCount(0)

            for s in sessions:
                # s tuple matching export mapping above
                row = self.table.rowCount()
                self.table.insertRow(row)

                display = [
                    s[0],                   # ID
                    s[1],                   # Date
                    s[2],                   # Language
                    s[3],                   # Type
                    s[4],                   # Work Item Name
                    "",                     # Target Time
                    s[5],                   # Status
                    f"{float(s[6]):.2f}" if s[6] is not None else "0.00",
                    s[7],                   # Notes
                    s[8],                   # Tags
                    s[9],                   # Difficulty
                    s[10],                  # Topic
                    f"{float(s[11]):.2f}" if s[11] is not None else "0.00",  # Points
                    f"{float(s[12]):.1f}%" if s[12] not in (None, "", 0) else "",  # Progress
                ]

                for c, val in enumerate(display):
                    it = QTableWidgetItem("" if val is None else str(val))
                    # Make computed columns read-only
                    if c in (0, 12, 13):  # ID, Points, Progress %
                        it.setFlags(it.flags() & ~Qt.ItemIsEditable)
                    # Limit editability to defined columns
                    if HEADERS[c] not in EDITABLE_COLS and c not in (0, 12, 13):
                        # leave default flags (editable via delegates if assigned)
                        pass
                    self.table.setItem(row, c, it)

            self.table.resizeRowsToContents()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load data: {e}")
        finally:
            self.reloading = False

    def on_cell_changed(self, item):"""
    Persist inline edits for the changed row and recompute Points.
    Safe no-op during bulk reloads.
    """
    if self.reloading:
        return
    try:
        row = item.row()

        # helper to get a cell by header name
        def cell(header: str) -> str:
            col = HEADERS.index(header)
            it = self.table.item(row, col)
            return "" if it is None else it.text().strip()

        # session id (read-only col 0)
        id_item = self.table.item(row, 0)
        if not id_item or not id_item.text().strip():
            return
        session_id = int(id_item.text())

        # gather values
        date_str   = cell("Date") or QDate.currentDate().toString("yyyy-MM-dd")
        status     = cell("Status") or "In Progress"
        notes      = cell("Notes")
        tags       = cell("Tags")
        difficulty = cell("Difficulty") or "Beginner"
        topic      = cell("Topic")

        # hours as float
        try:
            hours = float(cell("Hours") or "0")
        except ValueError:
            hours = 0.0
            self.reloading = True
            try:
                self.table.item(row, HEADERS.index("Hours")).setText("0.00")
            finally:
                self.reloading = False

        # compute points
        cfg = get_config() or {}
        diff_w   = (cfg.get("difficulty_weights") or {}).get(difficulty, 1.0)
        status_m = (cfg.get("status_multipliers") or {}).get(status, 1.0)
        points = float(hours) * float(diff_w) * float(status_m)

        # persist
        payload = {
            "id": session_id,
            "date": date_str,
            "status": status,
            "hours_spent": hours,
            "notes": notes,
            "tags": tags,
            "difficulty": difficulty,
            "topic": topic,
            "points_awarded": points,
        }
        insert_or_update_session(payload)

        # reflect points and optionally refresh if hours/status changed
        self.reloading = True
        try:
            self.table.item(row, HEADERS.index("Points")).setText(f"{points:.2f}")
            if item.column() in (HEADERS.index("Hours"), HEADERS.index("Status")):
                self.reload_table()
        finally:
            self.reloading = False

    except Exception as e:
        print(f"[on_cell_changed] {e}")
