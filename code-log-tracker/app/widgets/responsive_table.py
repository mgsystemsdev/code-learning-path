# app/widgets/responsive_table.py
"""
Responsive table widget that adapts to screen size.
"""

from __future__ import annotations
from typing import List, Dict, Set
from PySide6.QtWidgets import QTableWidget, QHeaderView, QAbstractItemView
from PySide6.QtCore import QSize, Signal
from app.config.ui_config import UIConfig
from app.config.table_config import TableConfig


class ResponsiveTable(QTableWidget):
    """Table that automatically adjusts visible columns based on available width."""
    
    columnsChanged = Signal()  # Emitted when column visibility changes
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.visible_columns: Set[int] = set()
        self.setup_table()
        
    def setup_table(self):
        """Configure table with modern styling and responsive behavior."""
        # Basic table setup
        self.setColumnCount(len(TableConfig.HEADERS))
        self.setHorizontalHeaderLabels(TableConfig.HEADERS)
        self.verticalHeader().setVisible(False)
        
        # Selection and editing
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setAlternatingRowColors(True)
        self.setEditTriggers(
            QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked
        )
        
        # Header configuration
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setStretchLastSection(False)
        
        # Apply styling
        self.setStyleSheet(UIConfig.MAIN_STYLE)
        
        # Install delegates for special editing
        self._install_delegates()
        
        # Set initial column visibility - show all 14 columns
        self.show_all_columns()
        
    def resizeEvent(self, event):
        """Handle window resize by updating column visibility."""
        super().resizeEvent(event)
        self.update_column_visibility()
        
    def update_column_visibility(self):
        """Show/hide columns based on available width and priority."""
        available_width = self.viewport().width()
        new_visible_columns = self._calculate_visible_columns(available_width)
        
        if new_visible_columns != self.visible_columns:
            self.visible_columns = new_visible_columns
            self._apply_column_visibility()
            self.columnsChanged.emit()
    
    def _calculate_visible_columns(self, available_width: int) -> Set[int]:
        """Determine which columns should be visible based on width."""
        visible = set()
        used_width = 0
        
        # Priority order for showing columns
        priority_order = (
            UIConfig.COLUMN_PRIORITIES['essential'] +
            UIConfig.COLUMN_PRIORITIES['important'] +
            UIConfig.COLUMN_PRIORITIES['optional']
        )
        
        for header in priority_order:
            try:
                col_idx = TableConfig.get_column_index(header)
                col_width = TableConfig.COLUMN_WIDTHS[col_idx]
                
                if used_width + col_width + 50 <= available_width:  # 50px buffer
                    visible.add(col_idx)
                    used_width += col_width
                else:
                    break
                    
            except (ValueError, IndexError):
                continue
                
        # Always show at least essential columns, even if cramped
        if len(visible) < len(UIConfig.COLUMN_PRIORITIES['essential']):
            for header in UIConfig.COLUMN_PRIORITIES['essential']:
                try:
                    col_idx = TableConfig.get_column_index(header)
                    visible.add(col_idx)
                except (ValueError, IndexError):
                    continue
                    
        return visible
    
    def _apply_column_visibility(self):
        """Apply the calculated column visibility to the table."""
        for col_idx in range(self.columnCount()):
            if col_idx in self.visible_columns:
                self.showColumn(col_idx)
                # Set responsive width
                if col_idx < len(TableConfig.COLUMN_WIDTHS):
                    self.setColumnWidth(col_idx, TableConfig.COLUMN_WIDTHS[col_idx])
            else:
                self.hideColumn(col_idx)
                
        # Stretch the last visible column if needed
        if self.visible_columns:
            last_visible = max(self.visible_columns)
            header = self.horizontalHeader()
            header.setSectionResizeMode(last_visible, QHeaderView.Stretch)
    
    def get_hidden_columns(self) -> List[str]:
        """Get list of currently hidden column names."""
        hidden = []
        for col_idx in range(self.columnCount()):
            if col_idx not in self.visible_columns:
                if col_idx < len(TableConfig.HEADERS):
                    hidden.append(TableConfig.HEADERS[col_idx])
        return hidden
    
    def toggle_column_visibility(self, header_name: str, visible: bool = None):
        """Manually toggle column visibility."""
        try:
            col_idx = TableConfig.get_column_index(header_name)
            
            if visible is None:
                # Toggle current state
                if col_idx in self.visible_columns:
                    self.visible_columns.discard(col_idx)
                else:
                    self.visible_columns.add(col_idx)
            elif visible:
                self.visible_columns.add(col_idx)
            else:
                self.visible_columns.discard(col_idx)
                
            self._apply_column_visibility()
            self.columnsChanged.emit()
            
        except ValueError:
            print(f"Warning: Column '{header_name}' not found")
    
    def show_all_columns(self):
        """Show all available columns."""
        self.visible_columns = set(range(self.columnCount()))
        self._apply_column_visibility()
        self.columnsChanged.emit()
    
    def reset_to_responsive_view(self):
        """Reset to automatically calculated responsive view."""
        self.update_column_visibility()
        
    def _install_delegates(self):
        """Install custom delegates for special column editing."""
        from app.dialogs import DateDelegate, HoursDelegate, ComboDelegate
        
        col_map = {h: i for i, h in enumerate(TableConfig.HEADERS)}
        
        # Date delegate
        if "Date" in col_map:
            self.setItemDelegateForColumn(
                col_map["Date"], DateDelegate(self)
            )
            
        # Type delegate
        if "Type" in col_map:
            self.setItemDelegateForColumn(
                col_map["Type"],
                ComboDelegate(
                    lambda: ["Exercise", "Project"], 
                    parent=self
                ),
            )
            
        # Status delegate
        if "Status" in col_map:
            self.setItemDelegateForColumn(
                col_map["Status"],
                ComboDelegate(
                    lambda: ["Planned", "In Progress", "Completed", "Blocked"], 
                    parent=self
                ),
            )
            
        # Hours delegate
        if "Hours" in col_map:
            self.setItemDelegateForColumn(
                col_map["Hours"], HoursDelegate(self)
            )
            
        # Language delegate
        if "Language" in col_map:
            self.setItemDelegateForColumn(
                col_map["Language"],
                ComboDelegate(
                    lambda: self._get_language_names(), 
                    parent=self
                ),
            )
            
        # Difficulty delegate
        if "Difficulty" in col_map:
            self.setItemDelegateForColumn(
                col_map["Difficulty"],
                ComboDelegate(
                    lambda: ["Beginner", "Intermediate", "Advanced", "Expert"], 
                    parent=self
                ),
            )
            
        # Target Time delegate
        if "Target Time" in col_map:
            self.setItemDelegateForColumn(
                col_map["Target Time"], HoursDelegate(self)
            )
    
    def _get_language_names(self) -> List[str]:
        """Get list of language names for delegate."""
        # This will be populated by the main window
        return []
