# app/widgets/scrollable_form.py
"""
Enhanced scrollable form with dark theme and improved organization.
"""

from __future__ import annotations
from typing import Dict, Any, Optional
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
    QGroupBox, QLabel, QPushButton, QComboBox, 
    QDoubleSpinBox, QLineEdit, QDateEdit, QFrame,
    QScrollArea, QSizePolicy, QTextEdit, QSpacerItem
)
from PySide6.QtCore import Qt, QDate, Signal
from app.config.ui_config import UIConfig


class ScrollableForm(QWidget):
    """Modern, scrollable form with dark theme and enhanced organization."""
    
    dataChanged = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.inputs: Dict[str, Any] = {}
        self.setup_form()
        
    def setup_form(self):
        """Create the enhanced scrollable form layout."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create main scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setFrameShape(QFrame.NoFrame)
        
        # Form container with padding
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setContentsMargins(16, 16, 16, 16)
        form_layout.setSpacing(20)
        
        # Essential information section
        essential_section = self._create_essential_section()
        form_layout.addWidget(essential_section)
        
        # Time and progress section
        time_section = self._create_time_section()
        form_layout.addWidget(time_section)
        
        # Additional details section
        details_section = self._create_details_section()
        form_layout.addWidget(details_section)
        
        # Notes section (expanded)
        notes_section = self._create_notes_section()
        form_layout.addWidget(notes_section)
        
        # Status display
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #60a5fa;
                font-style: italic;
                font-weight: 500;
                padding: 12px;
                background-color: #334155;
                border: 1px solid #475569;
                border-radius: 8px;
                margin: 8px 0;
            }
        """)
        form_layout.addWidget(self.status_label)
        
        # Add stretch to push content to top
        form_layout.addStretch()
        
        # Set scroll widget
        scroll.setWidget(form_widget)
        main_layout.addWidget(scroll)
        
    def _create_essential_section(self) -> QGroupBox:
        """Create essential information section."""
        group = QGroupBox("🎯 Essential Information")
        layout = QGridLayout(group)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 30, 20, 20)
        
        # Row 1: Date and Language (most important)
        self._add_field_to_grid(layout, "📅 Date *", self._create_date_input(), 0, 0)
        self._add_field_to_grid(layout, "💻 Language *", self._create_language_input(), 0, 1)
        
        # Row 2: Type and Work Item
        self._add_field_to_grid(layout, "📂 Type *", self._create_type_input(), 1, 0)
        self._add_field_to_grid(layout, "📝 Work Item *", self._create_work_item_input(), 1, 1, 1, 1)
        
        return group
        
    def _create_time_section(self) -> QGroupBox:
        """Create time and progress section."""
        group = QGroupBox("⏱️ Time & Progress")
        layout = QGridLayout(group)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 30, 20, 20)
        
        # Row 1: Hours and Status
        self._add_field_to_grid(layout, "🕒 Hours Spent *", self._create_hours_input(), 0, 0)
        self._add_field_to_grid(layout, "📊 Status", self._create_status_input(), 0, 1)
        
        return group
        
    def _create_details_section(self) -> QGroupBox:
        """Create additional details section."""
        group = QGroupBox("🔧 Learning Details")
        layout = QGridLayout(group)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 30, 20, 20)
        
        # Row 1: Difficulty and Topic
        self._add_field_to_grid(layout, "🎖️ Difficulty", self._create_difficulty_input(), 0, 0)
        self._add_field_to_grid(layout, "🎯 Topic", self._create_topic_input(), 0, 1)
        
        # Row 2: Tags (spans full width)
        self._add_field_to_grid(layout, "🏷️ Tags", self._create_tags_input(), 1, 0, 1, 2)
        
        return group
        
    def _create_notes_section(self) -> QGroupBox:
        """Create expandable notes section."""
        group = QGroupBox("📋 Session Notes")
        layout = QVBoxLayout(group)
        layout.setContentsMargins(20, 30, 20, 20)
        layout.setSpacing(12)
        
        # Notes field with more space
        notes_label = QLabel("What did you work on today?")
        notes_label.setStyleSheet("""
            QLabel {
                color: #cbd5e1;
                font-weight: 500;
                margin-bottom: 8px;
            }
        """)
        layout.addWidget(notes_label)
        
        self.inputs["notes"] = QTextEdit()
        self.inputs["notes"].setMaximumHeight(120)
        self.inputs["notes"].setMinimumHeight(80)
        self.inputs["notes"].setPlaceholderText(
            "Describe what you learned, challenges faced, or key insights..."
        )
        self.inputs["notes"].setStyleSheet("""
            QTextEdit {
                border: 2px solid #475569;
                border-radius: 8px;
                padding: 12px;
                background-color: #334155;
                color: #f8fafc;
                font-size: 13px;
                line-height: 1.4;
            }
            QTextEdit:focus {
                border-color: #60a5fa;
                background-color: #475569;
            }
        """)
        self.inputs["notes"].textChanged.connect(self.dataChanged)
        layout.addWidget(self.inputs["notes"])
        
        return group
    
    def _add_field_to_grid(self, layout: QGridLayout, label_text: str, 
                          widget: QWidget, row: int, col: int, 
                          row_span: int = 1, col_span: int = 1):
        """Add a labeled field to the grid layout with enhanced styling."""
        # Create container
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(8)
        
        # Create label with enhanced styling
        label = QLabel(label_text)
        label.setStyleSheet("""
            QLabel {
                font-weight: 600;
                color: #cbd5e1;
                font-size: 13px;
                margin-bottom: 4px;
            }
        """)
        container_layout.addWidget(label)
        
        # Add widget
        container_layout.addWidget(widget)
        
        # Add to grid
        layout.addWidget(container, row, col, row_span, col_span)
    
    def _create_date_input(self) -> QDateEdit:
        """Create enhanced date input."""
        date_edit = QDateEdit()
        date_edit.setCalendarPopup(True)
        date_edit.setDate(QDate.currentDate())
        date_edit.setMinimumWidth(160)
        date_edit.setMinimumHeight(45)
        date_edit.dateChanged.connect(self.dataChanged)
        self.inputs["date"] = date_edit
        return date_edit
    
    def _create_language_input(self) -> QComboBox:
        """Create enhanced language input."""
        combo = QComboBox()
        combo.setMinimumWidth(180)
        combo.setMinimumHeight(45)
        combo.currentTextChanged.connect(self.dataChanged)
        self.inputs["language"] = combo
        return combo
    
    def _create_type_input(self) -> QComboBox:
        """Create enhanced type input."""
        combo = QComboBox()
        combo.addItems(["", "Exercise", "Project"])
        combo.setMinimumWidth(140)
        combo.setMinimumHeight(45)
        combo.currentTextChanged.connect(self.dataChanged)
        self.inputs["type"] = combo
        return combo
    
    def _create_work_item_input(self) -> QComboBox:
        """Create enhanced work item input."""
        combo = QComboBox()
        combo.setEditable(True)
        combo.setMinimumWidth(300)
        combo.setMinimumHeight(45)
        combo.lineEdit().setPlaceholderText("Enter or select work item name...")
        combo.lineEdit().textChanged.connect(self.dataChanged)
        self.inputs["work_item"] = combo
        return combo
    
    def _create_hours_input(self) -> QDoubleSpinBox:
        """Create enhanced hours input."""
        hours_spin = QDoubleSpinBox()
        hours_spin.setRange(0, 24)
        hours_spin.setSingleStep(0.25)
        hours_spin.setDecimals(2)
        hours_spin.setMinimumWidth(120)
        hours_spin.setMinimumHeight(45)
        hours_spin.setSuffix(" hrs")
        hours_spin.valueChanged.connect(self.dataChanged)
        self.inputs["hours"] = hours_spin
        return hours_spin
    
    def _create_status_input(self) -> QComboBox:
        """Create enhanced status input."""
        combo = QComboBox()
        combo.addItems(["", "Planned", "In Progress", "Completed", "Blocked"])
        combo.setCurrentText("In Progress")
        combo.setMinimumWidth(160)
        combo.setMinimumHeight(45)
        combo.currentTextChanged.connect(self.dataChanged)
        self.inputs["status"] = combo
        return combo
    
    def _create_difficulty_input(self) -> QComboBox:
        """Create enhanced difficulty input."""
        combo = QComboBox()
        combo.addItems(["", "Beginner", "Intermediate", "Advanced", "Expert"])
        combo.setMinimumWidth(160)
        combo.setMinimumHeight(45)
        combo.currentTextChanged.connect(self.dataChanged)
        self.inputs["difficulty"] = combo
        return combo
    
    def _create_topic_input(self) -> QComboBox:
        """Create enhanced topic input."""
        combo = QComboBox()
        combo.setEditable(True)
        combo.setMinimumWidth(200)
        combo.setMinimumHeight(45)
        combo.lineEdit().setPlaceholderText("Enter or select topic...")
        combo.lineEdit().textChanged.connect(self.dataChanged)
        self.inputs["topic"] = combo
        return combo
    
    def _create_tags_input(self) -> QLineEdit:
        """Create enhanced tags input."""
        line_edit = QLineEdit()
        line_edit.setPlaceholderText("learning, practice, review, debugging...")
        line_edit.setMinimumHeight(45)
        line_edit.textChanged.connect(self.dataChanged)
        self.inputs["tags"] = line_edit
        return line_edit
    
    def get_form_data(self) -> Dict[str, Any]:
        """Get current form data."""
        data = {}
        
        if "date" in self.inputs:
            data["date"] = self.inputs["date"].date().toString("yyyy-MM-dd")
        if "hours" in self.inputs:
            data["hours_spent"] = self.inputs["hours"].value()
        if "status" in self.inputs:
            data["status"] = self.inputs["status"].currentText()
        if "language" in self.inputs:
            data["language"] = self.inputs["language"].currentText()
            data["language_code"] = self.inputs["language"].currentData()
        if "type" in self.inputs:
            data["type"] = self.inputs["type"].currentText()
        if "work_item" in self.inputs:
            data["work_item"] = self.inputs["work_item"].currentText()
        if "difficulty" in self.inputs:
            data["difficulty"] = self.inputs["difficulty"].currentText()
        if "topic" in self.inputs:
            data["topic"] = self.inputs["topic"].currentText()
        if "notes" in self.inputs:
            data["notes"] = self.inputs["notes"].toPlainText()
        if "tags" in self.inputs:
            data["tags"] = self.inputs["tags"].text()
            
        return data
    
    def clear_form(self):
        """Clear all form inputs."""
        if "date" in self.inputs:
            self.inputs["date"].setDate(QDate.currentDate())
        if "hours" in self.inputs:
            self.inputs["hours"].setValue(0.0)
        if "status" in self.inputs:
            self.inputs["status"].setCurrentText("In Progress")
        if "language" in self.inputs:
            self.inputs["language"].setCurrentIndex(0)
        if "type" in self.inputs:
            self.inputs["type"].setCurrentIndex(0)
        if "work_item" in self.inputs:
            self.inputs["work_item"].clearEditText()
        if "difficulty" in self.inputs:
            self.inputs["difficulty"].setCurrentIndex(0)
        if "topic" in self.inputs:
            self.inputs["topic"].clearEditText()
        if "notes" in self.inputs:
            self.inputs["notes"].clear()
        if "tags" in self.inputs:
            self.inputs["tags"].clear()
    
    def set_form_data(self, data: Dict[str, Any]):
        """Populate form with data for editing."""
        if "date" in data and "date" in self.inputs:
            date_str = data["date"]
            if date_str:
                date = QDate.fromString(date_str, "yyyy-MM-dd")
                self.inputs["date"].setDate(date)
                
        if "hours_spent" in data and "hours" in self.inputs:
            self.inputs["hours"].setValue(float(data["hours_spent"] or 0))
            
        if "status" in data and "status" in self.inputs:
            self.inputs["status"].setCurrentText(data["status"] or "In Progress")
            
        if "language_code" in data and "language" in self.inputs:
            # Find and set language by code
            combo = self.inputs["language"]
            for i in range(combo.count()):
                if combo.itemData(i) == data["language_code"]:
                    combo.setCurrentIndex(i)
                    break
                    
        if "type" in data and "type" in self.inputs:
            self.inputs["type"].setCurrentText(data["type"] or "")
            
        if "canonical_name" in data and "work_item" in self.inputs:
            self.inputs["work_item"].setCurrentText(data["canonical_name"] or "")
            
        if "difficulty" in data and "difficulty" in self.inputs:
            self.inputs["difficulty"].setCurrentText(data["difficulty"] or "")
            
        if "topic" in data and "topic" in self.inputs:
            self.inputs["topic"].setCurrentText(data["topic"] or "")
            
        if "notes" in data and "notes" in self.inputs:
            self.inputs["notes"].setPlainText(data["notes"] or "")
            
        if "tags" in data and "tags" in self.inputs:
            self.inputs["tags"].setText(data["tags"] or "")
    
    def update_status_display(self, message: str):
        """Update the status display label."""
        self.status_label.setText(message)
        
    def focus_first_field(self):
        """Focus the first input field."""
        if "date" in self.inputs:
            self.inputs["date"].setFocus()
