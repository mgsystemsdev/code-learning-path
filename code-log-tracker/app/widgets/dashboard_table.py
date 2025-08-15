# app/widgets/dashboard_table.py
"""
Dashboard table with all 14 columns always visible, proportional widths,
frozen header, filter row, and inline editing.
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
    QHeaderView, QAbstractItemView, QLineEdit, QComboBox,
    QTableWidgetItem, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from app.config.ui_config import UIConfig
from app.config.table_config import TableConfig


class FilterRow(QWidget):
    """Filter row widget with search inputs for each column."""
    
    filterChanged = Signal(str, str)  # column, filter_text
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.filters: Dict[str, QWidget] = {}
        self.setup_filters()
        
    def setup_filters(self):
        """Create filter inputs for each column."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)
        
        for i, header in enumerate(TableConfig.HEADERS):
            filter_widget = self._create_filter_widget(header)
            if filter_widget:
                self.filters[header] = filter_widget
                layout.addWidget(filter_widget)
            else:
                # Add spacer for columns without filters
                spacer = QWidget()
                spacer.setFixedWidth(TableConfig.COLUMN_WIDTHS_LIST[i])
                layout.addWidget(spacer)
        
        self.setStyleSheet("""
            QLineEdit, QComboBox {
                border: 1px solid #475569;
                border-radius: 3px;
                padding: 4px 6px;
                background-color: #334155;
                color: #f1f5f9;
                font-size: 11px;
                margin: 1px;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #60a5fa;
                background-color: #475569;
            }
        """)
    
    def _create_filter_widget(self, header: str) -> Optional[QWidget]:
        """Create appropriate filter widget for column."""
        # Skip filters for read-only columns
        if header in ["ID", "Points", "Progress %"]:
            return None
            
        if header in ["Type", "Status", "Language", "Difficulty"]:
            # Dropdown filters for enum-like fields
            combo = QComboBox()
            combo.addItem("")  # Empty = no filter
            
            if header == "Type":
                combo.addItems(["Exercise", "Project"])
            elif header == "Status":
                combo.addItems(["Planned", "In Progress", "Completed", "Blocked"])
            elif header == "Language":
                # Will be populated by main window
                combo.addItems(["Python", "JavaScript", "HTML/CSS"])  # Default
            elif header == "Difficulty":
                combo.addItems(["Beginner", "Intermediate", "Advanced", "Expert"])
                
            combo.currentTextChanged.connect(
                lambda text, h=header: self.filterChanged.emit(h, text)
            )
            return combo
        else:
            # Text input filters for other fields
            line_edit = QLineEdit()
            line_edit.setPlaceholderText(f"Filter {header}...")
            line_edit.textChanged.connect(
                lambda text, h=header: self.filterChanged.emit(h, text)
            )
            return line_edit
    
    def clear_all_filters(self):
        """Clear all filter inputs."""
        for widget in self.filters.values():
            if isinstance(widget, QLineEdit):
                widget.clear()
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)


class DashboardTable(QWidget):
    """
    Full-screen dashboard table with all 14 columns visible,
    proportional widths, filter row, and inline editing.
    """
    
    selectionChanged = Signal()
    cellChanged = Signal(int, int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.table: Optional[QTableWidget] = None
        self.filter_row: Optional[FilterRow] = None
        self.filters: Dict[str, str] = {}
        self.original_data: List[Dict[str, Any]] = []
        self.setup_table()
    
    def setup_table(self):
        """Create the dashboard table with filter row."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create table
        self.table = QTableWidget(0, len(TableConfig.HEADERS))
        self.table.setHorizontalHeaderLabels(TableConfig.HEADERS)
        self.table.verticalHeader().setVisible(False)
        
        # Table configuration
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(
            QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked
        )
        
        # Apply styling
        self.table.setStyleSheet(UIConfig.MAIN_STYLE)
        
        # Configure headers and column widths
        self._setup_columns()
        
        # Install delegates
        self._install_delegates()
        
        # Create filter row
        self.filter_row = FilterRow()
        self.filter_row.filterChanged.connect(self._apply_filter)
        
        # Add to layout
        layout.addWidget(self.table, 1)  # Table takes remaining space
        layout.addWidget(self.filter_row, 0)  # Filter row fixed height
        
        # Connect signals
        self.table.itemSelectionChanged.connect(self.selectionChanged)
        self.table.itemChanged.connect(self._on_cell_changed)
    
    def _setup_columns(self):
        """Configure column widths proportionally - no horizontal scroll."""
        header = self.table.horizontalHeader()
        
        # Use proportional widths for all 14 columns without horizontal scroll
        proportional_widths = {
            # Small (1×): ID, Date, Type, Status, Hours, Language, Progress %, Target
            "ID": 60, "Date": 100, "Type": 80, "Status": 100, "Hours": 80,
            "Language": 100, "Progress %": 90, "Target Hours": 100,
            # Wide (2×): Work Item Name, Notes  
            "Work Item": 200, "Notes": 200,
            # Medium (1.25×): Tags, Topic, Difficulty, Points
            "Tags": 120, "Topic": 120, "Difficulty": 120, "Points": 80
        }
        
        # Set all columns to stretch proportionally - NO horizontal scroll
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setMinimumSectionSize(60)
        
        # Apply minimum widths to maintain readability
        for i, header_name in enumerate(TableConfig.HEADERS):
            min_width = proportional_widths.get(header_name, 80)
            header.resizeSection(i, min_width)
        
        # Right-align numeric columns
        numeric_columns = ["Hours", "Target Hours", "Points", "Progress %"]
        for col_name in numeric_columns:
            if col_name in TableConfig.HEADERS:
                col_idx = TableConfig.HEADERS.index(col_name)
                # This will be applied when data is loaded
        
        header.setStretchLastSection(False)
        
    def _install_delegates(self):
        """Install custom delegates for inline editing."""
        from app.dialogs import DateDelegate, HoursDelegate, ComboDelegate
        
        col_map = {h: i for i, h in enumerate(TableConfig.HEADERS)}
        
        # Date delegate
        if "Date" in col_map:
            self.table.setItemDelegateForColumn(col_map["Date"], DateDelegate(self.table))
            
        # Type delegate  
        if "Type" in col_map:
            self.table.setItemDelegateForColumn(
                col_map["Type"],
                ComboDelegate(lambda: ["Exercise", "Project"], parent=self.table)
            )
            
        # Status delegate
        if "Status" in col_map:
            self.table.setItemDelegateForColumn(
                col_map["Status"],
                ComboDelegate(
                    lambda: ["Planned", "In Progress", "Completed", "Blocked"], 
                    parent=self.table
                )
            )
            
        # Hours delegate
        if "Hours" in col_map:
            self.table.setItemDelegateForColumn(col_map["Hours"], HoursDelegate(self.table))
            
        # Target Time delegate
        if "Target Time" in col_map:
            self.table.setItemDelegateForColumn(col_map["Target Time"], HoursDelegate(self.table))
            
        # Language delegate
        if "Language" in col_map:
            self.table.setItemDelegateForColumn(
                col_map["Language"],
                ComboDelegate(lambda: self._get_language_names(), parent=self.table)
            )
            
        # Difficulty delegate
        if "Difficulty" in col_map:
            self.table.setItemDelegateForColumn(
                col_map["Difficulty"],
                ComboDelegate(
                    lambda: ["Beginner", "Intermediate", "Advanced", "Expert"],
                    parent=self.table
                )
            )
    
    def _get_language_names(self) -> List[str]:
        """Get language names for delegate - populated by main window."""
        return ["Python", "JavaScript", "HTML/CSS", "React", "Django"]  # Default
    
    def _on_cell_changed(self, item: QTableWidgetItem):
        """Handle cell value changes."""
        self.cellChanged.emit(item.row(), item.column())
    
    def _apply_filter(self, column: str, filter_text: str):
        """Apply filter to table data."""
        self.filters[column] = filter_text.lower()
        self._refresh_filtered_data()
    
    def _refresh_filtered_data(self):
        """Refresh table with filtered data."""
        if not self.original_data:
            return
            
        # Apply all active filters
        filtered_data = []
        for row_data in self.original_data:
            include_row = True
            
            for column, filter_text in self.filters.items():
                if not filter_text:
                    continue
                    
                # Get the corresponding key for this column
                col_idx = TableConfig.HEADERS.index(column) if column in TableConfig.HEADERS else -1
                if col_idx >= 0:
                    key = TableConfig.KEYS[col_idx]
                    cell_value = str(row_data.get(key, "")).lower()
                    
                    if filter_text not in cell_value:
                        include_row = False
                        break
            
            if include_row:
                filtered_data.append(row_data)
        
        # Update table with filtered data
        self.load_data(filtered_data, is_filtered=True)
    
    def load_data(self, data: List[Dict[str, Any]], is_filtered: bool = False):
        """Load data into the table."""
        if not is_filtered:
            self.original_data = data.copy()
            
        self.table.setRowCount(len(data))
        
        for row_idx, row_data in enumerate(data):
            for col_idx, key in enumerate(TableConfig.KEYS):
                value = row_data.get(key, "")
                
                # Format numeric values
                if isinstance(value, (int, float)) and key != "id":
                    if key == "progress_pct":
                        value = f"{value:.1f}%" if value else "0.0%"
                    elif key in ["hours_spent", "points_awarded", "target_hours"]:
                        value = f"{value:.2f}" if value else "0.00"
                
                # Create item
                item = QTableWidgetItem(str(value))
                
                # Make read-only columns non-editable
                if col_idx in TableConfig.READONLY_COLUMNS:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                
                self.table.setItem(row_idx, col_idx, item)
    
    def get_selected_row_data(self) -> Optional[Dict[str, Any]]:
        """Get data from currently selected row."""
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            return None
            
        row = selected_rows[0].row()
        row_data = {}
        
        for col_idx, key in enumerate(TableConfig.KEYS):
            item = self.table.item(row, col_idx)
            if item:
                row_data[key] = item.text()
        
        return row_data
    
    def clear_filters(self):
        """Clear all filters and show all data."""
        self.filters.clear()
        if self.filter_row:
            self.filter_row.clear_all_filters()
        if self.original_data:
            self.load_data(self.original_data)
    
    def get_row_count(self) -> int:
        """Get current number of visible rows."""
        return self.table.rowCount()
    
    def select_row(self, row: int):
        """Select a specific row."""
        if 0 <= row < self.table.rowCount():
            self.table.selectRow(row)
