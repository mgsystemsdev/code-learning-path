"""
Smart Learning Tracker — PySide6 UI Scaffold
Layered, signal-driven scaffold aligned to your Master Spec (Form 13 fields, Table 17 fields).

Run:
  python smart_tracker_app.py

Notes:
- Pure scaffold: wires UI widgets, signals, validators, and presenter callbacks.
- Domain/use cases are injected via `AppServices` so you can swap implementations.
- Autofill hooks are clearly marked; connect to your JSON brain + DTOs when ready.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
from datetime import date, datetime

from PySide6 import QtCore, QtGui, QtWidgets as Qt
from PySide6.QtWidgets import QHeaderView

# ────────────────────────────────────────────────────────────────────────────────
# Shared Types (DTO-shaped, minimal for UI wiring)
# ────────────────────────────────────────────────────────────────────────────────

@dataclass
class SessionRow:
    session_id: str
    logged_at: datetime
    session_date: date
    language: str
    work_item: str
    skill: str
    category_type: str
    category_topic: str
    category_source: str
    difficulty: str
    status: str
    hours_spent: float
    target_hours: float
    points: float
    progress_pct: float
    tags: str
    notes: str

# ────────────────────────────────────────────────────────────────────────────────
# App Services (ports/presenters) — inject real implementations later
# ────────────────────────────────────────────────────────────────────────────────

class AppServices(QtCore.QObject):
    sessionSaved = QtCore.Signal(SessionRow)
    sessionUpdated = QtCore.Signal(SessionRow)
    publishProgress = QtCore.Signal(str)  # "queued|ok|error" or messages

    def __init__(self, parent: Optional[QtCore.QObject]=None):
        super().__init__(parent)
        # TODO: wire real use cases (LogSessionUseCase, etc.)

    @QtCore.Slot(dict)
    def log_session(self, payload: dict):
        """Pretend-log a session; emit a computed row.
        Replace with real application layer call.
        """
        now = datetime.utcnow()
        row = SessionRow(
            session_id=QtCore.QUuid.createUuid().toString(),
            logged_at=now,
            session_date=payload.get("session_date", date.today()),
            language=payload.get("language", "py"),
            work_item=payload.get("work_item", ""),
            skill=payload.get("skill", payload.get("work_item", "").title()),
            category_type=payload.get("category_type", "exercise"),
            category_topic=payload.get("category_topic", ""),
            category_source=payload.get("category_source", ""),
            difficulty=payload.get("difficulty", "beginner"),
            status=payload.get("status", "in_progress"),
            hours_spent=float(payload.get("hours_spent", 0.0)),
            target_hours=float(payload.get("target_hours", 10.0)),
            points=self._compute_points(
                float(payload.get("hours_spent", 0.0)),
                payload.get("difficulty", "beginner"),
                payload.get("status", "in_progress"),
            ),
            progress_pct=self._calc_progress(
                float(payload.get("hours_spent", 0.0)),
                float(payload.get("target_hours", 10.0)),
            ),
            tags=payload.get("tags", ""),
            notes=payload.get("notes", ""),
        )
        self.sessionSaved.emit(row)
        self.publishProgress.emit("queued")

    def _compute_points(self, hours: float, difficulty: str, status: str) -> float:
        weights = {"beginner": 1.0, "intermediate": 1.5, "advanced": 2.0}
        status_mult = {"in_progress": 1.0, "completed": 1.2, "dropped": 0.0}
        return round(hours * weights.get(difficulty, 1.0) * status_mult.get(status, 1.0), 2)

    def _calc_progress(self, hours: float, target: float) -> float:
        if target <= 0: return 0.0
        return round(min(100.0, (hours / target) * 100.0), 1)

# ────────────────────────────────────────────────────────────────────────────────
# Table Model (17 columns per spec)
# ────────────────────────────────────────────────────────────────────────────────

TABLE_HEADERS = [
    "ID", "Logged At", "Session Date", "Language", "Work Item", "Skill",
    "Category Type", "Category Topic", "Category Source", "Difficulty", "Status",
    "Hours Spent", "Target Hours", "Points", "Progress %", "Tags", "Notes"
]

class SessionTableModel(QtCore.QAbstractTableModel):
    def __init__(self, rows: Optional[List[SessionRow]] = None):
        super().__init__()
        self._rows: List[SessionRow] = rows or []

    # Required overrides
    def rowCount(self, parent=QtCore.QModelIndex()) -> int:
        return len(self._rows)

    def columnCount(self, parent=QtCore.QModelIndex()) -> int:
        return len(TABLE_HEADERS)

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return TABLE_HEADERS[section]
        return super().headerData(section, orientation, role)

    def data(self, index: QtCore.QModelIndex, role: int = QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        row = self._rows[index.row()]
        col = index.column()
        if role in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole):
            mapping = [
                row.session_id,
                row.logged_at.strftime('%Y-%m-%d %H:%M:%S'),
                row.session_date.isoformat(),
                row.language,
                row.work_item,
                row.skill,
                row.category_type,
                row.category_topic,
                row.category_source,
                row.difficulty,
                row.status,
                f"{row.hours_spent:.2f}",
                f"{row.target_hours:.2f}",
                f"{row.points:.2f}",
                f"{row.progress_pct:.1f}",
                row.tags,
                row.notes,
            ]
            return mapping[col]
        return None

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        if not index.isValid():
            return QtCore.Qt.NoItemFlags
        # Non-editable: ID, Logged At, Points, Progress % (per spec)
        non_editable_cols = {0, 1, 13, 14}
        flags = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
        if index.column() not in non_editable_cols:
            flags |= QtCore.Qt.ItemIsEditable
        return flags

    def setData(self, index: QtCore.QModelIndex, value, role: int = QtCore.Qt.EditRole) -> bool:
        if role != QtCore.Qt.EditRole or not index.isValid():
            return False
        row = self._rows[index.row()]
        col = index.column()
        # Simple parsing for numeric fields
        try:
            if col in (11, 12):
                value = float(value)
        except Exception:
            return False

        # Apply edits
        attrs = [
            "session_id", "logged_at", "session_date", "language", "work_item",
            "skill", "category_type", "category_topic", "category_source",
            "difficulty", "status", "hours_spent", "target_hours",
            "points", "progress_pct", "tags", "notes"
        ]
        attr = attrs[col]
        if attr in ("points", "progress_pct", "session_id", "logged_at"):
            return False  # non-editable
        setattr(row, attr, value)
        # Recompute if hours/difficulty/status changed
        if attr in ("hours_spent", "difficulty", "status", "target_hours"):
            # lightweight recompute to keep UX faithful to spec
            services = getattr(self, "_services", None)
            if isinstance(services, AppServices):
                row.points = services._compute_points(row.hours_spent, row.difficulty, row.status)
                row.progress_pct = services._calc_progress(row.hours_spent, row.target_hours)
        self.dataChanged.emit(index, index, [QtCore.Qt.DisplayRole])
        return True

    # External API
    def attach_services(self, services: AppServices):
        self._services = services

    def add_row(self, row: SessionRow):
        self.beginInsertRows(QtCore.QModelIndex(), len(self._rows), len(self._rows))
        self._rows.append(row)
        self.endInsertRows()

# ────────────────────────────────────────────────────────────────────────────────
# Form Widget (13 fields) — with autofill hooks
# ────────────────────────────────────────────────────────────────────────────────

class SessionForm(Qt.QWidget):
    submitRequested = QtCore.Signal(dict)

    def __init__(self, parent: Optional[Qt.QWidget] = None):
        super().__init__(parent)
        self._build()
        self._wire()

    def _build(self):
        self.setLayout(Qt.QVBoxLayout())

        grid = Qt.QGridLayout()
        r = 0
        # 1) Session Date
        self.date = Qt.QDateEdit(QtCore.QDate.currentDate())
        self.date.setCalendarPopup(True)
        grid.addWidget(Qt.QLabel("Session Date"), r, 0)
        grid.addWidget(self.date, r, 1); r += 1

        # 2) Language
        self.lang = Qt.QComboBox(); self.lang.setEditable(True)
        self.lang.addItems(["py", "js"])  # seed; will grow inline
        grid.addWidget(Qt.QLabel("Language"), r, 0)
        grid.addWidget(self.lang, r, 1); r += 1

        # 3) Work Item (raw)
        self.work = Qt.QLineEdit(); self.work.setPlaceholderText("e.g., Flask routing, arrays")
        grid.addWidget(Qt.QLabel("Work Item"), r, 0)
        grid.addWidget(self.work, r, 1); r += 1

        # 4) Skill (autofilled editable via ComboBox)
        self.skill = Qt.QComboBox(); self.skill.setEditable(True)
        grid.addWidget(Qt.QLabel("Skill"), r, 0)
        grid.addWidget(self.skill, r, 1); r += 1

        # 5) Category Type (fixed)
        self.cat_type = Qt.QComboBox(); self.cat_type.addItems(["exercise", "project"]) 
        grid.addWidget(Qt.QLabel("Category Type"), r, 0)
        grid.addWidget(self.cat_type, r, 1); r += 1

        # 6) Category Topic
        self.cat_topic = Qt.QComboBox(); self.cat_topic.setEditable(True)
        grid.addWidget(Qt.QLabel("Category Topic"), r, 0)
        grid.addWidget(self.cat_topic, r, 1); r += 1

        # 7) Category Source
        self.cat_source = Qt.QComboBox(); self.cat_source.setEditable(True)
        grid.addWidget(Qt.QLabel("Category Source"), r, 0)
        grid.addWidget(self.cat_source, r, 1); r += 1

        # 8) Difficulty (fixed enum)
        self.difficulty = Qt.QComboBox(); self.difficulty.addItems(["beginner", "intermediate", "advanced"]) 
        grid.addWidget(Qt.QLabel("Difficulty"), r, 0)
        grid.addWidget(self.difficulty, r, 1); r += 1

        # 9) Status (fixed enum)
        self.status = Qt.QComboBox(); self.status.addItems(["in_progress", "completed", "dropped"]) 
        grid.addWidget(Qt.QLabel("Status"), r, 0)
        grid.addWidget(self.status, r, 1); r += 1

        # 10) Hours Spent (required)
        self.hours = Qt.QDoubleSpinBox(); self.hours.setRange(0.0, 200.0); self.hours.setSingleStep(0.25)
        grid.addWidget(Qt.QLabel("Hours Spent"), r, 0)
        grid.addWidget(self.hours, r, 1); r += 1

        # 11) Target Hours (defaulted)
        self.target = Qt.QDoubleSpinBox(); self.target.setRange(1.0, 200.0); self.target.setSingleStep(0.5)
        self.target.setValue(10.0)
        grid.addWidget(Qt.QLabel("Target Hours"), r, 0)
        grid.addWidget(self.target, r, 1); r += 1

        # 12) Tags (comma-separated)
        self.tags = Qt.QLineEdit(); self.tags.setPlaceholderText("comma-separated")
        grid.addWidget(Qt.QLabel("Tags"), r, 0)
        grid.addWidget(self.tags, r, 1); r += 1

        # 13) Notes (multiline)
        self.notes = Qt.QTextEdit(); self.notes.setPlaceholderText("Optional notes (max 2000 chars)")
        grid.addWidget(Qt.QLabel("Notes"), r, 0)
        grid.addWidget(self.notes, r, 1); r += 1

        self.submit = Qt.QPushButton("Save Session")

        self.layout().addLayout(grid)
        self.layout().addWidget(self.submit)

    def _wire(self):
        # Autofill cascade hooks — attach to real resolver later
        self.work.editingFinished.connect(self._on_work_committed)
        self.submit.clicked.connect(self._submit)

    # Father→Son dependency example: Work Item → Skill, Difficulty, Target, Tags, Status
    def _on_work_committed(self):
        text = self.work.text().strip()
        if not text:
            return
        # Placeholder alias resolution
        resolved_skill = text.title()
        if self.skill.findText(resolved_skill) == -1:
            self.skill.addItem(resolved_skill)
        self.skill.setCurrentText(resolved_skill)
        # Defaults (simulate JSON brain)
        if self.difficulty.currentText() == "":
            self.difficulty.setCurrentText("beginner")
        if self.target.value() <= 0:
            self.target.setValue(10.0)
        if not self.tags.text():
            self.tags.setText(",".join(sorted({t.lower() for t in text.split()})))

    def _submit(self):
        # Minimal validation per spec
        if self.hours.value() <= 0.0:
            Qt.QMessageBox.warning(self, "Validation", "Hours Spent must be > 0")
            return
        payload = {
            "session_date": self.date.date().toPython(),
            "language": self.lang.currentText().strip(),
            "work_item": self.work.text().strip(),
            "skill": self.skill.currentText().strip(),
            "category_type": self.cat_type.currentText(),
            "category_topic": self.cat_topic.currentText().strip(),
            "category_source": self.cat_source.currentText().strip(),
            "difficulty": self.difficulty.currentText(),
            "status": self.status.currentText(),
            "hours_spent": float(self.hours.value()),
            "target_hours": float(self.target.value()),
            "tags": self.tags.text().strip(),
            "notes": self.notes.toPlainText()[:2000],
        }
        self.submitRequested.emit(payload)

# ────────────────────────────────────────────────────────────────────────────────
# Dashboard (Modal, read-only cards)
# ────────────────────────────────────────────────────────────────────────────────

class DashboardDialog(Qt.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Dashboard — Progress & Streaks")
        self.resize(720, 420)
        layout = Qt.QVBoxLayout(self)
        self.summary = Qt.QLabel("No data yet. Log a session to see stats.")
        layout.addWidget(self.summary)

    def render_summary(self, rows: List[SessionRow]):
        by_lang = {}
        for r in rows:
            acc = by_lang.setdefault(r.language, {"hours": 0.0, "points": 0.0, "logs": 0})
            acc["hours"] += r.hours_spent
            acc["points"] += r.points
            acc["logs"] += 1
        lines = ["<b>By Language</b>"]
        for lang, acc in by_lang.items():
            lines.append(f"{lang}: {acc['hours']:.2f}h · {acc['points']:.0f} pts · {acc['logs']} logs")
        self.summary.setText("<br>".join(lines) if rows else "No data yet.")

# ────────────────────────────────────────────────────────────────────────────────
# Main Window — Always-visible Table + Entry Form + Dashboard button
# ────────────────────────────────────────────────────────────────────────────────

class MainWindow(Qt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Learning Tracker — Desktop")
        self.resize(1900, 720)

        # Services & Data Model
        self.services = AppServices(self)
        self.model = SessionTableModel()
        self.model.attach_services(self.services)

        # Central layout
        central = Qt.QWidget(); self.setCentralWidget(central)
        hbox = Qt.QHBoxLayout(central)

        # Left: Form
        self.form = SessionForm(self)
        self.form.setFixedWidth(250)  # Set the form width to 350 pixels (adjust as needed)
        hbox.addWidget(self.form, 1)
        
        # Right: Table
        right = Qt.QWidget()
        right_layout = Qt.QVBoxLayout()
        right.setLayout(right_layout)
        self.table = Qt.QTableView()
        self.table.setModel(self.model)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSortingEnabled(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # Make columns fit window
        self.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)  # Remove horizontal scroll bar
        right_layout.addWidget(self.table)

        # Toolbar
        tb = Qt.QToolBar()
        self.addToolBar(tb)
        self.btn_dashboard = QtGui.QAction("Dashboard", self)
        tb.addAction(self.btn_dashboard)

        hbox.addWidget(right, 2)

        # Signals
        self.form.submitRequested.connect(self.services.log_session)
        self.services.sessionSaved.connect(self._on_session_saved)
        self.btn_dashboard.triggered.connect(self._open_dashboard)

        # Status bar feedback for publish queue
        self.statusBar().showMessage("Ready")
        self.services.publishProgress.connect(lambda s: self.statusBar().showMessage(f"Publish: {s}"))

        # Center the window on the screen
        screen_geometry = Qt.QApplication.primaryScreen().geometry()
        window_geometry = self.geometry()
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        self.move(x, y)

    @QtCore.Slot(SessionRow)
    def _on_session_saved(self, row: SessionRow):
        self.model.add_row(row)
        self.statusBar().showMessage("Session saved · queued for publish")

    def _open_dashboard(self):
        dlg = DashboardDialog(self)
        # Extract rows from the model
        rows = [self.model._rows[i] for i in range(self.model.rowCount())]
        dlg.render_summary(rows)
        dlg.exec()

# ────────────────────────────────────────────────────────────────────────────────
# Entrypoint
# ────────────────────────────────────────────────────────────────────────────────

def main():
    app = Qt.QApplication([])
    win = MainWindow()
    win.show()
    app.exec()

if __name__ == "__main__":
    main()
