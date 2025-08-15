# app/widgets/fixed_form.py
"""
Fixed (non-scrollable) form with exact field structure matching table requirements.
"""

from __future__ import annotations
from typing import Dict, Any, Optional, List
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
    QGroupBox, QLabel, QPushButton, QComboBox, 
    QDoubleSpinBox, QLineEdit, QDateEdit, QFrame,
    QTextEdit, QSizePolicy
)
from PySide6.QtCore import Qt, QDate, Signal
from app.config.ui_config import UIConfig


class FixedForm(QWidget):
    """Fixed form layout matching exact table field requirements."""
    
    dataChanged = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.inputs: Dict[str, Any] = {}
        self.setup_form()
        
    def setup_form(self):
        """Create fixed form layout with exact field requirements."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(12)
        
        # Essential information section (compact)
        essential_section = self._create_essential_section()
        main_layout.addWidget(essential_section)
        
        # Details section (compact)
        details_section = self._create_details_section()
        main_layout.addWidget(details_section)
        
        # Notes section (fixed height)
        notes_section = self._create_notes_section()
        main_layout.addWidget(notes_section)
        
        # Status display (compact)
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #60a5fa;
                font-style: italic;
                font-weight: 500;
                padding: 8px;
                background-color: #334155;
                border: 1px solid #475569;
                border-radius: 6px;
                max-height: 35px;
            }
        """)
        main_layout.addWidget(self.status_label)
        
        # No stretch - keep fixed height
        
    def _create_essential_section(self) -> QGroupBox:
        """Create compact essential information section."""
        group = QGroupBox("🎯 Essential Information")
        group.setMaximumHeight(140)
        layout = QGridLayout(group)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 24, 16, 12)
        
        # Row 1: Date, Type, Hours, Status (4 columns)
        self._add_compact_field(layout, "📅 Date *", self._create_date_input(), 0, 0)
        self._add_compact_field(layout, "📂 Type *", self._create_type_input(), 0, 1)
        self._add_compact_field(layout, "🕒 Hours *", self._create_hours_input(), 0, 2)
        self._add_compact_field(layout, "📊 Status", self._create_status_input(), 0, 3)
        
        # Row 2: Language, Work Item Name (spans 2 cols), Target Time
        self._add_compact_field(layout, "💻 Language *", self._create_language_input(), 1, 0)
        self._add_compact_field(layout, "📝 Work Item *", self._create_work_item_input(), 1, 1, 1, 2)
        self._add_compact_field(layout, "⏱️ Target", self._create_target_time_input(), 1, 3)
        
        return group
        
    def _create_details_section(self) -> QGroupBox:
        """Create compact details section."""
        group = QGroupBox("🔧 Learning Details")
        group.setMaximumHeight(100)
        layout = QGridLayout(group)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 24, 16, 12)
        
        # Single row: Difficulty, Topic, Tags (3 columns)
        self._add_compact_field(layout, "🎖️ Difficulty", self._create_difficulty_input(), 0, 0)
        self._add_compact_field(layout, "🎯 Topic", self._create_topic_input(), 0, 1)
        self._add_compact_field(layout, "🏷️ Tags", self._create_tags_input(), 0, 2)
        
        return group
        
    def _create_notes_section(self) -> QGroupBox:
        """Create fixed-height notes section."""
        group = QGroupBox("📋 Session Notes")
        group.setMaximumHeight(120)
        layout = QVBoxLayout(group)
        layout.setContentsMargins(16, 24, 16, 12)
        layout.setSpacing(8)
        
        # Notes field with fixed height
        self.inputs["notes"] = QTextEdit()
        self.inputs["notes"].setMaximumHeight(70)
        self.inputs["notes"].setMinimumHeight(70)
        self.inputs["notes"].setPlaceholderText("What did you work on? Key insights, challenges, progress...")
        self.inputs["notes"].setStyleSheet("""
            QTextEdit {
                border: 2px solid #475569;
                border-radius: 6px;
                padding: 10px;
                background-color: #334155;
                color: #f1f5f9;
                font-size: 13px;
                font-weight: 500;
                line-height: 1.4;
            }
            QTextEdit:focus {
                border-color: #60a5fa;
                background-color: #475569;
                color: #ffffff;
            }
        """)
        self.inputs["notes"].textChanged.connect(self.dataChanged)
        layout.addWidget(self.inputs["notes"])
        
        return group
    
    def _add_compact_field(self, layout: QGridLayout, label_text: str, 
                          widget: QWidget, row: int, col: int, 
                          row_span: int = 1, col_span: int = 1):
        """Add a compact labeled field to the grid layout."""
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(4)
        
        # Compact label with better readability
        label = QLabel(label_text)
        label.setStyleSheet("""
            QLabel {
                font-weight: 600;
                color: #e2e8f0;
                font-size: 13px;
                padding: 2px 0;
                background: transparent;
            }
        """)
        container_layout.addWidget(label)
        container_layout.addWidget(widget)
        
        layout.addWidget(container, row, col, row_span, col_span)
    
    def _create_date_input(self) -> QDateEdit:
        """Create date input field."""
        date_edit = QDateEdit()
        date_edit.setCalendarPopup(True)
        date_edit.setDate(QDate.currentDate())
        date_edit.setMinimumWidth(110)
        date_edit.setMaximumHeight(35)
        date_edit.dateChanged.connect(self.dataChanged)
        self.inputs["date"] = date_edit
        return date_edit
    
    def _create_type_input(self) -> QComboBox:
        """Create type input field."""
        combo = QComboBox()
        combo.addItems(["", "Exercise", "Project"])
        combo.setMinimumWidth(100)
        combo.setMaximumHeight(35)
        combo.currentTextChanged.connect(self.dataChanged)
        combo.currentTextChanged.connect(self._on_type_changed)
        self.inputs["type"] = combo
        return combo
    
    def _create_hours_input(self) -> QDoubleSpinBox:
        """Create hours input field."""
        hours_spin = QDoubleSpinBox()
        hours_spin.setRange(0, 24)
        hours_spin.setSingleStep(0.25)
        hours_spin.setDecimals(2)
        hours_spin.setMinimumWidth(80)
        hours_spin.setMaximumHeight(35)
        hours_spin.setSuffix(" h")
        hours_spin.valueChanged.connect(self.dataChanged)
        self.inputs["hours"] = hours_spin
        return hours_spin
    
    def _create_status_input(self) -> QComboBox:
        """Create status input field."""
        combo = QComboBox()
        combo.addItems(["", "Planned", "In Progress", "Completed", "Blocked"])
        combo.setCurrentText("In Progress")
        combo.setMinimumWidth(120)
        combo.setMaximumHeight(35)
        combo.currentTextChanged.connect(self.dataChanged)
        self.inputs["status"] = combo
        return combo
    
    def _create_language_input(self) -> QComboBox:
        """Create language input field."""
        combo = QComboBox()
        combo.setMinimumWidth(110)
        combo.setMaximumHeight(35)
        combo.currentTextChanged.connect(self.dataChanged)
        combo.currentTextChanged.connect(self._on_language_changed)
        self.inputs["language"] = combo
        return combo
    
    def _create_work_item_input(self) -> QComboBox:
        """Create work item input field."""
        combo = QComboBox()
        combo.setEditable(True)
        combo.setMinimumWidth(200)
        combo.setMaximumHeight(35)
        combo.lineEdit().setPlaceholderText("Enter work item name...")
        combo.lineEdit().textChanged.connect(self.dataChanged)
        combo.lineEdit().textChanged.connect(self._on_work_item_changed)
        self.inputs["work_item"] = combo
        return combo
    
    def _create_target_time_input(self) -> QDoubleSpinBox:
        """Create target time input field."""
        target_spin = QDoubleSpinBox()
        target_spin.setRange(0, 1000)
        target_spin.setSingleStep(1.0)
        target_spin.setDecimals(1)
        target_spin.setMinimumWidth(80)
        target_spin.setMaximumHeight(35)
        target_spin.setSuffix(" h")
        target_spin.valueChanged.connect(self.dataChanged)
        self.inputs["target_time"] = target_spin
        return target_spin
    
    def _create_difficulty_input(self) -> QComboBox:
        """Create difficulty input field."""
        combo = QComboBox()
        combo.addItems(["", "Beginner", "Intermediate", "Advanced", "Expert"])
        combo.setMinimumWidth(120)
        combo.setMaximumHeight(35)
        combo.currentTextChanged.connect(self.dataChanged)
        self.inputs["difficulty"] = combo
        return combo
    
    def _create_topic_input(self) -> QComboBox:
        """Create topic input field."""
        combo = QComboBox()
        combo.setEditable(True)
        combo.setMinimumWidth(140)
        combo.setMaximumHeight(35)
        combo.lineEdit().setPlaceholderText("Enter topic...")
        combo.lineEdit().textChanged.connect(self.dataChanged)
        self.inputs["topic"] = combo
        return combo
    
    def _create_tags_input(self) -> QComboBox:
        """Create multi-select tags input field."""
        combo = QComboBox()
        combo.setEditable(True)
        combo.setMinimumWidth(140)
        combo.setMaximumHeight(35)
        combo.lineEdit().setPlaceholderText("learning, practice...")
        combo.lineEdit().textChanged.connect(self.dataChanged)
        self.inputs["tags"] = combo
        return combo
    
    def _on_type_changed(self):
        """Handle type selection changes - implement smart field logic."""
        type_value = self.inputs["type"].currentText()
        
        if type_value == "Exercise":
            # Exercise-specific logic
            self.inputs["target_time"].setValue(0.0)  # Exercises usually single session
            self.inputs["target_time"].setEnabled(False)
        elif type_value == "Project":
            # Project-specific logic  
            self.inputs["target_time"].setEnabled(True)
        else:
            # Default state
            self.inputs["target_time"].setEnabled(True)
    
    def _on_language_changed(self):
        """Handle language changes - auto-fill suggestions."""
        # Placeholder for language-based auto-fill logic
        pass
    
    def _on_work_item_changed(self):
        """Handle work item changes - auto-fill difficulty, topic, etc."""
        # Placeholder for work item-based auto-fill logic
        pass
    
    def get_form_data(self) -> Dict[str, Any]:
        """Get current form data."""
        data = {}
        
        if "date" in self.inputs:
            data["date"] = self.inputs["date"].date().toString("yyyy-MM-dd")
        if "type" in self.inputs:
            data["type"] = self.inputs["type"].currentText()
        if "work_item" in self.inputs:
            data["canonical_name"] = self.inputs["work_item"].currentText()
        if "notes" in self.inputs:
            data["notes"] = self.inputs["notes"].toPlainText()
        if "status" in self.inputs:
            data["status"] = self.inputs["status"].currentText()
        if "hours" in self.inputs:
            data["hours_spent"] = self.inputs["hours"].value()
        if "tags" in self.inputs:
            data["tags"] = self.inputs["tags"].currentText()
        if "language" in self.inputs:
            data["language"] = self.inputs["language"].currentText()
            data["language_code"] = self.inputs["language"].currentData()
        if "difficulty" in self.inputs:
            data["difficulty"] = self.inputs["difficulty"].currentText()
        if "topic" in self.inputs:
            data["topic"] = self.inputs["topic"].currentText()
        if "target_time" in self.inputs:
            data["target_hours"] = self.inputs["target_time"].value()
            
        return data
    
    def clear_form(self):
        """Clear all form inputs."""
        if "date" in self.inputs:
            self.inputs["date"].setDate(QDate.currentDate())
        if "type" in self.inputs:
            self.inputs["type"].setCurrentIndex(0)
        if "work_item" in self.inputs:
            self.inputs["work_item"].clearEditText()
        if "notes" in self.inputs:
            self.inputs["notes"].clear()
        if "status" in self.inputs:
            self.inputs["status"].setCurrentText("In Progress")
        if "hours" in self.inputs:
            self.inputs["hours"].setValue(0.0)
        if "tags" in self.inputs:
            self.inputs["tags"].clearEditText()
        if "language" in self.inputs:
            self.inputs["language"].setCurrentIndex(0)
        if "difficulty" in self.inputs:
            self.inputs["difficulty"].setCurrentIndex(0)
        if "topic" in self.inputs:
            self.inputs["topic"].clearEditText()
        if "target_time" in self.inputs:
            self.inputs["target_time"].setValue(0.0)
    
    def set_form_data(self, data: Dict[str, Any]):
        """Populate form with data for editing."""
        if "date" in data and "date" in self.inputs:
            date_str = data["date"]
            if date_str:
                date = QDate.fromString(date_str, "yyyy-MM-dd")
                self.inputs["date"].setDate(date)
                
        if "type" in data and "type" in self.inputs:
            self.inputs["type"].setCurrentText(data["type"] or "")
            
        if "canonical_name" in data and "work_item" in self.inputs:
            self.inputs["work_item"].setCurrentText(data["canonical_name"] or "")
            
        if "notes" in data and "notes" in self.inputs:
            self.inputs["notes"].setPlainText(data["notes"] or "")
            
        if "status" in data and "status" in self.inputs:
            self.inputs["status"].setCurrentText(data["status"] or "In Progress")
            
        if "hours_spent" in data and "hours" in self.inputs:
            self.inputs["hours"].setValue(float(data["hours_spent"] or 0))
            
        if "tags" in data and "tags" in self.inputs:
            self.inputs["tags"].setCurrentText(data["tags"] or "")
            
        if "language_code" in data and "language" in self.inputs:
            combo = self.inputs["language"]
            for i in range(combo.count()):
                if combo.itemData(i) == data["language_code"]:
                    combo.setCurrentIndex(i)
                    break
                    
        if "difficulty" in data and "difficulty" in self.inputs:
            self.inputs["difficulty"].setCurrentText(data["difficulty"] or "")
            
        if "topic" in data and "topic" in self.inputs:
            self.inputs["topic"].setCurrentText(data["topic"] or "")
            
        if "target_hours" in data and "target_time" in self.inputs:
            self.inputs["target_time"].setValue(float(data["target_hours"] or 0))
    
    def update_status_display(self, message: str):
        """Update the status display label."""
        self.status_label.setText(message)
        
    def focus_first_field(self):
        """Focus the first input field."""
        if "date" in self.inputs:
            self.inputs["date"].setFocus()
            
    def load_languages(self, languages: List[tuple]):
        """Load available languages into dropdown."""
        combo = self.inputs.get("language")
        if combo:
            combo.clear()
            combo.addItem("")
            for code, name, _color in languages:
                combo.addItem(name, code)
    
    def validate_required_fields(self) -> tuple[bool, str]:
        """Validate that all required fields are filled."""
        form_data = self.get_form_data()
        
        required_fields = {
            "date": "Date",
            "type": "Type", 
            "canonical_name": "Work Item Name",
            "hours_spent": "Hours",
            "language_code": "Language"
        }
        
        missing = []
        for field, display_name in required_fields.items():
            if not form_data.get(field):
                missing.append(display_name)
        
        if missing:
            return False, f"Please fill in required fields: {', '.join(missing)}"
        
        return True, ""
