# app/dashboard_window.py
"""
Full-screen dashboard window with maximized layout,
all 14 columns visible, proportional widths, filter row,
and compact two-row form.
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QMessageBox, QFileDialog,
    QSplitter, QFrame, QStatusBar, QMenuBar, QMenu,
    QCheckBox, QDialog, QDialogButtonBox, QComboBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction

from app.widgets import DashboardTable, CompactForm
from app.services.session_service import SessionService
from app.services.language_service import LanguageService
from app.services.ui_state_service import UIStateService
from app.config.ui_config import UIConfig
from app.config.table_config import TableConfig


class DashboardWindow(QMainWindow):
    """
    Full-screen dashboard with all 14 columns always visible,
    proportional column widths, filter row, and compact form.
    """
    
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("Smart Learning Tracker - Dashboard")
        
        # Launch just under fullscreen
        self.resize(1400, 820)
        self.setMinimumSize(1800, 700)
        
        # Center window on screen
        screen = self.screen().availableGeometry()
        window_size = self.frameGeometry()
        x = (screen.width() - window_size.width()) // 2
        y = (screen.height() - window_size.height()) // 2
        self.move(x, y)
        
        self.show()
        
        # Services
        self.session_service = SessionService()
        self.language_service = LanguageService()
        self.ui_state_service = UIStateService()
        
        # UI State
        self.editing_session_id: Optional[int] = None
        
        # Apply dark theme
        self.setStyleSheet(UIConfig.MAIN_STYLE)
        
        # Build interface
        self._create_menu_bar()
        self._create_toolbar()
        self._create_status_bar()
        self._build_dashboard()
        
        # Load initial data
        self._load_languages()
        self.reload_table()
    
    def _create_menu_bar(self):
        """Create menu bar with essential functions."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        export_action = QAction("Export CSV", self)
        export_action.setShortcut("Ctrl+E")
        export_action.triggered.connect(self.export_csv)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        quit_action = QAction("Exit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        clear_filters_action = QAction("Clear All Filters", self)
        clear_filters_action.setShortcut("Ctrl+R")
        clear_filters_action.triggered.connect(self._clear_filters)
        view_menu.addAction(clear_filters_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        
        refresh_action = QAction("Refresh Data", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self.reload_table)
        tools_menu.addAction(refresh_action)
    
    def _create_toolbar(self):
        """Create always-visible toolbar."""
        # Create toolbar frame
        self.toolbar = QFrame()
        self.toolbar.setFrameStyle(QFrame.StyledPanel)
        self.toolbar.setFixedHeight(50)
        self.toolbar.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border-bottom: 2px solid #475569;
                padding: 6px 12px;
            }
        """)
        
        toolbar_layout = QHBoxLayout(self.toolbar)
        toolbar_layout.setContentsMargins(12, 8, 12, 8)
        toolbar_layout.setSpacing(12)
        
        # Primary actions
        self.add_btn = QPushButton("➕ Add Entry")
        self.add_btn.setProperty("variant", "primary")
        self.add_btn.setFixedHeight(32)
        self.add_btn.clicked.connect(self.add_entry)
        
        self.save_btn = QPushButton("💾 Save Entry")
        self.save_btn.setFixedHeight(32)
        self.save_btn.clicked.connect(self.save_entry)
        self.save_btn.setEnabled(False)
        
        self.cancel_btn = QPushButton("❌ Cancel")
        self.cancel_btn.setFixedHeight(32)
        self.cancel_btn.clicked.connect(self.cancel_edit)
        self.cancel_btn.setVisible(False)
        
        # Secondary actions
        self.delete_btn = QPushButton("🗑️ Delete")
        self.delete_btn.setProperty("variant", "danger")
        self.delete_btn.setFixedHeight(32)
        self.delete_btn.clicked.connect(self.delete_entry)
        self.delete_btn.setEnabled(False)
        
        # Filter controls
        self.clear_filters_btn = QPushButton("🔍 Clear Filters")
        self.clear_filters_btn.setFixedHeight(32)
        self.clear_filters_btn.clicked.connect(self._clear_filters)
        
        # Layout buttons
        toolbar_layout.addWidget(self.add_btn)
        toolbar_layout.addWidget(self.save_btn)
        toolbar_layout.addWidget(self.cancel_btn)
        toolbar_layout.addWidget(QWidget())  # Spacer
        toolbar_layout.addWidget(self.clear_filters_btn)
        toolbar_layout.addWidget(QWidget())  # Spacer
        toolbar_layout.addWidget(self.delete_btn)
        
    def _create_status_bar(self):
        """Create informative status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Status labels
        self.records_label = QLabel("📊 Records: 0")
        self.filtered_label = QLabel("")
        self.selected_label = QLabel("")
        
        self.status_bar.addWidget(self.records_label)
        self.status_bar.addPermanentWidget(self.filtered_label)
        self.status_bar.addPermanentWidget(self.selected_label)
    
    def _build_dashboard(self):
        """Build the main dashboard layout."""
        # Create main widget
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Add toolbar
        main_layout.addWidget(self.toolbar)
        
        # Create splitter for table and form with fixed proportions
        splitter = QSplitter(Qt.Vertical)
        splitter.setChildrenCollapsible(False)  # Prevent collapse
        
        # Top section: Dashboard table (takes ~75% of space)
        self.table = DashboardTable()
        self.table.selectionChanged.connect(self._on_selection_changed)
        self.table.cellChanged.connect(self._on_cell_changed)
        splitter.addWidget(self.table)
        
        # Bottom section: Compact form (takes ~25% of space)  
        self.form = CompactForm()
        self.form.dataChanged.connect(self._on_form_data_changed)
        splitter.addWidget(self.form)
        
        # Set fixed proportions: 75% table, 25% form
        splitter.setSizes([750, 250])  # Proportional sizes
        splitter.setStretchFactor(0, 3)  # Table gets 3x stretch
        splitter.setStretchFactor(1, 1)  # Form gets 1x stretch
        
        main_layout.addWidget(splitter, 1)
        self.setCentralWidget(main_widget)
    
    def _load_languages(self):
        """Load languages into form and table filters."""
        try:
            languages = self.language_service.get_languages()
            self.form.load_languages(languages)
            
            # Update table filter dropdown with languages
            if hasattr(self.table, 'filter_row') and self.table.filter_row:
                language_filter = self.table.filter_row.filters.get('Language')
                if isinstance(language_filter, QComboBox):
                    current_text = language_filter.currentText()
                    language_filter.clear()
                    language_filter.addItem("")  # Empty = no filter
                    for code, name, _color in languages:
                        language_filter.addItem(name)
                    # Restore selection if it still exists
                    index = language_filter.findText(current_text)
                    if index >= 0:
                        language_filter.setCurrentIndex(index)
            
        except Exception as e:
            self._show_error("Loading Languages", f"Failed to load languages: {e}")
    
    def _on_selection_changed(self):
        """Handle table row selection."""
        row_data = self.table.get_selected_row_data()
        
        if row_data:
            self.delete_btn.setEnabled(True)
            session_id = row_data.get("id", "")
            self.selected_label.setText(f"✏️ Selected: Session #{session_id}")
            
            # Auto-populate form for editing
            self.form.set_form_data(row_data)
            self.editing_session_id = int(session_id) if session_id else None
            
        else:
            self.delete_btn.setEnabled(False)
            self.selected_label.setText("")
            self.editing_session_id = None
    
    def _on_cell_changed(self, row: int, col: int):
        """Handle inline table edits."""
        try:
            # Get the edited row data
            row_data = self.table.get_selected_row_data()
            if not row_data:
                return
            
            # Validate that we have a valid session ID
            session_id = row_data.get("id")
            if not session_id:
                return
                
            # Convert row data to session format
            session_data = {
                "id": int(session_id),
                "date": row_data.get("date", ""),
                "status": row_data.get("status", "In Progress"),
                "hours_spent": float(row_data.get("hours_spent", 0)) if row_data.get("hours_spent") else 0.0,
                "notes": row_data.get("notes", ""),
                "tags": row_data.get("tags", ""),
                "difficulty": row_data.get("difficulty", "Beginner"),
                "topic": row_data.get("topic", ""),
                "item_id": row_data.get("item_id", 0)  # Will be resolved by service
            }
            
            # Save the updated session
            self.session_service.save_session(session_data, editing_session_id=int(session_id))
            
            # Reload the table to show updated computed values
            self.reload_table()
            
        except Exception as e:
            self._show_error("Edit Error", f"Failed to save inline edit: {e}")
            # Reload table to revert changes
            self.reload_table()
    
    def _on_form_data_changed(self):
        """Handle form data changes."""
        self.save_btn.setEnabled(True)
    
    def _clear_filters(self):
        """Clear all table filters."""
        self.table.clear_filters()
        self.filtered_label.setText("")
    
    def add_entry(self):
        """Start adding new entry."""
        self.editing_session_id = None
        self.form.clear_form()
        self.cancel_btn.setVisible(True)
        self.add_btn.setEnabled(False)
        self.form.update_status_display("🆕 Ready to add new learning session")
        self.form.focus_first_field()
    
    def save_entry(self):
        """Save the current entry."""
        try:
            form_data = self.form.get_form_data()
            
            # Validate required fields
            is_valid, error_message = self.form.validate_required_fields()
            if not is_valid:
                self._show_error("Validation Error", error_message)
                return
                
            # Find or create work item
            item_id, suggestions = self.session_service.find_or_create_item(
                form_data.get("language_code", ""), 
                form_data.get("type", ""), 
                form_data.get("canonical_name", "")
            )
            
            # Add item_id to session data
            form_data["item_id"] = item_id
            
            # Save session
            self.session_service.save_session(
                form_data, editing_session_id=self.editing_session_id
            )
            
            # Reset form and reload
            self.form.clear_form()
            self.reload_table()
            self._reset_form_state()
            
            self.form.update_status_display("✅ Entry saved successfully!")
            QTimer.singleShot(3000, lambda: self.form.update_status_display(""))
            
        except Exception as e:
            self._show_error("Save Error", f"Failed to save entry: {e}")
    
    def cancel_edit(self):
        """Cancel current editing operation."""
        self.form.clear_form()
        self._reset_form_state()
        self.form.update_status_display("")
    
    def delete_entry(self):
        """Delete selected entry."""
        row_data = self.table.get_selected_row_data()
        if not row_data:
            return
            
        # Confirm deletion
        reply = QMessageBox.question(
            self, "Confirm Deletion", 
            "Are you sure you want to delete this learning session?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                session_id = int(row_data.get("id", 0))
                if session_id:
                    self.session_service.delete_session(session_id)
                    self.reload_table()
                    self.form.update_status_display("🗑️ Entry deleted")
                    QTimer.singleShot(2000, lambda: self.form.update_status_display(""))
                    
            except Exception as e:
                self._show_error("Delete Error", f"Failed to delete entry: {e}")
    
    def export_csv(self):
        """Export data to CSV."""
        try:
            filename, _ = QFileDialog.getSaveFileName(
                self, "Export CSV", "learning_data.csv", "CSV Files (*.csv)"
            )
            if filename:
                self.session_service.export_csv(filename)
                self.form.update_status_display(f"📁 Data exported to {filename}")
                QTimer.singleShot(3000, lambda: self.form.update_status_display(""))
                
        except Exception as e:
            self._show_error("Export Error", f"Failed to export data: {e}")
    
    def reload_table(self):
        """Reload table data."""
        try:
            # Get sessions data
            sessions = self.session_service.get_sessions()
            
            # Convert to proper format for dashboard table
            table_data = []
            for session_tuple in sessions:
                session_data = {
                    "id": session_tuple[0],
                    "date": session_tuple[1],
                    "type": session_tuple[3],
                    "canonical_name": session_tuple[4],
                    "notes": session_tuple[7],
                    "status": session_tuple[5], 
                    "hours_spent": session_tuple[6],
                    "tags": session_tuple[8],
                    "language_code": session_tuple[2],
                    "difficulty": session_tuple[9],
                    "topic": session_tuple[10],
                    "points_awarded": session_tuple[11],
                    "progress_pct": session_tuple[12],
                    "target_hours": session_tuple[14] if len(session_tuple) > 14 else 0,
                }
                table_data.append(session_data)
            
            # Load into table
            self.table.load_data(table_data)
            
            # Update status
            self.records_label.setText(f"📊 Records: {len(table_data)}")
            
        except Exception as e:
            self._show_error("Load Error", f"Failed to load data: {e}")
    
    def _reset_form_state(self):
        """Reset form to default state."""
        self.editing_session_id = None
        self.cancel_btn.setVisible(False)
        self.add_btn.setEnabled(True)
        self.save_btn.setEnabled(False)
    
    def _show_error(self, title: str, message: str):
        """Show error dialog."""
        QMessageBox.critical(self, title, message)
    
    def closeEvent(self, event):
        """Handle window close event."""
        # Check if there are unsaved changes in the form
        if self.save_btn.isEnabled():
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                "You have unsaved changes in the form. Do you want to save them before closing?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            
            if reply == QMessageBox.Save:
                self.save_entry()
                event.accept()
            elif reply == QMessageBox.Discard:
                event.accept()
            else:  # Cancel
                event.ignore()
                return
        
        event.accept()
