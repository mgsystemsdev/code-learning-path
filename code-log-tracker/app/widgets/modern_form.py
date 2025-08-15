# app/widgets/modern_form.py
"""
Modern form widget with improved layout and styling.
"""

from __future__ import annotations
from typing import Dict, Any, Optional
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
    QGroupBox, QLabel, QPushButton, QComboBox, 
    QDoubleSpinBox, QLineEdit, QDateEdit, QFrame,
    QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt, QDate, Signal
from app.config.ui_config import UIConfig


class ModernForm(QWidget):
    """Modern, responsive form for data entry."""
    
    dataChanged = Signal()  # Emitted when form data changes
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.inputs: Dict[str, Any] = {}
        self.setup_form()
        
    def setup_form(self):
        """Create the modern form layout."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create scroll area for form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Form container
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        
        # Essential information group
        essential_group = self._create_essential_group()
        form_layout.addWidget(essential_group)
        
        # Details group
        details_group = self._create_details_group()
        form_layout.addWidget(details_group)
        
        # Status display
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #64748b;
                font-style: italic;
                padding: 8px;
                background-color: #f1f5f9;
                border-radius: 4px;
                margin: 8px 0;
            }
        """)
        form_layout.addWidget(self.status_label)
        
        # Add stretch to push content to top
        form_layout.addStretch()
        
        # Set scroll widget
        scroll.setWidget(form_widget)
        main_layout.addWidget(scroll)
        
        # Apply styling
        self.setStyleSheet(UIConfig.MAIN_STYLE)
        
    def _create_essential_group(self) -> QGroupBox:
        """Create the essential information group."""
        group = QGroupBox("Essential Information")
        layout = QGridLayout(group)
        layout.setSpacing(16)
        layout.setContentsMargins(16, 24, 16, 16)
        
        # Row 1: Date, Hours, Status
        self._add_field_to_grid(layout, "Date *", self._create_date_input(), 0, 0)
        self._add_field_to_grid(layout, "Hours *", self._create_hours_input(), 0, 1)
        self._add_field_to_grid(layout, "Status", self._create_status_input(), 0, 2)
        
        # Row 2: Language, Type
        self._add_field_to_grid(layout, "Language *", self._create_language_input(), 1, 0)
        self._add_field_to_grid(layout, "Type *", self._create_type_input(), 1, 1)
        
        # Row 3: Work Item (spans full width)
        self._add_field_to_grid(layout, "Work Item Name *", self._create_work_item_input(), 2, 0, 1, 3)
        
        return group
        
    def _create_details_group(self) -> QGroupBox:
        """Create the additional details group."""
        group = QGroupBox("Additional Details")
        layout = QGridLayout(group)
        layout.setSpacing(16)
        layout.setContentsMargins(16, 24, 16, 16)
        
        # Row 1: Difficulty, Topic
        self._add_field_to_grid(layout, "Difficulty", self._create_difficulty_input(), 0, 0)
        self._add_field_to_grid(layout, "Topic", self._create_topic_input(), 0, 1)
        
        # Row 2: Notes (spans full width)
        self._add_field_to_grid(layout, "Notes", self._create_notes_input(), 1, 0, 1, 2)
        
        # Row 3: Tags (spans full width)
        self._add_field_to_grid(layout, "Tags", self._create_tags_input(), 2, 0, 1, 2)
        
        return group
    
    def _add_field_to_grid(self, layout: QGridLayout, label_text: str, 
                          widget: QWidget, row: int, col: int, 
                          row_span: int = 1, col_span: int = 1):
        """Add a labeled field to the grid layout."""
        # Create label
        label = QLabel(label_text)
        label.setStyleSheet("""
            QLabel {
                font-weight: 600;
                color: #374151;
                margin-bottom: 4px;
            }
        """)
        
        # Create container
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(4)
        
        container_layout.addWidget(label)
        container_layout.addWidget(widget)
        
        # Add to grid
        layout.addWidget(container, row, col, row_span, col_span)
    
    def _create_date_input(self) -> QDateEdit:
        """Create date input field."""
        date_edit = QDateEdit()
        date_edit.setCalendarPopup(True)
        date_edit.setDate(QDate.currentDate())
        date_edit.setMinimumWidth(140)
        date_edit.dateChanged.connect(self.dataChanged)
        self.inputs["date"] = date_edit
        return date_edit
    
    def _create_hours_input(self) -> QDoubleSpinBox:
        """Create hours input field."""
        hours_spin = QDoubleSpinBox()
        hours_spin.setRange(0, 24)
        hours_spin.setSingleStep(0.25)
        hours_spin.setDecimals(2)
        hours_spin.setMinimumWidth(100)
        hours_spin.valueChanged.connect(self.dataChanged)
        self.inputs["hours"] = hours_spin
        return hours_spin
    
    def _create_status_input(self) -> QComboBox:
        """Create status input field."""
        combo = QComboBox()
        combo.addItems(["", "Planned", "In Progress", "Completed", "Blocked"])
        combo.setCurrentText("In Progress")
        combo.setMinimumWidth(140)
        combo.currentTextChanged.connect(self.dataChanged)
        self.inputs["status"] = combo
        return combo
    
    def _create_language_input(self) -> QComboBox:
        """Create language input field."""
        combo = QComboBox()
        combo.setMinimumWidth(160)
        combo.currentTextChanged.connect(self.dataChanged)
        self.inputs["language"] = combo
        return combo
    
    def _create_type_input(self) -> QComboBox:
        """Create type input field."""
        combo = QComboBox()
        combo.addItems(["", "Exercise", "Project"])
        combo.setMinimumWidth(120)
        combo.currentTextChanged.connect(self.dataChanged)
        self.inputs["type"] = combo
        return combo
    
    def _create_work_item_input(self) -> QComboBox:
        """Create work item input field."""
        combo = QComboBox()
        combo.setEditable(True)
        combo.setMinimumWidth(300)
        combo.lineEdit().textChanged.connect(self.dataChanged)
        self.inputs["work_item"] = combo
        return combo
    
    def _create_difficulty_input(self) -> QComboBox:
        """Create difficulty input field."""
        combo = QComboBox()
        combo.addItems(["", "Beginner", "Intermediate", "Advanced", "Expert"])
        combo.setMinimumWidth(140)
        combo.currentTextChanged.connect(self.dataChanged)
        self.inputs["difficulty"] = combo
        return combo
    
    def _create_topic_input(self) -> QComboBox:
        """Create topic input field."""
        combo = QComboBox()
        combo.setEditable(True)
        combo.setMinimumWidth(180)
        combo.lineEdit().textChanged.connect(self.dataChanged)
        self.inputs["topic"] = combo
        return combo
    
    def _create_notes_input(self) -> QLineEdit:
        """Create notes input field."""
        line_edit = QLineEdit()
        line_edit.setPlaceholderText("What did you work on?")
        line_edit.textChanged.connect(self.dataChanged)
        self.inputs["notes"] = line_edit
        return line_edit
    
    def _create_tags_input(self) -> QLineEdit:
        """Create tags input field."""
        line_edit = QLineEdit()
        line_edit.setPlaceholderText("comma, separated, tags")
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
            data["notes"] = self.inputs["notes"].text()
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
    
    def update_status_display(self, message: str):
        """Update the status display label."""
        self.status_label.setText(message)
