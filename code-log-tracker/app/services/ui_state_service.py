# app/services/ui_state_service.py
"""
UI State Service - Handles UI state management and formatting.

Handles:
- Status display formatting
- UI state persistence
- Display formatting utilities
"""

from __future__ import annotations
from typing import Dict, Any, List
from PySide6.QtWidgets import (
    QWidget, QComboBox, QDateEdit, QDoubleSpinBox, QPlainTextEdit, QLineEdit,
    QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy, QPushButton, QFrame,
    QTableWidget, QHeaderView, QMainWindow
)
from PySide6.QtCore import Qt, Signal, QDate
# from .widgets.compact_form import CompactForm
# from .widgets.session_table import SessionTable


class UIStateService:
    """Service for managing UI state and display formatting."""

    def format_item_status(self, item: Dict[str, Any]) -> List[str]:
        """Format item information for status display.
        
        Args:
            item: Dictionary containing item data
            
        Returns:
            List of formatted status strings
        """
        status_parts = []
        
        if item.get("name"):
            status_parts.append(f"Item: {item['name']}")
            
        if item.get("language"):
            status_parts.append(f"Language: {item['language']}")
            
        if item.get("topic"):
            status_parts.append(f"Topic: {item['topic']}")
            
        if item.get("difficulty"):
            status_parts.append(f"Difficulty: {item['difficulty']}")
            
        return status_parts


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1400, 820)  # Slightly under full screen
        
        # Create central widget and layout
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Add table
        self.table = SessionTable()
        layout.addWidget(self.table)
        
        # Add compact form at bottom
        self.form = CompactForm()
        layout.addWidget(self.form)


class CompactForm(QFrame):
    saved = Signal(dict)  # Emitted when form is saved
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setFixedHeight(140)  # Fixed height, no scrolling
        
        # Helper functions for creating widgets
        self._setup_helpers()
        # Create and layout all widgets
        self._setup_ui()
        # Connect signals
        self._connect_signals()
        
    def _setup_helpers(self):
        """Create helper functions for widget creation"""
        def make_label(text):
            label = QLabel(text)
            label.setStyleSheet("color: #a0aec0; font-size: 12px; letter-spacing: 0.5px;")
            return label
            
        def make_combo(items, editable=False):
            cb = QComboBox()
            if items: cb.addItems(items)
            cb.setEditable(editable)
            cb.setInsertPolicy(QComboBox.NoInsert)
            cb.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            cb.setMinimumHeight(34)
            cb.setStyleSheet("padding: 4px 8px;")
            return cb
            
        def make_spin(minv, maxv, step, decimals=2):
            sp = QDoubleSpinBox()
            sp.setRange(minv, maxv)
            sp.setSingleStep(step)
            sp.setDecimals(decimals)
            sp.setButtonSymbols(QDoubleSpinBox.PlusMinus)
            sp.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            sp.setMinimumHeight(34)
            return sp
            
        self.make_label = make_label
        self.make_combo = make_combo
        self.make_spin = make_spin
        
    def _setup_ui(self):
        """Create and arrange all widgets"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Row A: Essential fields
        row_a = QHBoxLayout()
        row_a.setSpacing(16)
        
        # Date
        date_container = QVBoxLayout()
        date_container.addWidget(self.make_label("Date"))
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setMinimumHeight(34)
        date_container.addWidget(self.date_edit)
        row_a.addLayout(date_container)
        
        # Language
        lang_container = QVBoxLayout()
        lang_container.addWidget(self.make_label("Language"))
        self.language = self.make_combo(['Python', 'JavaScript', 'Java', 'C++'], True)
        lang_container.addWidget(self.language)
        row_a.addLayout(lang_container)
        
        # Type
        type_container = QVBoxLayout()
        type_container.addWidget(self.make_label("Type"))
        self.type_combo = self.make_combo(['Exercise', 'Project'])
        type_container.addWidget(self.type_combo)
        row_a.addLayout(type_container)
        
        # Work Item Name
        work_container = QVBoxLayout()
        work_container.addWidget(self.make_label("Work Item Name"))
        self.work_item = self.make_combo([], True)
        work_container.addWidget(self.work_item)
        row_a.addLayout(work_container, stretch=2)
        
        # Status
        status_container = QVBoxLayout()
        status_container.addWidget(self.make_label("Status"))
        self.status = self.make_combo(['Planned', 'In Progress', 'Completed', 'Blocked'])
        status_container.addWidget(self.status)
        row_a.addLayout(status_container)
        
        layout.addLayout(row_a)
        
        # Row B: Detail fields
        row_b = QHBoxLayout()
        row_b.setSpacing(16)
        
        # Hours
        hours_container = QVBoxLayout()
        hours_container.addWidget(self.make_label("Hours"))
        self.hours = self.make_spin(0, 24, 0.25)
        hours_container.addWidget(self.hours)
        row_b.addLayout(hours_container)
        
        # Target Time
        target_container = QVBoxLayout()
        target_container.addWidget(self.make_label("Target Time"))
        self.target = self.make_spin(0, 200, 0.5)
        target_container.addWidget(self.target)
        row_b.addLayout(target_container)
        
        # Difficulty
        diff_container = QVBoxLayout()
        diff_container.addWidget(self.make_label("Difficulty"))
        self.difficulty = self.make_combo(['Beginner', 'Intermediate', 'Advanced'])
        diff_container.addWidget(self.difficulty)
        row_b.addLayout(diff_container)
        
        # Topic
        topic_container = QVBoxLayout()
        topic_container.addWidget(self.make_label("Topic Area"))
        self.topic = self.make_combo([], True)
        topic_container.addWidget(self.topic)
        row_b.addLayout(topic_container)
        
        # Tags
        tags_container = QVBoxLayout()
        tags_container.addWidget(self.make_label("Tags"))
        self.tags = QLineEdit()
        self.tags.setMinimumHeight(34)
        tags_container.addWidget(self.tags)
        row_b.addLayout(tags_container)
        
        # Notes
        notes_container = QVBoxLayout()
        notes_container.addWidget(self.make_label("Notes"))
        self.notes = QPlainTextEdit()
        self.notes.setFixedHeight(56)
        self.notes.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.notes.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        notes_container.addWidget(self.notes)
        row_b.addLayout(notes_container, stretch=2)
        
        layout.addLayout(row_b)


class SessionTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_table()
        
    def _setup_table(self):
        # Set columns
        columns = [
            "ID", "Date", "Language", "Type", "Work Item Name", 
            "Status", "Hours", "Target Time", "Difficulty",
            "Topic", "Tags", "Progress %", "Points", "Notes"
        ]
        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels(columns)
        
        # Configure header
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setMinimumSectionSize(80)
        
        # Set column widths
        widths = {
            "Work Item Name": 2,  # 2x width
            "Notes": 2,
            "Tags": 1.25,
            "Topic": 1.25,
            "Difficulty": 1.25
        }
        
        for i, col in enumerate(columns):
            multiplier = widths.get(col, 1)
            width = int(80 * multiplier)
            self.setColumnWidth(i, width)
            
            # Right-align numeric columns
            if col in ["Hours", "Target Time", "Progress %", "Points"]:
                self.horizontalHeaderItem(i).setTextAlignment(Qt.AlignRight)
        
        # Only vertical scrolling
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
