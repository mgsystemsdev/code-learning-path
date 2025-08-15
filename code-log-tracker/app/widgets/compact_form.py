# app/widgets/compact_form_fixed.py
"""
Ultra-compact form with no internal scrollbars and proper QComboBox implementation.
Follows exact specifications: clean, compact, scrollbar-free.
"""

from __future__ import annotations
from typing import Dict, Any, Optional, List, Tuple
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QGridLayout,
    QLabel, QPushButton, QComboBox, QDoubleSpinBox, 
    QLineEdit, QDateEdit, QSizePolicy, QFrame,
    QPlainTextEdit, QHeaderView
)
from PySide6.QtCore import Qt, QDate, Signal, QTimer
from PySide6.QtGui import QFont

from app.config.ui_config import UIConfig


class CompactForm(QWidget):
    """
    Ultra-compact form with no internal scrollbars.
    Two rows: essentials + details, all properly labeled.
    """
    
    dataChanged = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.inputs: Dict[str, Any] = {}
        self.notes_text: str = ""
        self.setup_form()
        
    def setup_form(self):
        """Create the ultra-compact two-row form with no scrollbars."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(6)
        
        # Form title
        title = QLabel("📝 Learning Session Entry")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        title.setStyleSheet("color: #60a5fa; margin-bottom: 6px;")
        main_layout.addWidget(title)
        
        # Create form container - FIXED HEIGHT prevents scrolling
        form_container = QFrame()
        form_container.setFixedHeight(120)  # Locked height
        form_container.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border: 1px solid #475569;
                border-radius: 8px;
                padding: 8px;
            }
        """)
        
        form_layout = QVBoxLayout(form_container)
        form_layout.setContentsMargins(10, 10, 10, 10)
        form_layout.setSpacing(8)
        
        # Row 1: Essentials - Date | Language | Type | Work Item Name | Status
        row1 = self._create_row1()
        form_layout.addLayout(row1)
        
        # Row 2: Details - Hours | Target Time | Difficulty | Topic Area | Tags | Notes
        row2 = self._create_row2()
        form_layout.addLayout(row2)
        
        main_layout.addWidget(form_container)
        
        # Status display (compact, hidden by default)
        self.status_label = QLabel("")
        self.status_label.setFixedHeight(24)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #10b981;
                background-color: #064e3b;
                padding: 4px 8px;
                border-radius: 4px;
                border: 1px solid #065f46;
                font-size: 12px;
            }
        """)
        self.status_label.hide()
        main_layout.addWidget(self.status_label)
        
    def _create_row1(self) -> QHBoxLayout:
        """Row 1: Date | Language | Type | Work Item Name | Status"""
        row = QHBoxLayout()
        row.setSpacing(8)
        
        # Date
        date_container = self._create_labeled_field("📅 Date *")
        self.inputs["date"] = QDateEdit()
        self.inputs["date"].setCalendarPopup(True)
        self.inputs["date"].setDate(QDate.currentDate())
        self.inputs["date"].setFixedWidth(110)
        self._apply_input_style(self.inputs["date"])
        self.inputs["date"].dateChanged.connect(self.dataChanged)
        date_container.addWidget(self.inputs["date"])
        row.addLayout(date_container)
        
        # Language
        lang_container = self._create_labeled_field("💻 Language *")
        self.inputs["language"] = self._make_combo([], editable=False)
        self.inputs["language"].setFixedWidth(120)
        self.inputs["language"].currentTextChanged.connect(self.dataChanged)
        lang_container.addWidget(self.inputs["language"])
        row.addLayout(lang_container)
        
        # Type
        type_container = self._create_labeled_field("📂 Type *")
        self.inputs["type"] = self._make_combo(["", "Exercise", "Project"], editable=False)
        self.inputs["type"].setFixedWidth(100)
        self.inputs["type"].currentTextChanged.connect(self.dataChanged)
        self.inputs["type"].currentTextChanged.connect(self._on_type_changed)
        type_container.addWidget(self.inputs["type"])
        row.addLayout(type_container)
        
        # Work Item Name (expandable, searchable)
        item_container = self._create_labeled_field("📝 Work Item Name *")
        self.inputs["work_item"] = self._make_combo([], editable=True)
        self.inputs["work_item"].lineEdit().setPlaceholderText("Search or enter new...")
        self.inputs["work_item"].lineEdit().textChanged.connect(self.dataChanged)
        item_container.addWidget(self.inputs["work_item"])
        row.addLayout(item_container, 2)  # Give more space
        
        # Status
        status_container = self._create_labeled_field("📊 Status")
        self.inputs["status"] = self._make_combo(["", "Planned", "In Progress", "Completed", "Blocked"])
        self.inputs["status"].setCurrentText("In Progress")
        self.inputs["status"].setFixedWidth(120)
        self.inputs["status"].currentTextChanged.connect(self.dataChanged)
        status_container.addWidget(self.inputs["status"])
        row.addLayout(status_container)
        
        return row
        
    def _create_row2(self) -> QHBoxLayout:
        """Row 2: Hours | Target Time | Difficulty | Topic Area | Tags | Notes"""
        row = QHBoxLayout()
        row.setSpacing(8)
        
        # Hours
        hours_container = self._create_labeled_field("🕒 Hours *")
        self.inputs["hours"] = self._make_spin(0, 24, 0.25)
        self.inputs["hours"].setSuffix(" h")
        self.inputs["hours"].setFixedWidth(80)
        self.inputs["hours"].valueChanged.connect(self.dataChanged)
        hours_container.addWidget(self.inputs["hours"])
        row.addLayout(hours_container)
        
        # Target Time
        target_container = self._create_labeled_field("⏱️ Target")
        self.inputs["target_time"] = self._make_spin(0, 200, 0.5)
        self.inputs["target_time"].setSuffix(" h")
        self.inputs["target_time"].setFixedWidth(80)
        self.inputs["target_time"].valueChanged.connect(self.dataChanged)
        target_container.addWidget(self.inputs["target_time"])
        row.addLayout(target_container)
        
        # Difficulty
        diff_container = self._create_labeled_field("🎖️ Difficulty")
        self.inputs["difficulty"] = self._make_combo(["", "Beginner", "Intermediate", "Advanced", "Expert"])
        self.inputs["difficulty"].setFixedWidth(110)
        self.inputs["difficulty"].currentTextChanged.connect(self.dataChanged)
        diff_container.addWidget(self.inputs["difficulty"])
        row.addLayout(diff_container)
        
        # Topic Area
        topic_container = self._create_labeled_field("🎯 Topic")
        self.inputs["topic"] = self._make_combo([], editable=True)
        self.inputs["topic"].lineEdit().setPlaceholderText("Enter topic...")
        self.inputs["topic"].setFixedWidth(120)
        self.inputs["topic"].lineEdit().textChanged.connect(self.dataChanged)
        topic_container.addWidget(self.inputs["topic"])
        row.addLayout(topic_container)
        
        # Tags
        tags_container = self._create_labeled_field("🏷️ Tags")
        self.inputs["tags"] = QLineEdit()
        self.inputs["tags"].setPlaceholderText("learning, practice...")
        self.inputs["tags"].setFixedWidth(140)
        self._apply_input_style(self.inputs["tags"])
        self.inputs["tags"].textChanged.connect(self.dataChanged)
        tags_container.addWidget(self.inputs["tags"])
        row.addLayout(tags_container)
        
        # Notes (compact, no scrollbars)
        notes_container = self._create_labeled_field("📋 Notes")
        self.inputs["notes"] = QPlainTextEdit()
        self.inputs["notes"].setFixedHeight(36)  # ~2 lines, no scroll
        self.inputs["notes"].setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.inputs["notes"].setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.inputs["notes"].setPlaceholderText("Quick notes...")
        self._apply_input_style(self.inputs["notes"])
        self.inputs["notes"].textChanged.connect(self.dataChanged)
        notes_container.addWidget(self.inputs["notes"])
        row.addLayout(notes_container, 2)  # Give more space
        
        return row
    
    def _create_labeled_field(self, label_text: str) -> QVBoxLayout:
        """Create a compact labeled field container."""
        container = QVBoxLayout()
        container.setSpacing(2)
        container.setContentsMargins(0, 0, 0, 0)
        
        # High contrast label
        label = QLabel(label_text)
        label.setStyleSheet("""
            QLabel {
                font-weight: 600;
                color: #f1f5f9;
                font-size: 11px;
                margin-bottom: 1px;
            }
        """)
        container.addWidget(label)
        
        return container
    
    def _make_combo(self, items: List[str], editable: bool = False) -> QComboBox:
        """Create a properly configured QComboBox with no internal scrollbars."""
        cb = QComboBox()
        cb.addItems(items)
        cb.setEditable(editable)
        cb.setInsertPolicy(QComboBox.NoInsert)
        cb.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Apply styling and ensure no scrollbars
        self._apply_combo_style(cb)
        
        # Disable scrollbars in dropdown if possible
        if cb.view():
            cb.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # Minimal scrolling
        
        return cb
    
    def _make_spin(self, minv: float, maxv: float, step: float) -> QDoubleSpinBox:
        """Create a properly configured QDoubleSpinBox with no scrollbars."""
        sp = QDoubleSpinBox()
        sp.setRange(minv, maxv)
        sp.setSingleStep(step)
        sp.setDecimals(2)
        sp.setButtonSymbols(QDoubleSpinBox.PlusMinus)
        sp.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        self._apply_input_style(sp)
        return sp
    
    def _apply_combo_style(self, combo: QComboBox):
        """Apply consistent styling to combo boxes."""
        combo.setStyleSheet("""
            QComboBox {
                background-color: #334155;
                border: 2px solid #475569;
                border-radius: 6px;
                padding: 4px 8px;
                color: #e2e8f0;
                font-weight: 500;
                min-height: 20px;
            }
            QComboBox:focus {
                border-color: #60a5fa;
                background-color: #475569;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
                background-color: #475569;
            }
            QComboBox QAbstractItemView {
                background-color: #334155;
                border: 2px solid #60a5fa;
                selection-background-color: #60a5fa;
                selection-color: white;
                outline: none;
            }
        """)
    
    def _apply_input_style(self, widget):
        """Apply consistent styling to input widgets."""
        widget.setStyleSheet("""
            QLineEdit, QDoubleSpinBox, QDateEdit, QPlainTextEdit {
                background-color: #334155;
                border: 2px solid #475569;
                border-radius: 6px;
                padding: 4px 8px;
                color: #e2e8f0;
                font-weight: 500;
                min-height: 20px;
            }
            QLineEdit:focus, QDoubleSpinBox:focus, QDateEdit:focus, QPlainTextEdit:focus {
                border-color: #60a5fa;
                background-color: #475569;
            }
        """)
    
    def _on_type_changed(self):
        """Handle type selection - show/hide target time for exercises."""
        type_value = self.inputs["type"].currentText()
        
        if type_value == "Exercise":
            # Exercises usually don't need target times
            self.inputs["target_time"].setValue(0.0)
            self.inputs["target_time"].setEnabled(False)
            self.inputs["target_time"].setStyleSheet(self.inputs["target_time"].styleSheet() + "color: #6b7280;")
        else:
            # Projects need target times
            self.inputs["target_time"].setEnabled(True)
            self._apply_input_style(self.inputs["target_time"])
    
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
            data["tags"] = self.inputs["tags"].text()
        if "notes" in self.inputs:
            data["notes"] = self.inputs["notes"].toPlainText()
        
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
            self.inputs["tags"].clear()
        if "notes" in self.inputs:
            self.inputs["notes"].clear()
            
        self.status_label.hide()
    
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
            self.inputs["tags"].setText(data["tags"] or "")
            
        if "notes" in data and "notes" in self.inputs:
            self.inputs["notes"].setPlainText(data["notes"] or "")
    
    def load_languages(self, languages: List[tuple]):
        """Load available languages into combo."""
        combo = self.inputs.get("language")
        if combo:
            combo.clear()
            combo.addItem("")  # Empty option
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
            return False, f"Required: {', '.join(missing)}"
            
        return True, ""
    
    def update_status_display(self, message: str):
        """Update status label with auto-hide."""
        if message:
            self.status_label.setText(message)
            self.status_label.show()
            # Auto-hide after 3 seconds
            QTimer.singleShot(3000, self.status_label.hide)
        else:
            self.status_label.hide()
            
    def focus_first_field(self):
        """Focus the first input field."""
        if "date" in self.inputs:
            self.inputs["date"].setFocus()
