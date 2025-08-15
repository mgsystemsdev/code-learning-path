# app/widgets/compact_form.py
"""
Compact two-row form layout for dashboard interface.
Notes field becomes a popup modal to save space.
"""

from __future__ import annotations
from typing import Dict, Any, Optional, List, Tuple
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QGridLayout,
    QLabel, QPushButton, QComboBox, QDoubleSpinBox, 
    QLineEdit, QDateEdit, QDialog, QTextEdit,
    QDialogButtonBox, QSizePolicy, QFrame
)
from PySide6.QtCore import Qt, QDate, Signal
from PySide6.QtGui import QFont

from app.config.ui_config import UIConfig


class NotesDialog(QDialog):
    """Modal dialog for editing notes."""
    
    def __init__(self, initial_text: str = "", parent=None):
        super().__init__(parent)
        self.setWindowTitle("📋 Session Notes")
        self.setModal(True)
        self.resize(500, 300)
        
        layout = QVBoxLayout(self)
        
        # Instructions
        instructions = QLabel("Describe what you worked on, challenges faced, key insights...")
        instructions.setStyleSheet("color: #cbd5e1; font-style: italic; margin-bottom: 8px;")
        layout.addWidget(instructions)
        
        # Text area
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(initial_text)
        self.text_edit.setStyleSheet("""
            QTextEdit {
                border: 2px solid #475569;
                border-radius: 8px;
                padding: 12px;
                background-color: #334155;
                color: #f1f5f9;
                font-size: 13px;
                font-weight: 500;
                line-height: 1.5;
            }
            QTextEdit:focus {
                border-color: #60a5fa;
                background-color: #475569;
            }
        """)
        layout.addWidget(self.text_edit)
        
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        # Apply dark theme to dialog
        self.setStyleSheet(UIConfig.MAIN_STYLE)
        
    def get_text(self) -> str:
        """Get the edited text."""
        return self.text_edit.toPlainText()


class CompactForm(QWidget):
    """
    Compact two-row form layout for maximum space efficiency.
    All essential fields in just two horizontal rows.
    """
    
    dataChanged = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.inputs: Dict[str, Any] = {}
        self.notes_text: str = ""
        self.setup_form()
        
    def setup_form(self):
        """Create the compact two-row form."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)
        
        # Create form frame
        form_frame = QFrame()
        form_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        form_frame.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border: 1px solid #475569;
                border-radius: 8px;
                padding: 12px;
            }
        """)
        
        form_layout = QVBoxLayout(form_frame)
        form_layout.setContentsMargins(12, 12, 12, 12)
        form_layout.setSpacing(12)
        
        # Row 1: Date, Language, Type, Work Item Name, Status
        row1 = self._create_row1()
        form_layout.addLayout(row1)
        
        # Row 2: Hours, Target Time, Difficulty, Topic Area, Tags, Progress, Notes Button
        row2 = self._create_row2()
        form_layout.addLayout(row2)
        
        main_layout.addWidget(form_frame)
        
        # Status display
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #60a5fa;
                font-weight: 500;
                padding: 6px 12px;
                background-color: #334155;
                border: 1px solid #475569;
                border-radius: 6px;
                margin: 4px 0;
            }
        """)
        main_layout.addWidget(self.status_label)
        
    def _create_row1(self) -> QHBoxLayout:
        """Create first row: Date, Language, Type, Work Item Name, Status."""
        row = QHBoxLayout()
        row.setSpacing(12)
        
        # Date
        date_container = self._create_field_container("📅 Date *")
        self.inputs["date"] = QDateEdit()
        self.inputs["date"].setCalendarPopup(True)
        self.inputs["date"].setDate(QDate.currentDate())
        self.inputs["date"].setFixedWidth(120)
        self.inputs["date"].dateChanged.connect(self.dataChanged)
        date_container.addWidget(self.inputs["date"])
        row.addLayout(date_container)
        
        # Language
        lang_container = self._create_field_container("💻 Language *")
        self.inputs["language"] = QComboBox()
        self.inputs["language"].setFixedWidth(130)
        self.inputs["language"].currentTextChanged.connect(self.dataChanged)
        self.inputs["language"].currentTextChanged.connect(self._on_language_changed)
        lang_container.addWidget(self.inputs["language"])
        row.addLayout(lang_container)
        
        # Type
        type_container = self._create_field_container("📂 Type *")
        self.inputs["type"] = QComboBox()
        self.inputs["type"].addItems(["", "Exercise", "Project"])
        self.inputs["type"].setFixedWidth(110)
        self.inputs["type"].currentTextChanged.connect(self.dataChanged)
        self.inputs["type"].currentTextChanged.connect(self._on_type_changed)
        type_container.addWidget(self.inputs["type"])
        row.addLayout(type_container)
        
        # Work Item Name (expandable)
        item_container = self._create_field_container("📝 Work Item Name *")
        self.inputs["work_item"] = QComboBox()
        self.inputs["work_item"].setEditable(True)
        self.inputs["work_item"].lineEdit().setPlaceholderText("Search or enter new item...")
        self.inputs["work_item"].lineEdit().textChanged.connect(self.dataChanged)
        self.inputs["work_item"].lineEdit().textChanged.connect(self._on_work_item_changed)
        item_container.addWidget(self.inputs["work_item"])
        row.addLayout(item_container, 2)  # Give more space
        
        # Status
        status_container = self._create_field_container("📊 Status")
        self.inputs["status"] = QComboBox()
        self.inputs["status"].addItems(["", "Planned", "In Progress", "Completed", "Blocked"])
        self.inputs["status"].setCurrentText("In Progress")
        self.inputs["status"].setFixedWidth(130)
        self.inputs["status"].currentTextChanged.connect(self.dataChanged)
        status_container.addWidget(self.inputs["status"])
        row.addLayout(status_container)
        
        return row
        
    def _create_row2(self) -> QHBoxLayout:
        """Create second row: Hours, Target Time, Difficulty, Topic, Tags, Progress, Notes."""
        row = QHBoxLayout()
        row.setSpacing(12)
        
        # Hours
        hours_container = self._create_field_container("🕒 Hours *")
        self.inputs["hours"] = QDoubleSpinBox()
        self.inputs["hours"].setRange(0, 24)
        self.inputs["hours"].setSingleStep(0.25)
        self.inputs["hours"].setDecimals(2)
        self.inputs["hours"].setSuffix(" h")
        self.inputs["hours"].setFixedWidth(90)
        self.inputs["hours"].valueChanged.connect(self.dataChanged)
        self.inputs["hours"].valueChanged.connect(self._on_hours_changed)
        hours_container.addWidget(self.inputs["hours"])
        row.addLayout(hours_container)
        
        # Target Time
        target_container = self._create_field_container("⏱️ Target")
        self.inputs["target_time"] = QDoubleSpinBox()
        self.inputs["target_time"].setRange(0, 1000)
        self.inputs["target_time"].setSingleStep(1.0)
        self.inputs["target_time"].setDecimals(1)
        self.inputs["target_time"].setSuffix(" h")
        self.inputs["target_time"].setFixedWidth(90)
        self.inputs["target_time"].valueChanged.connect(self.dataChanged)
        target_container.addWidget(self.inputs["target_time"])
        row.addLayout(target_container)
        
        # Difficulty
        diff_container = self._create_field_container("🎖️ Difficulty")
        self.inputs["difficulty"] = QComboBox()
        self.inputs["difficulty"].addItems(["", "Beginner", "Intermediate", "Advanced", "Expert"])
        self.inputs["difficulty"].setFixedWidth(130)
        self.inputs["difficulty"].currentTextChanged.connect(self.dataChanged)
        diff_container.addWidget(self.inputs["difficulty"])
        row.addLayout(diff_container)
        
        # Topic Area
        topic_container = self._create_field_container("🎯 Topic")
        self.inputs["topic"] = QComboBox()
        self.inputs["topic"].setEditable(True)
        self.inputs["topic"].lineEdit().setPlaceholderText("Enter topic...")
        self.inputs["topic"].setFixedWidth(140)
        self.inputs["topic"].lineEdit().textChanged.connect(self.dataChanged)
        topic_container.addWidget(self.inputs["topic"])
        row.addLayout(topic_container)
        
        # Tags (expandable)
        tags_container = self._create_field_container("🏷️ Tags")
        self.inputs["tags"] = QComboBox()
        self.inputs["tags"].setEditable(True)
        self.inputs["tags"].lineEdit().setPlaceholderText("learning, practice, review...")
        self.inputs["tags"].lineEdit().textChanged.connect(self.dataChanged)
        tags_container.addWidget(self.inputs["tags"])
        row.addLayout(tags_container, 1)  # Give some extra space
        
        # Progress (read-only)
        progress_container = self._create_field_container("📈 Progress")
        self.inputs["progress"] = QLineEdit()
        self.inputs["progress"].setReadOnly(True)
        self.inputs["progress"].setFixedWidth(80)
        self.inputs["progress"].setStyleSheet("QLineEdit { background-color: #1e293b; color: #60a5fa; }")
        progress_container.addWidget(self.inputs["progress"])
        row.addLayout(progress_container)
        
        # Notes button
        notes_container = self._create_field_container("📋 Notes")
        self.notes_btn = QPushButton("Edit Notes")
        self.notes_btn.setFixedWidth(100)
        self.notes_btn.clicked.connect(self._edit_notes)
        notes_container.addWidget(self.notes_btn)
        row.addLayout(notes_container)
        
        return row
    
    def _create_field_container(self, label_text: str) -> QVBoxLayout:
        """Create a labeled field container."""
        container = QVBoxLayout()
        container.setSpacing(4)
        container.setContentsMargins(0, 0, 0, 0)
        
        label = QLabel(label_text)
        label.setStyleSheet("""
            QLabel {
                font-weight: 600;
                color: #e2e8f0;
                font-size: 12px;
                margin-bottom: 2px;
            }
        """)
        container.addWidget(label)
        
        return container
    
    def _edit_notes(self):
        """Open notes editing dialog."""
        dialog = NotesDialog(self.notes_text, self)
        if dialog.exec() == QDialog.Accepted:
            self.notes_text = dialog.get_text()
            # Update button text to show if notes exist
            if self.notes_text.strip():
                self.notes_btn.setText(f"Notes ({len(self.notes_text.strip())})")
                self.notes_btn.setStyleSheet("QPushButton { background-color: #059669; }")
            else:
                self.notes_btn.setText("Edit Notes")
                self.notes_btn.setStyleSheet("")
            self.dataChanged.emit()
    
    def _on_language_changed(self):
        """Handle language selection - filter topics and suggestions."""
        language = self.inputs["language"].currentText()
        # Placeholder for smart filtering logic
        pass
    
    def _on_type_changed(self):
        """Handle type selection - adjust UI behavior."""
        type_value = self.inputs["type"].currentText()
        
        if type_value == "Exercise":
            # Exercises usually don't have target times
            self.inputs["target_time"].setValue(0.0)
            self.inputs["target_time"].setEnabled(False)
        elif type_value == "Project":
            # Projects should have target times
            self.inputs["target_time"].setEnabled(True)
        else:
            # Default
            self.inputs["target_time"].setEnabled(True)
    
    def _on_work_item_changed(self):
        """Handle work item changes - auto-fill related fields."""
        # Placeholder for auto-fill logic based on existing items
        pass
    
    def _on_hours_changed(self):
        """Handle hours change - update progress calculation."""
        # Placeholder for progress calculation
        pass
    
    def get_form_data(self) -> Dict[str, Any]:
        """Get current form data."""
        data = {}
        
        if "date" in self.inputs:
            data["date"] = self.inputs["date"].date().toString("yyyy-MM-dd")
        if "language" in self.inputs:
            data["language"] = self.inputs["language"].currentText()
            data["language_code"] = self.inputs["language"].currentData()
        if "type" in self.inputs:
            data["type"] = self.inputs["type"].currentText()
        if "work_item" in self.inputs:
            data["canonical_name"] = self.inputs["work_item"].currentText()
        if "status" in self.inputs:
            data["status"] = self.inputs["status"].currentText()
        if "hours" in self.inputs:
            data["hours_spent"] = self.inputs["hours"].value()
        if "target_time" in self.inputs:
            data["target_hours"] = self.inputs["target_time"].value()
        if "difficulty" in self.inputs:
            data["difficulty"] = self.inputs["difficulty"].currentText()
        if "topic" in self.inputs:
            data["topic"] = self.inputs["topic"].currentText()
        if "tags" in self.inputs:
            data["tags"] = self.inputs["tags"].currentText()
        
        # Add notes
        data["notes"] = self.notes_text
        
        return data
    
    def clear_form(self):
        """Clear all form inputs."""
        if "date" in self.inputs:
            self.inputs["date"].setDate(QDate.currentDate())
        if "language" in self.inputs:
            self.inputs["language"].setCurrentIndex(0)
        if "type" in self.inputs:
            self.inputs["type"].setCurrentIndex(0)
        if "work_item" in self.inputs:
            self.inputs["work_item"].clearEditText()
        if "status" in self.inputs:
            self.inputs["status"].setCurrentText("In Progress")
        if "hours" in self.inputs:
            self.inputs["hours"].setValue(0.0)
        if "target_time" in self.inputs:
            self.inputs["target_time"].setValue(0.0)
        if "difficulty" in self.inputs:
            self.inputs["difficulty"].setCurrentIndex(0)
        if "topic" in self.inputs:
            self.inputs["topic"].clearEditText()
        if "tags" in self.inputs:
            self.inputs["tags"].clearEditText()
        if "progress" in self.inputs:
            self.inputs["progress"].setText("0.0%")
            
        self.notes_text = ""
        self.notes_btn.setText("Edit Notes")
        self.notes_btn.setStyleSheet("")
    
    def set_form_data(self, data: Dict[str, Any]):
        """Populate form with data for editing."""
        if "date" in data and "date" in self.inputs:
            date_str = data["date"]
            if date_str:
                date = QDate.fromString(date_str, "yyyy-MM-dd")
                self.inputs["date"].setDate(date)
                
        if "language_code" in data and "language" in self.inputs:
            combo = self.inputs["language"]
            for i in range(combo.count()):
                if combo.itemData(i) == data["language_code"]:
                    combo.setCurrentIndex(i)
                    break
                    
        if "type" in data and "type" in self.inputs:
            self.inputs["type"].setCurrentText(data["type"] or "")
            
        if "canonical_name" in data and "work_item" in self.inputs:
            self.inputs["work_item"].setCurrentText(data["canonical_name"] or "")
            
        if "status" in data and "status" in self.inputs:
            self.inputs["status"].setCurrentText(data["status"] or "In Progress")
            
        if "hours_spent" in data and "hours" in self.inputs:
            self.inputs["hours"].setValue(float(data["hours_spent"] or 0))
            
        if "target_hours" in data and "target_time" in self.inputs:
            self.inputs["target_time"].setValue(float(data["target_hours"] or 0))
            
        if "difficulty" in data and "difficulty" in self.inputs:
            self.inputs["difficulty"].setCurrentText(data["difficulty"] or "")
            
        if "topic" in data and "topic" in self.inputs:
            self.inputs["topic"].setCurrentText(data["topic"] or "")
            
        if "tags" in data and "tags" in self.inputs:
            self.inputs["tags"].setCurrentText(data["tags"] or "")
            
        if "progress_pct" in data and "progress" in self.inputs:
            progress = float(data["progress_pct"] or 0)
            self.inputs["progress"].setText(f"{progress:.1f}%")
        
        # Handle notes
        self.notes_text = data.get("notes", "")
        if self.notes_text.strip():
            self.notes_btn.setText(f"Notes ({len(self.notes_text.strip())})")
            self.notes_btn.setStyleSheet("QPushButton { background-color: #059669; }")
        else:
            self.notes_btn.setText("Edit Notes")
            self.notes_btn.setStyleSheet("")
    
    def load_languages(self, languages: List[tuple]):
        """Load available languages."""
        combo = self.inputs.get("language")
        if combo:
            combo.clear()
            combo.addItem("")
            for code, name, _color in languages:
                combo.addItem(name, code)
    
    def validate_required_fields(self) -> Tuple[bool, str]:
        """Validate required fields."""
        form_data = self.get_form_data()
        
        required_fields = {
            "date": "Date",
            "language_code": "Language",
            "type": "Type",
            "canonical_name": "Work Item Name",
            "hours_spent": "Hours"
        }
        
        missing = []
        for field, display_name in required_fields.items():
            if not form_data.get(field):
                missing.append(display_name)
        
        if missing:
            return False, f"Please fill in required fields: {', '.join(missing)}"
            
        return True, ""
    
    def update_status_display(self, message: str):
        """Update status label."""
        self.status_label.setText(message)
        
    def focus_first_field(self):
        """Focus the first input field."""
        if "date" in self.inputs:
            self.inputs["date"].setFocus()
