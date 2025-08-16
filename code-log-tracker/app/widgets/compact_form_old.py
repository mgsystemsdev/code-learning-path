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
    QPlainTextEdit, QHeaderView, QGroupBox, QFormLayout,
    QCompleter
)
from PySide6.QtCore import Qt, QDate, Signal, QTimer
from PySide6.QtGui import QFont, QStandardItemModel, QStandardItem

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
        
    def create_label(self, text: str) -> QLabel:
        """Create a right-aligned label with consistent styling."""
        label = QLabel(text)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        font = label.font()
        font.setPointSize(9)
        label.setFont(font)
        return label

    def setup_form(self):
        """Create the Learning Session Entry form with optimized horizontal layout."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Wrap in QGroupBox titled "Learning Session Entry" 
        entry_group = QGroupBox("Learning Session Entry")
        entry_group.setObjectName("entryGroup")
        
        # Use QGridLayout for the new horizontal arrangement
        grid_layout = QGridLayout(entry_group)
        grid_layout.setHorizontalSpacing(16)
        grid_layout.setVerticalSpacing(12)
        grid_layout.setContentsMargins(16, 16, 16, 16)
        
        # Configure column stretching for optimal field widths
        for col in range(12):
            if col in [7, 8, 9]:  # Work Item columns
                grid_layout.setColumnStretch(col, 2)
            elif col == 11:  # Last column
                grid_layout.setColumnStretch(col, 1)
            else:
                grid_layout.setColumnStretch(col, 1)
                
        # Create form fields with the grid layout
        self._create_form_fields(grid_layout)
        
        main_layout.addWidget(entry_group)
        
        # Status display (minimal, hidden by default)
        self.status_label = QLabel("")
        self.status_label.setFixedHeight(24)
        self.status_label.hide()
        main_layout.addWidget(self.status_label)
        
        # Apply styling
        self._apply_form_styling()
        
        # Create all form fields with proper types and configurations
        # Left this empty as form fields are created in setup_form
        
        main_layout.addWidget(entry_group)
        
        # Status display (minimal, hidden by default)
        self.status_label = QLabel("")
        self.status_label.setFixedHeight(24)
        self.status_label.hide()
        main_layout.addWidget(self.status_label)
        
        # Apply the specified stylesheet
        self._apply_form_styling()
        
    def _create_form_fields(self, grid_layout: QGridLayout):
        """Create all form fields in optimized horizontal layout."""
        
        # ROW 1: Core Data (Date, Language, Type, Work Item, Status)
        # Column spans: Date(2), Language(2), Type(2), Work Item(4), Status(2)
        
        # Date field with calendar popup
        self.inputs["date"] = QDateEdit()
        self.inputs["date"].setCalendarPopup(True)
        self.inputs["date"].setDisplayFormat("M/d/yy")
        self.inputs["date"].setDate(QDate.currentDate())
        self.inputs["date"].setMinimumHeight(32)
        self.inputs["date"].dateChanged.connect(self.dataChanged)
        grid_layout.addWidget(self.create_label("Date:"), 0, 0)
        grid_layout.addWidget(self.inputs["date"], 0, 1)
        
        # Language ComboBox with type-ahead
        self.inputs["language"] = self._create_scrollable_combo([])
        self.inputs["language"].setMinimumHeight(32)
        grid_layout.addWidget(self.create_label("Language:"), 0, 2)
        grid_layout.addWidget(self.inputs["language"], 0, 3)
        
        # Type ComboBox
        self.inputs["type"] = self._create_scrollable_combo(["", "Exercise", "Project"])
        self.inputs["type"].setMinimumHeight(32)
        self.inputs["type"].currentTextChanged.connect(self._on_type_changed)
        grid_layout.addWidget(self.create_label("Type:"), 0, 4)
        grid_layout.addWidget(self.inputs["type"], 0, 5)
        
        # Work Item ComboBox with type-ahead
        # Work Item (wider field)
        self.inputs["work_item"] = self._create_scrollable_combo([], editable=True)
        self.inputs["work_item"].setPlaceholderText("Enter work item name...")
        self.inputs["work_item"].setMinimumHeight(32)
        self.inputs["work_item"].lineEdit().textChanged.connect(self.dataChanged)
        grid_layout.addWidget(self.create_label("Work Item:"), 0, 6)
        grid_layout.addWidget(self.inputs["work_item"], 0, 7, 1, 3)  # Span 3 columns
        
        # Status
        self.inputs["status"] = self._create_scrollable_combo(["", "Planned", "In Progress", "Completed", "Blocked"])
        self.inputs["status"].setCurrentText("In Progress")
        self.inputs["status"].setMinimumHeight(32)
        grid_layout.addWidget(self.create_label("Status:"), 0, 10)
        grid_layout.addWidget(self.inputs["status"], 0, 11)
        
        # ROW 2: Details & Effort
        
        # Topic (wider field)
        self.inputs["topic"] = self._create_scrollable_combo([], editable=True)
        self.inputs["topic"].setPlaceholderText("Enter topic...")
        self.inputs["topic"].setMinimumHeight(32)
        self.inputs["topic"].lineEdit().textChanged.connect(self.dataChanged)
        grid_layout.addWidget(self.create_label("Topic:"), 1, 0)
        grid_layout.addWidget(self.inputs["topic"], 1, 1, 1, 3)  # Span 3 columns
        
        # Difficulty
        self.inputs["difficulty"] = self._create_scrollable_combo(["", "Beginner", "Intermediate", "Advanced", "Expert"])
        self.inputs["difficulty"].setMinimumHeight(32)
        grid_layout.addWidget(self.create_label("Difficulty:"), 1, 4)
        grid_layout.addWidget(self.inputs["difficulty"], 1, 5)
        
        # Hours
        self.inputs["hours"] = QDoubleSpinBox()
        self.inputs["hours"].setDecimals(2)
        self.inputs["hours"].setRange(0, 24)
        self.inputs["hours"].setSingleStep(0.25)
        self.inputs["hours"].setSuffix(" hrs")
        self.inputs["hours"].setMinimumHeight(32)
        self.inputs["hours"].valueChanged.connect(self.dataChanged)
        grid_layout.addWidget(self.create_label("Hours:"), 1, 6)
        grid_layout.addWidget(self.inputs["hours"], 1, 7)
        
        # Target Time
        self.inputs["target_time"] = QDoubleSpinBox()
        self.inputs["target_time"].setDecimals(2)
        self.inputs["target_time"].setRange(0, 200)
        self.inputs["target_time"].setSingleStep(0.5)
        self.inputs["target_time"].setSuffix(" hrs")
        self.inputs["target_time"].setMinimumHeight(32)
        self.inputs["target_time"].valueChanged.connect(self.dataChanged)
        grid_layout.addWidget(self.create_label("Target:"), 1, 8)
        grid_layout.addWidget(self.inputs["target_time"], 1, 9)
        
        # Tags
        self.inputs["tags"] = self._create_checkable_combo([
            "learning", "practice", "review", "project", "tutorial", 
            "exercise", "debugging", "research", "documentation"
        ])
        self.inputs["tags"].setMinimumHeight(32)
        grid_layout.addWidget(self.create_label("Tags:"), 1, 10)
        grid_layout.addWidget(self.inputs["tags"], 1, 11)
        
        # Notes field (expandable)
        self.inputs["notes"] = QLineEdit()
        self.inputs["notes"].setPlaceholderText("Quick notes about this session...")
        self.inputs["notes"].setMinimumHeight(32)
        self.inputs["notes"].textChanged.connect(self.dataChanged)
        grid_layout.addWidget(self.create_label("Notes:"), 2, 0)
        grid_layout.addWidget(self.inputs["notes"], 2, 1, 1, 11)  # Span the entire row
        
    def _create_scrollable_combo(self, items: List[str], editable: bool = False) -> QComboBox:
        """Create a QComboBox with proper scrolling and type-ahead as per task specs."""
        combo = QComboBox()
        combo.addItems(items)
        combo.setMinimumContentsLength(20)
        combo.setSizeAdjustPolicy(QComboBox.AdjustToContentsOnFirstShow)
        combo.setMaxVisibleItems(12)  # Dropdown scrolls beyond this
        combo.setEditable(editable)
        
        if editable and items:
            # Add type-ahead completer
            completer = QCompleter(items)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            completer.setFilterMode(Qt.MatchContains)
            combo.setCompleter(completer)
        
        combo.currentTextChanged.connect(self.dataChanged)
        return combo
        
    def _create_checkable_combo(self, items: List[str]) -> QComboBox:
        """Create a QComboBox with checkable items for multi-select tags."""
        combo = QComboBox()
        combo.setMinimumContentsLength(20)
        combo.setSizeAdjustPolicy(QComboBox.AdjustToContentsOnFirstShow)
        combo.setMaxVisibleItems(12)
        
        # Set up model with checkable items
        model = QStandardItemModel()
        for item_text in items:
            item = QStandardItem(item_text)
            item.setCheckable(True)
            model.appendRow(item)
        
        combo.setModel(model)
        combo.setPlaceholderText("Select tags...")
        
        # Update display text when selections change
        model.itemChanged.connect(lambda: self._update_tags_display(combo))
        return combo
        
    def _update_tags_display(self, combo: QComboBox):
        """Update combo display to show selected tags."""
        model = combo.model()
        selected = []
        for i in range(model.rowCount()):
            item = model.item(i)
            if item.checkState() == Qt.Checked:
                selected.append(item.text())
        
        if selected:
            combo.setCurrentText(", ".join(selected))
        else:
            combo.setCurrentText("")
        
        self.dataChanged.emit()
        
    def _apply_form_styling(self):
        """Apply the specified stylesheet for consistent appearance."""
        self.setStyleSheet("""
            QGroupBox#entryGroup { 
                border: 1px solid #3b3f46; 
                border-radius: 10px; 
                margin-top: 12px; 
                padding: 16px;
                font-weight: bold;
            }
            QGroupBox::title { 
                subcontrol-origin: margin;
                left: 8px; 
                padding: 0 8px;
                color: #e2e8f0;
            }
            QLabel {
                color: #94a3b8;
                font-size: 11pt;
                padding-right: 4px;
            }
            QComboBox, QLineEdit, QDateEdit, QDoubleSpinBox {
                min-height: 34px; 
                padding: 4px 12px;
                border: 1px solid #4a4f57; 
                border-radius: 6px;
                background-color: #2d3748;
                color: #e2e8f0;
                font-size: 11pt;
            }
            QComboBox:focus, QLineEdit:focus, QDateEdit:focus, QDoubleSpinBox:focus {
                border-color: #3b82f6;
                background-color: #374151;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 8px;
            }
            QComboBox::down-arrow {
                width: 14px;
                height: 14px;
            }
            QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
                border: none;
                padding: 2px 4px;
            }
            QComboBox QAbstractItemView { 
                min-width: 280px;
                background-color: #2d3748;
                border: 1px solid #4a4f57;
                selection-background-color: #3b82f6;
            }
        """)
        
    def _on_type_changed(self):
        """Handle type selection changes."""
        type_value = self.inputs["type"].currentText()
        # Enable/disable target time based on type
        if type_value == "Exercise":
            self.inputs["target_time"].setValue(0.0)
            self.inputs["target_time"].setEnabled(False)
        else:
            self.inputs["target_time"].setEnabled(True)
        

    
    def get_form_data(self) -> Dict[str, Any]:
        """Get current form data from the new form layout."""
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
            # For tags combo, get the current text (could be comma-separated selected tags)
            data["tags"] = self.inputs["tags"].currentText()
        if "notes" in self.inputs:
            # Notes is now a QLineEdit instead of QPlainTextEdit
            data["notes"] = self.inputs["notes"].text()
        
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
            if self.inputs["work_item"].isEditable():
                self.inputs["work_item"].clearEditText()
            else:
                self.inputs["work_item"].setCurrentIndex(0)
        if "status" in self.inputs:
            self.inputs["status"].setCurrentText("In Progress")
        if "hours" in self.inputs:
            self.inputs["hours"].setValue(0.0)
        if "target_time" in self.inputs:
            self.inputs["target_time"].setValue(0.0)
        if "difficulty" in self.inputs:
            self.inputs["difficulty"].setCurrentIndex(0)
        if "topic" in self.inputs:
            if self.inputs["topic"].isEditable():
                self.inputs["topic"].clearEditText()
            else:
                self.inputs["topic"].setCurrentIndex(0)
        if "tags" in self.inputs:
            # Clear checkable tags
            model = self.inputs["tags"].model()
            if model:
                for i in range(model.rowCount()):
                    item = model.item(i)
                    if item:
                        item.setCheckState(Qt.Unchecked)
            self.inputs["tags"].setCurrentText("")
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
            # Handle tags for checkable combo - parse comma-separated values
            tags_text = data["tags"] or ""
            if tags_text:
                tag_list = [tag.strip() for tag in tags_text.split(",")]
                model = self.inputs["tags"].model()
                if model:
                    for i in range(model.rowCount()):
                        item = model.item(i)
                        if item and item.text() in tag_list:
                            item.setCheckState(Qt.Checked)
                self._update_tags_display(self.inputs["tags"])
            
        if "notes" in data and "notes" in self.inputs:
            # Notes is now a QLineEdit, not QPlainTextEdit
            self.inputs["notes"].setText(data["notes"] or "")
    
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
