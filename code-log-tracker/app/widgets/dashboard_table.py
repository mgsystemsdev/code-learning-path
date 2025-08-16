# app/widgets/dashboard_table.py
"""
Clean UI-only dashboard table with 14 columns ready for data connection.
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QSizePolicy
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont


class DashboardTable(QWidget):
    """A clean table with 14 columns ready for data connection."""
    
    selectionChanged = Signal()
    cellChanged = Signal(int, int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.columns = [
            "Date", "Language", "Type", "Work Item Name", "Topic", "Difficulty",
            "Status", "Tags", "Hours", "Target Time", "Points", "Progress %", "ID", "Notes"
        ]
        self.data: List[Dict[str, Any]] = []
        self.filtered_data: List[Dict[str, Any]] = []
        self.setup_table()

    def setup_table(self):
        """Initialize the table widget."""
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Table
        self.table = QTableWidget(0, len(self.columns))
        self.table.setHorizontalHeaderLabels(self.columns)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(False)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Configure selection and editing
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(
            QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked
        )
        
        # Setup column widths (proportional)
        self._setup_column_widths()
        
        # Connect signals
        self.table.itemSelectionChanged.connect(self.selectionChanged)
        self.table.itemChanged.connect(self._on_cell_changed)
        
        root.addWidget(self.table, 1)

    def _setup_column_widths(self):
        """Configure column widths proportionally - no horizontal scroll."""
        header = self.table.horizontalHeader()
        
        # Use proportional widths for all 14 columns without horizontal scroll
        proportional_widths = {
            # Small (1×): ID, Date, Type, Status, Hours, Language, Progress %, Target
            "ID": 60, "Date": 100, "Type": 80, "Status": 100, "Hours": 80,
            "Language": 100, "Progress %": 90, "Target Time": 100,
            # Wide (2×): Work Item Name, Notes  
            "Work Item Name": 200, "Notes": 200,
            # Medium (1.25×): Tags, Topic, Difficulty, Points
            "Tags": 120, "Topic": 120, "Difficulty": 120, "Points": 80
        }
        
        # Set all columns to stretch proportionally - NO horizontal scroll
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setMinimumSectionSize(60)
        
        # Apply minimum widths to maintain readability
        for i, header_name in enumerate(self.columns):
            min_width = proportional_widths.get(header_name, 80)
            header.resizeSection(i, min_width)
        
        header.setStretchLastSection(False)
    
    def _on_cell_changed(self, row: int, col: int):
        """Handle cell edits."""
        self.cellChanged.emit(row, col)
    
    def load_data(self, data: List[Dict[str, Any]]):
        """Load data into table."""
        self.data = data
        self.filtered_data = data.copy()
        self._refresh_table()
    
    def _refresh_table(self):
        """Refresh table display."""
        self.table.setRowCount(len(self.filtered_data))
        
        for row_idx, row_data in enumerate(self.filtered_data):
            for col_idx, col_name in enumerate(self.columns):
                data_key = col_name.lower().replace(' ', '_').replace('%', 'pct')
                if data_key == 'work_item_name':
                    data_key = 'canonical_name'
                elif data_key == 'language':
                    data_key = 'language_code'
                elif data_key == 'hours':
                    data_key = 'hours_spent'
                elif data_key == 'target_time':
                    data_key = 'target_hours'
                
                value = row_data.get(data_key, '')
                
                if col_name == 'Hours' and value:
                    value = f"{float(value):.2f}"
                elif col_name == 'Points' and value:
                    value = f"{float(value):.1f}"
                elif col_name == 'Progress %' and value:
                    value = f"{float(value):.1f}%"
                elif col_name == 'Target Time' and value:
                    value = f"{float(value):.1f}"
                
                item = QTableWidgetItem(str(value))
                
                if col_name == 'ID':
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                
                self.table.setItem(row_idx, col_idx, item)
    
    def get_selected_row_data(self) -> Optional[Dict[str, Any]]:
        """Get selected row data."""
        current_row = self.table.currentRow()
        if 0 <= current_row < len(self.filtered_data):
            return self.filtered_data[current_row]
        return None
    
    def clear_filters(self):
        """Clear filters (placeholder for future filter implementation)."""
        pass
