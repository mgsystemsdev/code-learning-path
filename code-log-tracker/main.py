# app/main.py
# --- HiDPI fixes must be set BEFORE creating QApplication ---
import os
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"

import sys, csv
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QDoubleSpinBox,
    QLineEdit, QMessageBox, QFileDialog, QDateEdit, QAbstractItemView,
    QHeaderView, QStyledItemDelegate
)
from PySide6.QtCore import Qt, QDate, QObject, Signal
from PySide6.QtGui import QPalette, QGuiApplication

# Remove deprecated HiDPI attribute
QGuiApplication.setHighDpiScaleFactorRoundingPolicy(
    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
)

from app.db import (
    init_db, fetch_lookup, insert_or_update_session, list_sessions,
    get_weights, project_target_hours, project_logged_hours
)

# ---------- Friendly headers (table) ----------
HEADERS = [
    "ID", "Date", "Type", "Exercise Name", "Project Name", "Activity Name",
    "Notes", "Status", "Hours", "Tags", "Difficulty Level", "Topic Area",
    "Points", "Progress %"
]

# ---------- DB keys order (must match list_sessions / insert_or_update_session) ----------
KEYS = [
    "id","date","type","exercise_name","project_name","activity_name",
    "description","lifecycle","hours_spent","tags","difficulty","domain",
    "points_awarded","project_progress_pct"
]

# Editable columns (inline)
EDITABLE_COLS = {
    "date","type","exercise_name","project_name","activity_name",
    "description","lifecycle","hours_spent","tags","difficulty","domain"
}

# ---------- Keyword maps for auto-fill ----------
KW_DIFF = {
    "Beginner": ["variables","syntax","loops","if","lists","strings","functions","basics"],
    "Intermediate": ["classes","exceptions","files","testing","pytest","sql","pandas","apis","auth","regex","docker"],
    "Advanced": ["algorithms","async","kafka","spark","kubernetes","ml","xgboost","prophet","llm","security","jwt","encryption"]
}
KW_DOMAIN = {
    "Python Basics": ["variables","syntax","loops","functions","basics"],
    "APIs": ["api","http","auth","jwt","rest","fastapi"],
    "Data": ["pandas","eda","csv","etl","sql","join"],
    "ML": ["xgboost","prophet","lstm","model","ml"],
    "DevOps": ["docker","kubernetes","ci","deploy","refactor"],
    "Security": ["encryption","rbac","oauth","jwt","security"],
    "Cloud": ["aws","azure","gcp","s3","eks"],
    "DB/SQL": ["postgres","migrations","joins","sql"],
    "Frontend": ["react","streamlit","dash","ui","dashboard"],
}

# ---------- Stable Delegates ----------
class DateDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        ed = QDateEdit(parent)
        ed.setCalendarPopup(True)
        ed.setDisplayFormat("yyyy-MM-dd")
        return ed
        
    def setEditorData(self, editor, index):
        txt = index.data() or QDate.currentDate().toString("yyyy-MM-dd")
        try:
            if isinstance(txt, str) and len(txt) == 10:
                y, m, d = [int(x) for x in txt.split("-")]
                editor.setDate(QDate(y, m, d))
            else:
                editor.setDate(QDate.currentDate())
        except (ValueError, IndexError):
            editor.setDate(QDate.currentDate())
            
    def setModelData(self, editor, model, index):
        model.setData(index, editor.date().toString("yyyy-MM-dd"))

class ComboDelegate(QStyledItemDelegate):
    def __init__(self, choices_func, allow_blank=True, parent=None, editable=True):
        super().__init__(parent)
        self.choices_func = choices_func
        self.allow_blank = allow_blank
        self.editable = editable
        
    def createEditor(self, parent, option, index):
        cb = QComboBox(parent)
        if self.allow_blank:
            cb.addItem("")
        try:
            choices = self.choices_func()
            if choices:
                cb.addItems(choices)
        except Exception:
            pass  # Fallback for missing data
        cb.setEditable(self.editable)
        return cb
        
    def setEditorData(self, editor, index):
        val = str(index.data() or "")
        idx = editor.findText(val)
        if idx < 0 and val and self.editable:
            editor.addItem(val)
            idx = editor.findText(val)
        editor.setCurrentIndex(max(0, idx))
        
    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentText())

class HoursDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        sp = QDoubleSpinBox(parent)
        sp.setRange(0, 24)
        sp.setSingleStep(0.25)
        sp.setDecimals(2)
        return sp
        
    def setEditorData(self, editor, index):
        try:
            v = float(index.data() or 0.0)
        except (ValueError, TypeError):
            v = 0.0
        editor.setValue(v)
        
    def setModelData(self, editor, model, index):
        model.setData(index, f"{editor.value():.2f}")

class MainWindow(QMainWindow):
    # Bottom template fields (properly separated)
    BOTTOM_FIELDS = [
        "Date","Type","Exercise Name","Project Name","Activity Name",
        "Notes","Status","Hours","Tags","Difficulty Level","Topic Area"
    ]

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Learning Tracker")
        self.resize(1280, 760)
        
        # Initialize flags
        self.reloading = False
        self.updating_template = False
        
        # Initialize database
        try:
            init_db()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to initialize database: {e}")
            return

        self.setup_ui()
        self.reload_table()

    def setup_ui(self):
        # --- Main Table ---
        self.table = QTableWidget(0, len(HEADERS))
        self.table.setHorizontalHeaderLabels(HEADERS)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setWordWrap(False)
        
        # Stable styling
        self.table.setStyleSheet("""
            QTableWidget::item:selected { 
                background: #dbeafe; 
                color: black;
            }
            QTableWidget { 
                gridline-color: #e5e7eb;
                selection-background-color: #dbeafe;
            }
        """)
        
        # Header configuration
        hdr = self.table.horizontalHeader()
        hdr.setSectionResizeMode(QHeaderView.Stretch)
        hdr.setMinimumSectionSize(80)
        
        # Edit triggers
        self.table.setEditTriggers(
            QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked
        )
        
        # Install delegates safely
        self.install_delegates()
        
        # Connect signals
        self.table.itemChanged.connect(self.on_cell_changed)

        # --- Toolbar ---
        self.setup_toolbar()

        # --- Bottom Template ---
        self.labels_layout, self.inputs_layout = self.build_bottom_template()

        # --- Main Layout ---
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.toolbar_layout)
        main_layout.addWidget(self.table, 1)  # Give table most space
        main_layout.addLayout(self.labels_layout)
        main_layout.addLayout(self.inputs_layout)
        
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Platform-specific styling
        if sys.platform == "darwin":  # macOS
            pal = self.palette()
            pal.setColor(QPalette.AlternateBase, pal.color(QPalette.Base).lighter(104))
            self.setPalette(pal)

    def setup_toolbar(self):
        self.toolbar_layout = QHBoxLayout()
        
        # Create buttons
        self.add_btn = QPushButton("Add Row")
        self.save_btn = QPushButton("Save Row")
        self.del_btn = QPushButton("Delete Row")
        self.export_btn = QPushButton("Export CSV")
        
        # Connect signals
        self.add_btn.clicked.connect(self.add_row)
        self.save_btn.clicked.connect(self.save_row)
        self.del_btn.clicked.connect(self.delete_row)
        self.export_btn.clicked.connect(self.export_csv)
        
        # Add to layout
        self.toolbar_layout.addWidget(self.add_btn)
        self.toolbar_layout.addWidget(self.save_btn)
        self.toolbar_layout.addWidget(self.del_btn)
        self.toolbar_layout.addStretch()
        self.toolbar_layout.addWidget(self.export_btn)

    def install_delegates(self):
        try:
            col_map = {header: i for i, header in enumerate(HEADERS)}
            
            # Date delegate
            if "Date" in col_map:
                self.table.setItemDelegateForColumn(col_map["Date"], DateDelegate(self.table))
            
            # Type delegate
            if "Type" in col_map:
                self.table.setItemDelegateForColumn(
                    col_map["Type"], 
                    ComboDelegate(lambda: ["Exercise", "Project"], allow_blank=False, parent=self.table)
                )
            
            # Status delegate
            if "Status" in col_map:
                self.table.setItemDelegateForColumn(
                    col_map["Status"], 
                    ComboDelegate(lambda: fetch_lookup("lifecycle"), parent=self.table)
                )
            
            # Difficulty delegate
            if "Difficulty Level" in col_map:
                self.table.setItemDelegateForColumn(
                    col_map["Difficulty Level"], 
                    ComboDelegate(lambda: fetch_lookup("difficulty"), parent=self.table)
                )
            
            # Topic Area delegate
            if "Topic Area" in col_map:
                self.table.setItemDelegateForColumn(
                    col_map["Topic Area"], 
                    ComboDelegate(lambda: fetch_lookup("domain"), parent=self.table)
                )
            
            # Hours delegate
            if "Hours" in col_map:
                self.table.setItemDelegateForColumn(col_map["Hours"], HoursDelegate(self.table))
                
        except Exception as e:
            print(f"Warning: Failed to install delegates: {e}")

    def build_bottom_template(self):
        # Labels row
        labels_layout = QHBoxLayout()
        labels_layout.setSpacing(5)
        self.label_widgets = {}
        
        # Define field widths for better readability
        field_widths = {
            "Date": 100,
            "Type": 80,
            "Exercise Name": 150,
            "Project Name": 200,
            "Activity Name": 150,
            "Notes": 180,
            "Status": 100,
            "Hours": 70,
            "Tags": 120,
            "Difficulty Level": 120,
            "Topic Area": 120
        }
        
        for title in self.BOTTOM_FIELDS:
            label = QLabel(title)
            label.setStyleSheet("font-weight: 600; padding: 2px; font-size: 11px;")
            label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            label.setMinimumWidth(field_widths.get(title, 100))
            label.setMaximumWidth(field_widths.get(title, 100))
            labels_layout.addWidget(label)
            self.label_widgets[title] = label

        # Inputs row
        inputs_layout = QHBoxLayout()
        inputs_layout.setSpacing(5)
        self.input_widgets = {}

        # Date input - separate dedicated field
        date_input = QDateEdit()
        date_input.setCalendarPopup(True)
        date_input.setDate(QDate.currentDate())
        date_input.setMinimumWidth(field_widths["Date"])
        date_input.setMaximumWidth(field_widths["Date"])
        inputs_layout.addWidget(date_input)
        self.input_widgets["Date"] = date_input

        # Type combo - separate dedicated field
        type_combo = QComboBox()
        type_combo.addItem("")
        type_combo.addItems(["Exercise", "Project"])
        type_combo.currentTextChanged.connect(self.apply_type_dependency)
        type_combo.setMinimumWidth(field_widths["Type"])
        type_combo.setMaximumWidth(field_widths["Type"])
        inputs_layout.addWidget(type_combo)
        self.input_widgets["Type"] = type_combo

        # Exercise Name combo - separate dedicated field
        exercise_combo = QComboBox()
        exercise_combo.setEditable(True)
        exercise_combo.addItem("")
        try:
            exercise_combo.addItems(fetch_lookup("exercises"))
        except Exception:
            pass
        exercise_combo.currentTextChanged.connect(self.auto_fill_from_text)
        exercise_combo.setMinimumWidth(field_widths["Exercise Name"])
        exercise_combo.setMaximumWidth(field_widths["Exercise Name"])
        inputs_layout.addWidget(exercise_combo)
        self.input_widgets["Exercise Name"] = exercise_combo

        # Project Name combo - separate dedicated field
        project_combo = QComboBox()
        project_combo.setEditable(True)
        project_combo.addItem("")
        try:
            project_combo.addItems(fetch_lookup("projects"))
        except Exception:
            pass
        project_combo.setMinimumWidth(field_widths["Project Name"])
        project_combo.setMaximumWidth(field_widths["Project Name"])
        project_combo.setToolTip("Project Name - Long names will show in tooltip")
        inputs_layout.addWidget(project_combo)
        self.input_widgets["Project Name"] = project_combo

        # Activity Name combo - separate dedicated field
        activity_combo = QComboBox()
        activity_combo.setEditable(True)
        activity_combo.addItem("")
        try:
            activity_combo.addItems(fetch_lookup("activities"))
        except Exception:
            pass
        activity_combo.currentTextChanged.connect(self.auto_fill_from_text)
        activity_combo.setMinimumWidth(field_widths["Activity Name"])
        activity_combo.setMaximumWidth(field_widths["Activity Name"])
        activity_combo.setToolTip("Activity Name")
        inputs_layout.addWidget(activity_combo)
        self.input_widgets["Activity Name"] = activity_combo

        # Notes input - separate dedicated field
        notes_input = QLineEdit()
        notes_input.setPlaceholderText("What did you do?")
        notes_input.textChanged.connect(self.auto_fill_from_text)
        notes_input.setMinimumWidth(field_widths["Notes"])
        notes_input.setMaximumWidth(field_widths["Notes"])
        inputs_layout.addWidget(notes_input)
        self.input_widgets["Notes"] = notes_input

        # Status combo - separate dedicated field
        status_combo = QComboBox()
        status_combo.addItem("")
        try:
            status_combo.addItems(fetch_lookup("lifecycle"))
        except Exception:
            pass
        status_combo.setMinimumWidth(field_widths["Status"])
        status_combo.setMaximumWidth(field_widths["Status"])
        inputs_layout.addWidget(status_combo)
        self.input_widgets["Status"] = status_combo

        # Hours input - separate dedicated field
        hours_input = QDoubleSpinBox()
        hours_input.setRange(0, 24)
        hours_input.setSingleStep(0.25)
        hours_input.setDecimals(2)
        hours_input.setMinimumWidth(field_widths["Hours"])
        hours_input.setMaximumWidth(field_widths["Hours"])
        inputs_layout.addWidget(hours_input)
        self.input_widgets["Hours"] = hours_input

        # Tags input - separate dedicated field
        tags_input = QLineEdit()
        tags_input.setPlaceholderText("comma, separated, tags")
        tags_input.setMinimumWidth(field_widths["Tags"])
        tags_input.setMaximumWidth(field_widths["Tags"])
        inputs_layout.addWidget(tags_input)
        self.input_widgets["Tags"] = tags_input

        # Difficulty combo - separate dedicated field
        difficulty_combo = QComboBox()
        difficulty_combo.addItem("")
        try:
            difficulty_combo.addItems(fetch_lookup("difficulty"))
        except Exception:
            pass
        difficulty_combo.setMinimumWidth(field_widths["Difficulty Level"])
        difficulty_combo.setMaximumWidth(field_widths["Difficulty Level"])
        inputs_layout.addWidget(difficulty_combo)
        self.input_widgets["Difficulty Level"] = difficulty_combo

        # Topic Area combo - separate dedicated field
        topic_combo = QComboBox()
        topic_combo.addItem("")
        try:
            topic_combo.addItems(fetch_lookup("domain"))
        except Exception:
            pass
        topic_combo.setMinimumWidth(field_widths["Topic Area"])
        topic_combo.setMaximumWidth(field_widths["Topic Area"])
        inputs_layout.addWidget(topic_combo)
        self.input_widgets["Topic Area"] = topic_combo

        return labels_layout, inputs_layout

    def apply_type_dependency(self, type_text):
        if self.updating_template:
            return
            
        type_text = (type_text or "").strip()
        is_exercise = type_text == "Exercise"
        is_project = type_text == "Project"

        # Enable/disable fields based on type
        self.input_widgets["Exercise Name"].setEnabled(is_exercise)
        self.input_widgets["Project Name"].setEnabled(is_project)
        self.input_widgets["Activity Name"].setEnabled(is_project)

        # Clear disabled fields
        if not is_exercise:
            self.input_widgets["Exercise Name"].setCurrentIndex(0)
        if not is_project:
            self.input_widgets["Project Name"].setCurrentIndex(0)
            self.input_widgets["Activity Name"].setCurrentIndex(0)

    def auto_fill_from_text(self):
        if self.updating_template:
            return
            
        try:
            text = " ".join([
                self.input_widgets["Exercise Name"].currentText() or "",
                self.input_widgets["Activity Name"].currentText() or "",
                self.input_widgets["Notes"].text() or ""
            ]).lower()

            # Auto-fill difficulty
            best_diff, best_hits = None, -1
            for diff, keywords in KW_DIFF.items():
                hits = sum(1 for kw in keywords if kw in text)
                if hits > best_hits:
                    best_hits, best_diff = hits, diff

            if best_diff:
                diff_combo = self.input_widgets["Difficulty Level"]
                idx = diff_combo.findText(best_diff)
                if idx >= 0:
                    diff_combo.setCurrentIndex(idx)

            # Auto-fill domain
            best_domain, best_hits = None, -1
            for domain, keywords in KW_DOMAIN.items():
                hits = sum(1 for kw in keywords if kw in text)
                if hits > best_hits:
                    best_hits, best_domain = hits, domain

            if best_domain:
                domain_combo = self.input_widgets["Topic Area"]
                idx = domain_combo.findText(best_domain)
                if idx >= 0:
                    domain_combo.setCurrentIndex(idx)
                    
        except Exception as e:
            print(f"Warning: Auto-fill failed: {e}")

    def clear_template(self):
        self.updating_template = True
        try:
            self.input_widgets["Date"].setDate(QDate.currentDate())
            
            # Clear combo boxes
            for field in ["Type", "Exercise Name", "Project Name", "Activity Name", 
                         "Status", "Difficulty Level", "Topic Area"]:
                self.input_widgets[field].setCurrentIndex(0)
            
            # Clear text fields
            self.input_widgets["Notes"].clear()
            self.input_widgets["Tags"].clear()
            
            # Reset hours
            self.input_widgets["Hours"].setValue(0.0)
        finally:
            self.updating_template = False

    def add_row(self):
        self.clear_template()
        self.apply_type_dependency("")

    def save_row(self):
        try:
            # Validate type
            type_text = (self.input_widgets["Type"].currentText() or "").strip()
            if not type_text:
                QMessageBox.warning(self, "Validation", "Type is required.")
                return

            # Get form values
            date_str = self.input_widgets["Date"].date().toString("yyyy-MM-dd")
            is_exercise = type_text == "Exercise"
            is_project = type_text == "Project"

            exercise_name = self.input_widgets["Exercise Name"].currentText().strip()
            project_name = self.input_widgets["Project Name"].currentText().strip()
            activity_name = self.input_widgets["Activity Name"].currentText().strip()
            notes = self.input_widgets["Notes"].text().strip()

            # Validate based on type
            if is_exercise:
                if not exercise_name and not notes:
                    QMessageBox.warning(self, "Validation", "Exercise needs Exercise Name or Notes.")
                    return
                if project_name or activity_name:
                    QMessageBox.warning(self, "Validation", "Exercise rows cannot set Project/Activity.")
                    return
            elif is_project:
                if not project_name:
                    QMessageBox.warning(self, "Validation", "Project rows need Project Name.")
                    return
                if exercise_name:
                    QMessageBox.warning(self, "Validation", "Project rows cannot set Exercise Name.")
                    return

            # Calculate points
            try:
                diff_weights, life_mults = get_weights()
            except Exception:
                diff_weights, life_mults = {"Beginner": 1.0}, {"Planned": 1.0}

            hours = float(self.input_widgets["Hours"].value())
            difficulty = self.input_widgets["Difficulty Level"].currentText() or "Beginner"
            lifecycle = self.input_widgets["Status"].currentText() or "Planned"

            points = hours * diff_weights.get(difficulty, 1.0) * life_mults.get(lifecycle, 1.0)

            # Calculate progress PREVIEW for Projects only
            progress_preview = 0.0
            logged = 0.0
            if is_project and project_name:
                try:
                    target = project_target_hours(project_name) or 0.0
                    logged = project_logged_hours(project_name) or 0.0
                    if target > 0:
                        progress_preview = min(100.0, ((logged + hours) / target) * 100.0)
                    else:
                        progress_preview = 0.0
                except Exception as e:
                    print(f"Warning: Progress calculation failed: {e}")
                    progress_preview = 0.0

            # Create row data
            row_data = {
                "id": None,
                "date": date_str,
                "type": type_text,
                "exercise_name": exercise_name if is_exercise else "",
                "project_name": project_name if is_project else "",
                "activity_name": activity_name if is_project else "",
                "description": notes,
                "lifecycle": lifecycle,
                "hours_spent": hours,
                "tags": self.input_widgets["Tags"].text().strip(),
                "difficulty": difficulty,
                "domain": self.input_widgets["Topic Area"].currentText().strip(),
                "points_awarded": points,
                "project_progress_pct": float(f"{progress_preview:.1f}") if is_project else 0.0,  # One decimal place
            }

            # Save to database
            insert_or_update_session(row_data)
            self.reload_table()
            self.clear_template()
            
            # Show success message with progress info for projects
            if is_project and project_name:
                QMessageBox.information(
                    self,
                    "Success",
                    f"Project row saved successfully!\n"
                    f"Progress: {progress_preview:.1f}% ({logged + hours:.1f}h logged)",
                )
            else:
                QMessageBox.information(self, "Success", "Row saved successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save row: {e}")

    def delete_row(self):
        try:
            current_row = self.table.currentRow()
            if current_row < 0:
                QMessageBox.information(self, "Info", "Please select a row to delete.")
                return

            id_item = self.table.item(current_row, 0)
            if not id_item:
                return

            row_id = id_item.text()
            
            # Confirm deletion
            reply = QMessageBox.question(
                self, "Confirm Delete", 
                f"Are you sure you want to delete row {row_id}?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                from app.db import connect
                with connect() as con:
                    cur = con.cursor()
                    cur.execute("DELETE FROM sessions WHERE id=?", (row_id,))
                    con.commit()
                
                self.reload_table()
                QMessageBox.information(self, "Success", "Row deleted successfully!")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete row: {e}")

    def export_csv(self):
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Export CSV", "sessions.csv", "CSV Files (*.csv)"
            )
            if not file_path:
                return

            rows = list_sessions(100000)
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(KEYS)
                for row in rows:
                    writer.writerow(row)

            QMessageBox.information(self, "Export", f"Exported {len(rows)} rows to {file_path}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export CSV: {e}")

    def reload_table(self):
        self.reloading = True
        try:
            rows = list_sessions(1000)
            self.table.setRowCount(0)
            
            for row_data in rows:
                row_index = self.table.rowCount()
                self.table.insertRow(row_index)
                
                for col_index, value in enumerate(row_data):
                    item_text = "" if value is None else str(value)
                    item = QTableWidgetItem(item_text)
                    
                    # Make computed columns read-only
                    key = KEYS[col_index] if col_index < len(KEYS) else ""
                    if key not in EDITABLE_COLS or key == "project_progress_pct":  # Progress is always read-only
                        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    
                    # Special formatting for progress column
                    if key == "project_progress_pct" and item_text and item_text != "0.0":
                        item.setToolTip(f"Project Progress: {item_text}%")
                    
                    self.table.setItem(row_index, col_index, item)
            
            self.table.resizeRowsToContents()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load data: {e}")
        finally:
            self.reloading = False

    def on_cell_changed(self, item):
        if self.reloading:
            return

        try:
            row_idx = item.row()
            id_item = self.table.item(row_idx, 0)
            if not id_item or not id_item.text().strip():
                return

            session_id = int(id_item.text())

            row_values = {}
            for col_idx, key in enumerate(KEYS):
                cell_item = self.table.item(row_idx, col_idx)
                row_values[key] = "" if cell_item is None else cell_item.text()

            try:
                hours = float(row_values["hours_spent"] or 0.0)
            except (ValueError, TypeError):
                hours = 0.0

            try:
                diff_weights, life_mults = get_weights()
            except Exception:
                diff_weights, life_mults = {"Beginner": 1.0}, {"Planned": 1.0}

            difficulty = row_values["difficulty"] or "Beginner"
            lifecycle = row_values["lifecycle"] or "Planned"
            points = hours * diff_weights.get(difficulty, 1.0) * life_mults.get(lifecycle, 1.0)
            row_values["points_awarded"] = f"{points:.2f}"

            row_values["id"] = session_id
            row_values["hours_spent"] = hours
            insert_or_update_session(row_values)

            progress_pct = ""
            if row_values["type"] == "Project" and row_values["project_name"]:
                try:
                    target = project_target_hours(row_values["project_name"]) or 0.0
                    logged = project_logged_hours(row_values["project_name"]) or 0.0
                    progress_pct = f"{min(100.0, (logged / target) * 100.0):.1f}" if target > 0 else "0.0"
                except Exception as e:
                    print(f"Warning: Progress recalculation failed: {e}")
                    progress_pct = "0.0"
            row_values["project_progress_pct"] = progress_pct

            self.reloading = True
            try:
                points_col = KEYS.index("points_awarded")
                progress_col = KEYS.index("project_progress_pct")
                self.table.item(row_idx, points_col).setText(row_values["points_awarded"])
                self.table.item(row_idx, progress_col).setText(row_values["project_progress_pct"])

                progress_item = self.table.item(row_idx, progress_col)
                if progress_item:
                    progress_item.setFlags(progress_item.flags() & ~Qt.ItemIsEditable)
            finally:
                self.reloading = False
        except Exception as e:
            print(f"Error updating cell: {e}")


def main():
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Learning Tracker")
    app.setApplicationVersion("1.0")
    
    try:
        window = MainWindow()
        window.show()
        return app.exec()
    except Exception as e:
        QMessageBox.critical(None, "Startup Error", f"Failed to start application: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
