# app/main.py
# --- HiDPI fixes must be set BEFORE creating QApplication ---
import os
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"

import sys, csv, json
from datetime import datetime, date
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QDoubleSpinBox,
    QLineEdit, QMessageBox, QFileDialog, QDateEdit, QAbstractItemView,
    QHeaderView, QStyledItemDelegate, QDialog, QDialogButtonBox, QListWidget,
    QListWidgetItem, QTextEdit, QGroupBox, QGridLayout, QSpinBox
)
from PySide6.QtCore import Qt, QDate, QObject, Signal
from PySide6.QtGui import QPalette, QGuiApplication, QFont

# Remove deprecated HiDPI attribute
QGuiApplication.setHighDpiScaleFactorRoundingPolicy(
    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
)

from app.db import (
    init_db, get_languages, find_or_create_item, insert_or_update_session,
    list_sessions, get_config, search_items, get_item_by_id, load_language_pack
)

# ---------- Updated Headers ----------
HEADERS = [
    "ID", "Date", "Language", "Type", "Work Item Name", "Target Time",
    "Status", "Hours", "Notes", "Tags", "Difficulty", "Topic", 
    "Points", "Progress %"
]

KEYS = [
    "id", "date", "language_code", "type", "canonical_name", "target_hours",
    "status", "hours_spent", "notes", "tags", "difficulty", 
    "topic", "points_awarded", "progress_pct"
]

# Editable columns
EDITABLE_COLS = {
    "date", "status", "hours_spent", "notes", "tags", "difficulty", "topic"
}

# ---------- Suggestion Dialog ----------
class SuggestionDialog(QDialog):
    def __init__(self, suggestions, work_item_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Similar Items Found")
        self.setModal(True)
        self.selected_item_id = None
        self.create_new = False
        
        layout = QVBoxLayout()
        
        # Message
        msg = QLabel(f"Found similar items to '{work_item_name}'. Choose one or create new:")
        msg.setWordWrap(True)
        layout.addWidget(msg)
        
        # Suggestion list
        self.list_widget = QListWidget()
        for suggestion in suggestions:
            item_text = f"{suggestion['name']} ({suggestion['similarity_hint']})"
            list_item = QListWidgetItem(item_text)
            list_item.setData(Qt.UserRole, suggestion['id'])
            self.list_widget.addItem(list_item)
        
        self.list_widget.itemDoubleClicked.connect(self.accept_suggestion)
        layout.addWidget(self.list_widget)
        
        # Buttons
        button_box = QDialogButtonBox()
        
        use_btn = QPushButton("Use Selected")
        use_btn.clicked.connect(self.accept_suggestion)
        button_box.addButton(use_btn, QDialogButtonBox.AcceptRole)
        
        new_btn = QPushButton("Create New")
        new_btn.clicked.connect(self.create_new_item)
        button_box.addButton(new_btn, QDialogButtonBox.AcceptRole)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_box.addButton(cancel_btn, QDialogButtonBox.RejectRole)
        
        layout.addWidget(button_box)
        self.setLayout(layout)
        
        # Select first item by default
        if self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(0)
    
    def accept_suggestion(self):
        current_item = self.list_widget.currentItem()
        if current_item:
            self.selected_item_id = current_item.data(Qt.UserRole)
            self.accept()
    
    def create_new_item(self):
        self.create_new = True
        self.accept()

# ---------- Target Time Dialog ----------
class TargetTimeDialog(QDialog):
    def __init__(self, item_name, suggested_target=5.0, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Set Target Time")
        self.setModal(True)
        self.target_hours = suggested_target
        
        layout = QVBoxLayout()
        
        # Message
        msg = QLabel(f"Set target hours for '{item_name}':")
        layout.addWidget(msg)
        
        # Quick buttons
        quick_layout = QHBoxLayout()
        for hours in [5, 10, 15, 20, 30, 50]:
            btn = QPushButton(f"{hours}h")
            btn.clicked.connect(lambda checked, h=hours: self.set_target(h))
            quick_layout.addWidget(btn)
        layout.addLayout(quick_layout)
        
        # Custom input
        custom_layout = QHBoxLayout()
        custom_layout.addWidget(QLabel("Custom:"))
        self.custom_spin = QDoubleSpinBox()
        self.custom_spin.setRange(0, 1000)
        self.custom_spin.setValue(suggested_target)
        self.custom_spin.setSuffix(" hours")
        custom_layout.addWidget(self.custom_spin)
        layout.addLayout(custom_layout)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept_custom)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def set_target(self, hours):
        self.target_hours = hours
        self.accept()
    
    def accept_custom(self):
        self.target_hours = self.custom_spin.value()
        self.accept()

# ---------- Delegates ----------
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

class ComboDelegate(QStyledItemDelegate):
    def __init__(self, choices_func, allow_blank=True, parent=None):
        super().__init__(parent)
        self.choices_func = choices_func
        self.allow_blank = allow_blank
    
    def createEditor(self, parent, option, index):
        cb = QComboBox(parent)
        if self.allow_blank:
            cb.addItem("")
        try:
            choices = self.choices_func()
            if choices:
                cb.addItems(choices)
        except Exception:
            pass
        return cb
    
    def setEditorData(self, editor, index):
        val = str(index.data() or "")
        idx = editor.findText(val)
        editor.setCurrentIndex(max(0, idx))
    
    def setModelData(self, editor, model, index):
        text = editor.currentText()
        model.setData(index, text, Qt.EditRole)

# ---------- Main Window ----------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Learning Tracker")
        self.resize(1400, 800)
        
        # Initialize flags
        self.reloading = False
        self.updating_template = False
        self.current_language_pack = {}
        
        # Initialize database
        try:
            init_db()
            self.config = get_config()
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
        
        # Styling
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
        hdr.setSectionResizeMode(QHeaderView.Interactive)
        hdr.setStretchLastSection(True)
        
        # Set minimum column widths
        column_widths = [50, 100, 80, 80, 200, 80, 100, 70, 150, 120, 100, 120, 70, 80]
        for i, width in enumerate(column_widths):
            hdr.resizeSection(i, width)
        
        # Edit triggers
        self.table.setEditTriggers(
            QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked
        )
        
        # Install delegates
        self.install_delegates()
        
        # Connect signals
        self.table.itemChanged.connect(self.on_cell_changed)

        # --- Toolbar ---
        self.setup_toolbar()

        # --- Enhanced Input Form ---
        self.setup_input_form()

        # --- Main Layout ---
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.toolbar_layout)
        main_layout.addWidget(self.table, 1)  # Give table most space
        main_layout.addWidget(self.input_group)
        
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def setup_toolbar(self):
        self.toolbar_layout = QHBoxLayout()
        
        # Create buttons
        self.add_btn = QPushButton("Add Entry")
        self.save_btn = QPushButton("Save Entry") 
        self.del_btn = QPushButton("Delete Entry")
        self.export_btn = QPushButton("Export CSV")
        
        # Style buttons
        button_style = """
            QPushButton {
                padding: 8px 16px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #f0f9ff;
            }
        """
        for btn in [self.add_btn, self.save_btn, self.del_btn, self.export_btn]:
            btn.setStyleSheet(button_style)
        
        # Connect signals
        self.add_btn.clicked.connect(self.add_entry)
        self.save_btn.clicked.connect(self.save_entry)
        self.del_btn.clicked.connect(self.delete_entry)
        self.export_btn.clicked.connect(self.export_csv)
        
        # Add to layout
        self.toolbar_layout.addWidget(self.add_btn)
        self.toolbar_layout.addWidget(self.save_btn)
        self.toolbar_layout.addWidget(self.del_btn)
        self.toolbar_layout.addStretch()
        self.toolbar_layout.addWidget(self.export_btn)

    def setup_input_form(self):
        # Group box for input form
        self.input_group = QGroupBox("Add New Learning Entry")
        form_layout = QVBoxLayout()
        
        # Create two rows of inputs
        row1_layout = QHBoxLayout()
        row2_layout = QHBoxLayout()
        
        # Input widgets dictionary
        self.inputs = {}
        
        # Row 1: Date, Language, Type, Work Item Name
        # Date
        date_layout = QVBoxLayout()
        date_layout.addWidget(QLabel("Date *"))
        self.inputs['date'] = QDateEdit()
        self.inputs['date'].setCalendarPopup(True)
        self.inputs['date'].setDate(QDate.currentDate())
        self.inputs['date'].setMinimumWidth(120)
        date_layout.addWidget(self.inputs['date'])
        row1_layout.addLayout(date_layout)
        
        # Language
        lang_layout = QVBoxLayout()
        lang_layout.addWidget(QLabel("Language *"))
        self.inputs['language'] = QComboBox()
        self.inputs['language'].setMinimumWidth(120)
        self.load_languages()
        self.inputs['language'].currentTextChanged.connect(self.on_language_changed)
        lang_layout.addWidget(self.inputs['language'])
        row1_layout.addLayout(lang_layout)
        
        # Type
        type_layout = QVBoxLayout()
        type_layout.addWidget(QLabel("Type *"))
        self.inputs['type'] = QComboBox()
        self.inputs['type'].addItems(["", "Exercise", "Project"])
        self.inputs['type'].setMinimumWidth(100)
        type_layout.addWidget(self.inputs['type'])
        row1_layout.addLayout(type_layout)
        
        # Work Item Name (with smart suggestions)
        item_layout = QVBoxLayout()
        item_layout.addWidget(QLabel("Work Item Name *"))
        self.inputs['work_item'] = QComboBox()
        self.inputs['work_item'].setEditable(True)
        self.inputs['work_item'].setMinimumWidth(250)
        self.inputs['work_item'].lineEdit().textChanged.connect(self.on_work_item_changed)
        item_layout.addWidget(self.inputs['work_item'])
        row1_layout.addLayout(item_layout)
        
        # Hours
        hours_layout = QVBoxLayout()
        hours_layout.addWidget(QLabel("Hours *"))
        self.inputs['hours'] = QDoubleSpinBox()
        self.inputs['hours'].setRange(0, 24)
        self.inputs['hours'].setSingleStep(0.25)
        self.inputs['hours'].setDecimals(2)
        self.inputs['hours'].setMinimumWidth(80)
        hours_layout.addWidget(self.inputs['hours'])
        row1_layout.addLayout(hours_layout)
        
        # Row 2: Status, Difficulty, Topic, Notes, Tags
        # Status
        status_layout = QVBoxLayout()
        status_layout.addWidget(QLabel("Status"))
        self.inputs['status'] = QComboBox()
        self.inputs['status'].addItems(["", "Planned", "In Progress", "Completed", "Blocked"])
        self.inputs['status'].setCurrentText("In Progress")
        self.inputs['status'].setMinimumWidth(120)
        status_layout.addWidget(self.inputs['status'])
        row2_layout.addLayout(status_layout)
        
        # Difficulty (auto-filled)
        diff_layout = QVBoxLayout()
        diff_layout.addWidget(QLabel("Difficulty"))
        self.inputs['difficulty'] = QComboBox()
        self.inputs['difficulty'].addItems(["", "Beginner", "Intermediate", "Advanced", "Expert"])
        self.inputs['difficulty'].setMinimumWidth(120)
        diff_layout.addWidget(self.inputs['difficulty'])
        row2_layout.addLayout(diff_layout)
        
        # Topic (auto-filled)
        topic_layout = QVBoxLayout()
        topic_layout.addWidget(QLabel("Topic"))
        self.inputs['topic'] = QComboBox()
        self.inputs['topic'].setEditable(True)
        self.inputs['topic'].setMinimumWidth(120)
        topic_layout.addWidget(self.inputs['topic'])
        row2_layout.addLayout(topic_layout)
        
        # Notes
        notes_layout = QVBoxLayout()
        notes_layout.addWidget(QLabel("Notes"))
        self.inputs['notes'] = QLineEdit()
        self.inputs['notes'].setPlaceholderText("What did you do?")
        self.inputs['notes'].setMinimumWidth(200)
        self.inputs['notes'].textChanged.connect(self.auto_fill_from_text)
        notes_layout.addWidget(self.inputs['notes'])
        row2_layout.addLayout(notes_layout)
        
        # Tags
        tags_layout = QVBoxLayout()
        tags_layout.addWidget(QLabel("Tags"))
        self.inputs['tags'] = QLineEdit()
        self.inputs['tags'].setPlaceholderText("comma, separated, tags")
        self.inputs['tags'].setMinimumWidth(150)
        tags_layout.addWidget(self.inputs['tags'])
        row2_layout.addLayout(tags_layout)
        
        # Add rows to form
        form_layout.addLayout(row1_layout)
        form_layout.addLayout(row2_layout)
        
        # Smart status indicators
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #666; font-style: italic; padding: 4px;")
        form_layout.addWidget(self.status_label)
        
        self.input_group.setLayout(form_layout)

    def install_delegates(self):
        try:
            col_map = {header: i for i, header in enumerate(HEADERS)}
            
            # Date delegate
            if "Date" in col_map:
                self.table.setItemDelegateForColumn(col_map["Date"], DateDelegate(self.table))
            
            # Status delegate
            if "Status" in col_map:
                self.table.setItemDelegateForColumn(
                    col_map["Status"], 
                    ComboDelegate(lambda: ["Planned", "In Progress", "Completed", "Blocked"], parent=self.table)
                )
            
            # Difficulty delegate
            if "Difficulty" in col_map:
                self.table.setItemDelegateForColumn(
                    col_map["Difficulty"], 
                    ComboDelegate(lambda: ["Beginner", "Intermediate", "Advanced", "Expert"], parent=self.table)
                )
            
            # Hours delegate
            if "Hours" in col_map:
                self.table.setItemDelegateForColumn(col_map["Hours"], HoursDelegate(self.table))
                
        except Exception as e:
            print(f"Warning: Failed to install delegates: {e}")

    def load_languages(self):
        """Load languages into the combo box"""
        try:
            languages = get_languages()
            self.inputs['language'].clear()
            self.inputs['language'].addItem("")
            
            for code, name, color in languages:
                self.inputs['language'].addItem(name, code)
                
        except Exception as e:
            print(f"Warning: Failed to load languages: {e}")

    def on_language_changed(self):
        """Handle language selection change"""
        if self.updating_template:
            return
            
        current_data = self.inputs['language'].currentData()
        if current_data:
            try:
                self.current_language_pack = load_language_pack(current_data)
                self.update_topic_suggestions()
                self.update_work_item_suggestions()
            except Exception as e:
                print(f"Warning: Failed to load language pack: {e}")

    def update_topic_suggestions(self):
        """Update topic dropdown based on language pack"""
        topics = list(self.current_language_pack.get('topics', {}).keys())
        
        self.inputs['topic'].clear()
        self.inputs['topic'].addItem("")
        if topics:
            self.inputs['topic'].addItems(topics)

    def update_work_item_suggestions(self):
        """Update work item suggestions based on language and type"""
        language_code = self.inputs['language'].currentData()
        item_type = self.inputs['type'].currentText()
        
        if not language_code or not item_type:
            return
            
        try:
            items = search_items(language_code, item_type, limit=20)
            
            self.inputs['work_item'].clear()
            self.inputs['work_item'].addItem("")
            
            for item in items:
                display_text = f"{item['name']}"
                if item['total_hours'] > 0:
                    display_text += f" ({item['total_hours']:.1f}h logged)"
                
                self.inputs['work_item'].addItem(display_text, item['id'])
                
        except Exception as e:
            print(f"Warning: Failed to update work item suggestions: {e}")

    def on_work_item_changed(self):
        """Handle work item name changes"""
        if self.updating_template:
            return
            
        # If user selected from dropdown, get item details
        current_data = self.inputs['work_item'].currentData()
        if current_data:
            try:
                item = get_item_by_id(current_data)
                if item:
                    self.inputs['difficulty'].setCurrentText(item['default_difficulty'] or "")
                    self.inputs['topic'].setCurrentText(item['default_topic'] or "")
                    self.update_status_display(item)
                    return
            except Exception as e:
                print(f"Warning: Failed to get item details: {e}")
        
        # Auto-fill from text
        self.auto_fill_from_text()

    def auto_fill_from_text(self):
        """Auto-fill difficulty and topic based on text content"""
        if self.updating_template:
            return
            
        try:
            # Combine text from work item name and notes
            text = " ".join([
                self.inputs['work_item'].currentText(),
                self.inputs['notes'].text()
            ]).lower()
            
            if not text.strip():
                return
            
            # Score against language pack
            best_topic = ""
            best_difficulty = ""
            best_score = 0
            
            for topic, topic_info in self.current_language_pack.get('topics', {}).items():
                score = 0
                if topic.lower() in text:
                    score += 10
                    
                if score > best_score:
                    best_score = score
                    best_topic = topic
                    best_difficulty = topic_info.get('default_difficulty', 'Beginner')
            
            # Check skills for better matches
            for skill_name, skill_info in self.current_language_pack.get('skills', {}).items():
                score = 0
                keywords = skill_info.get('keywords', [])
                
                for keyword in keywords:
                    if keyword.lower() in text:
                        score += 5
                
                if skill_name.lower() in text:
                    score += 15
                    
                if score > best_score:
                    best_score = score
                    best_difficulty = skill_info.get('difficulty', best_difficulty)
            
            # Update fields if we found matches
            if best_topic and best_score > 0:
                self.inputs['topic'].setCurrentText(best_topic)
            if best_difficulty and best_score > 0:
                self.inputs['difficulty'].setCurrentText(best_difficulty)
                
        except Exception as e:
            print(f"Warning: Auto-fill failed: {e}")

    def update_status_display(self, item=None):
        """Update the status display with item information"""
        if not item:
            self.status_label.setText("")
            return
            
        try:
            status_parts = []
            
            if item['total_hours'] > 0:
                status_parts.append(f"Logged: {item['total_hours']:.1f}h")
            
            if item['target_hours'] > 0:
                progress = min(100, (item['total_hours'] / item['target_hours']) * 100)
                status_parts.append(f"Progress: {progress:.1f}%")
            
            if item['current_streak_days'] > 0:
                status_parts.append(f"Streak: {item['current_streak_days']} days")
            
            if item['projected_finish_date']:
                try:
                    finish_date = datetime.fromisoformat(item['projected_finish_date']).date()
                    status_parts.append(f"ETA: {finish_date}")
                except:
                    pass
            
            self.status_label.setText(" | ".join(status_parts))
            
        except Exception as e:
            print(f"Warning: Failed to update status display: {e}")

    def clear_form(self):
        """Clear the input form"""
        self.updating_template = True
        try:
            self.inputs['date'].setDate(QDate.currentDate())
            self.inputs['hours'].setValue(0.0)
            self.inputs['notes'].clear()
            self.inputs['tags'].clear()
            self.inputs['status'].setCurrentText("In Progress")
            
            # Clear combo boxes
            for field in ['language', 'type', 'work_item', 'difficulty', 'topic']:
                self.inputs[field].setCurrentIndex(0)
            
            self.status_label.setText("")
        finally:
            self.updating_template = False

    def add_entry(self):
        """Prepare form for new entry"""
        self.clear_form()

    def save_entry(self):
        """Save the current entry"""
        try:
            # Validate required fields
            language_code = self.inputs['language'].currentData()
            item_type = self.inputs['type'].currentText().strip()
            work_item_name = self.inputs['work_item'].currentText().strip()
            hours = self.inputs['hours'].value()
            
            if not language_code:
                QMessageBox.warning(self, "Validation", "Please select a language.")
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
            progress = 0.0
            if is_project and project_name:
                try:
                    target = project_target_hours(project_name) or 0.0
                    logged = project_logged_hours(project_name) or 0.0
                    if target > 0:
                        # Include current form's hours in preview calculation
                        progress_preview = (logged + hours) / target * 100.0
                        progress = min(100.0, progress_preview)  # Cap at 100%
                    else:
                        # Warn if target is missing or 0
                        QMessageBox.warning(self, "Warning", f"No target hours set for project '{project_name}'. Progress will show 0%.")
                        progress = 0.0
                except Exception as e:
                    print(f"Warning: Progress calculation failed: {e}")
                    progress = 0.0

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
                "project_progress_pct": float(f"{progress:.1f}") if is_project else 0.0,  # One decimal place
            }

            # Save to database
            insert_or_update_session(row_data)
            self.reload_table()
            self.clear_form()
            
            # Show success message with progress info for projects
            if is_project and project_name:
                QMessageBox.information(self, "Success", 
                    f"Project row saved successfully!\n"
                    f"Progress: {progress:.1f}% ({logged + hours:.1f}h logged)")
            else:
                QMessageBox.information(self, "Success", "Row saved successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save entry: {e}")

    def delete_entry(self):
        """Delete selected entry"""
        try:
            current_row = self.table.currentRow()
            if current_row < 0:
                QMessageBox.information(self, "Info", "Please select a row to delete.")
                return

            id_item = self.table.item(current_row, 0)
            if not id_item:
                return

            session_id = id_item.text()
            
            # Confirm deletion
            reply = QMessageBox.question(
                self, "Confirm Delete", 
                f"Are you sure you want to delete session {session_id}?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                from app.db import connect, update_item_summaries
                
                # Get item_id before deletion for summary update
                with connect() as con:
                    cur = con.cursor()
                    cur.execute("SELECT item_id FROM sessions WHERE id=?", (session_id,))
                    item_row = cur.fetchone()
                    
                    if item_row:
                        item_id = item_row[0]
                        cur.execute("DELETE FROM sessions WHERE id=?", (session_id,))
                        con.commit()
                        
                        # Update item summaries
                        update_item_summaries(item_id)
                
                self.reload_table()
                QMessageBox.information(self, "Success", "Entry deleted successfully!")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete entry: {e}")

    def export_csv(self):
        """Export data to CSV"""
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Export CSV", "learning_sessions.csv", "CSV Files (*.csv)"
            )
            if not file_path:
                return

            sessions = list_sessions(100000)
            
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(HEADERS)
                
                for session in sessions:
                    # Map session data to headers
                    row = [
                        session[0],  # ID
                        session[1],  # Date
                        session[2],  # Language
                        session[3],  # Type
                        session[4],  # Work Item Name
                        "",          # Target Time (would need separate query)
                        session[5],  # Status
                        session[6],  # Hours
                        session[7],  # Notes
                        session[8],  # Tags
                        session[9],  # Difficulty
                        session[10], # Topic
                        session[11], # Points
                        session[12]  # Progress %
                    ]
                    writer.writerow(row)

            QMessageBox.information(self, "Export", f"Exported {len(sessions)} sessions to {file_path}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export CSV: {e}")

    def reload_table(self):
        """Reload the table with current data"""
        self.reloading = True
        try:
            sessions = list_sessions(1000)
            self.table.setRowCount(0)
            
            for session_data in sessions:
                row_index = self.table.rowCount()
                self.table.insertRow(row_index)
                
                # Map session data to table columns
                display_data = [
                    session_data[0],   # ID
                    session_data[1],   # Date
                    session_data[2],   # Language
                    session_data[3],   # Type
                    session_data[4],   # Work Item Name
                    "",               # Target Time (needs separate query)
                    session_data[5],   # Status
                    f"{float(session_data[6]):.2f}" if session_data[6] else "0.00",  # Hours
                    session_data[7],   # Notes
                    session_data[8],   # Tags
                    session_data[9],   # Difficulty
                    session_data[10],  # Topic
                    f"{float(session_data[11]):.2f}" if session_data[11] else "0.00",  # Points
                    f"{float(session_data[12]):.1f}%" if session_data[12] and float(session_data[12]) > 0 else ""  # Progress
                ]
                
                for col_index, value in enumerate(display_data):
                    item_text = "" if value is None else str(value)
                    item = QTableWidgetItem(item_text)
                    
                    # Make computed columns read-only
                    if col_index in [0, 12, 13]:  # ID, Points, Progress
                        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    
                    self.table.setItem(row_index, col_index, item)
            
            self.table.resizeRowsToContents()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load data: {e}")
        finally:
            self.reloading = False

    def on_cell_changed(self, item):
        """Handle cell changes in the table"""
        if self.reloading:
            return

        try:
            row_idx = item.row()
            col_idx = item.column()
            
            # Get session ID
            id_item = self.table.item(row_idx, 0)
            if not id_item or not id_item.text().strip():
                return

            session_id = int(id_item.text())

            # Collect all row values
            row_values = {}
            for col_idx, key in enumerate(KEYS):
                cell_item = self.table.item(row_idx, col_idx)
                row_values[key] = "" if cell_item is None else cell_item.text()

            # Recompute calculated fields
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

            # Calculate project progress - RECOMPUTE after DB update
            progress_pct = ""
            if row_values["type"] == "Project" and row_values["project_name"]:
                try:
                    # Update database FIRST so logged hours includes this change
                    row_values["id"] = session_id
                    row_values["hours_spent"] = hours
                    insert_or_update_session(row_values)
                    
                    # Now recompute progress with updated data
                    target = project_target_hours(row_values["project_name"]) or 0.0
                    logged = project_logged_hours(row_values["project_name"]) or 0.0
                    if target > 0:
                        progress_val = min(100.0, (logged / target) * 100.0)  # Cap at 100%
                        progress_pct = f"{progress_val:.1f}"  # One decimal place
                    else:
                        progress_pct = "0.0"
                except Exception as e:
                    print(f"Warning: Progress recalculation failed: {e}")
                    progress_pct = "0.0"
            else:
                # Exercise rows or missing project name
                progress_pct = ""
                # Still update database for non-project rows
                row_values["id"] = session_id
                row_values["hours_spent"] = hours
                insert_or_update_session(row_values)

            row_values["project_progress_pct"] = progress_pct

            # Update UI with recomputed values
            self.reloading = True
            try:
                points_col = KEYS.index("points_awarded")
                progress_col = KEYS.index("project_progress_pct")
                self.table.item(row_idx, points_col).setText(row_values["points_awarded"])
                self.table.item(row_idx, progress_col).setText(row_values["project_progress_pct"])
                
                # Make progress column read-only
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
    app.setApplicationName("Smart Learning Tracker")
    app.setApplicationVersion("2.0")
    
    try:
        window = MainWindow()
        window.show()
        return app.exec()
    except Exception as e:
        QMessageBox.critical(None, "Startup Error", f"Failed to start application: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
