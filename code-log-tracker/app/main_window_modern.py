# app/main_window_modern.py
"""
Modern MainWindow with responsive design and improved UX.
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QMessageBox, QFileDialog,
    QSplitter, QGroupBox, QMenuBar, QMenu, QCheckBox,
    QStatusBar, QFrame
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction

from app.widgets import ResponsiveTable, FixedForm
from app.services.session_service import SessionService
from app.services.language_service import LanguageService
from app.services.ui_state_service import UIStateService
from app.config.ui_config import UIConfig
from app.config.table_config import TableConfig


class ModernMainWindow(QMainWindow):
    """Modern main window with responsive design and improved UX."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Learning Tracker")
        self.resize(UIConfig.WINDOW_SIZE)
        self.setMinimumSize(UIConfig.MIN_WINDOW_SIZE)
        
        # Services
        self.session_service = SessionService()
        self.language_service = LanguageService()
        self.ui_state_service = UIStateService()
        
        # UI State
        self.reloading = False
        self.editing_session_id: Optional[int] = None
        
        # Apply modern styling
        self.setStyleSheet(UIConfig.MAIN_STYLE)
        
        # Build UI
        self._create_menu_bar()
        self._create_status_bar()
        self._build_ui()
        
        # Load initial data
        self._load_languages()
        self.reload_table()
        
        # Auto-save timer
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self._auto_save_check)
        self.auto_save_timer.start(30000)  # 30 seconds
        
    def _create_menu_bar(self):
        """Create modern menu bar."""
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
        
        toggle_columns_action = QAction("Column Visibility", self)
        toggle_columns_action.triggered.connect(self._show_column_visibility_dialog)
        view_menu.addAction(toggle_columns_action)
        
        reset_layout_action = QAction("Reset Layout", self)
        reset_layout_action.triggered.connect(self._reset_layout)
        view_menu.addAction(reset_layout_action)
        
    def _create_status_bar(self):
        """Create status bar with useful information."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Status labels
        self.records_label = QLabel("Records: 0")
        self.selected_label = QLabel("")
        self.columns_label = QLabel("")
        
        self.status_bar.addWidget(self.records_label)
        self.status_bar.addPermanentWidget(self.selected_label)
        self.status_bar.addPermanentWidget(self.columns_label)
        
    def _build_ui(self):
        """Build the main UI with responsive components."""
        # Create splitter for resizable layout
        main_splitter = QSplitter(Qt.Vertical)
        
        # Top section: Table and controls
        top_widget = self._create_top_section()
        main_splitter.addWidget(top_widget)
        
        # Bottom section: Fixed Form (non-scrollable)
        self.form = FixedForm()
        self.form.dataChanged.connect(self._on_form_data_changed)
        main_splitter.addWidget(self.form)
        
        # Set splitter proportions (70% table, 30% form)
        main_splitter.setSizes([700, 300])
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 0)
        
        self.setCentralWidget(main_splitter)
        
    def _create_top_section(self) -> QWidget:
        """Create the top section with table and toolbar."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Toolbar
        toolbar = self._create_modern_toolbar()
        layout.addWidget(toolbar)
        
        # Table
        self.table = ResponsiveTable()
        self.table.columnsChanged.connect(self._update_columns_status)
        layout.addWidget(self.table, 1)
        
        # Connect table signals
        self.table.itemSelectionChanged.connect(self._on_selection_changed)
        
        return widget
        
    def _create_modern_toolbar(self) -> QWidget:
        """Create modern toolbar with styled buttons."""
        toolbar = QFrame()
        toolbar.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        toolbar.setStyleSheet("""
            QFrame {
                background-color: #1e293b;
                border: 1px solid #475569;
                border-radius: 12px;
                padding: 12px;
                margin-bottom: 12px;
            }
        """)
        
        layout = QHBoxLayout(toolbar)
        layout.setContentsMargins(12, 8, 12, 8)
        
        # Primary actions
        self.add_btn = QPushButton("Add Entry")
        self.add_btn.setProperty("variant", "primary")
        self.add_btn.clicked.connect(self.add_entry)
        
        self.save_btn = QPushButton("Save Entry")  
        self.save_btn.clicked.connect(self.save_entry)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.cancel_edit)
        self.cancel_btn.hide()  # Hidden by default
        
        # Secondary actions
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setProperty("variant", "danger")
        self.delete_btn.clicked.connect(self.delete_entry)
        self.delete_btn.setEnabled(False)
        
        # Layout buttons
        layout.addWidget(self.add_btn)
        layout.addWidget(self.save_btn)
        layout.addWidget(self.cancel_btn)
        layout.addStretch()
        layout.addWidget(self.delete_btn)
        
        return toolbar
        
    def _show_column_visibility_dialog(self):
        """Show dialog to toggle column visibility."""
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Column Visibility")
        dialog.resize(300, 400)
        
        layout = QVBoxLayout(dialog)
        
        # Create checkboxes for each column
        checkboxes = {}
        visible_columns = self.table.visible_columns
        
        for i, header in enumerate(TableConfig.HEADERS):
            if header not in UIConfig.COLUMN_PRIORITIES['hidden']:
                checkbox = QCheckBox(header)
                checkbox.setChecked(i in visible_columns)
                layout.addWidget(checkbox)
                checkboxes[header] = checkbox
        
        # Dialog buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        if dialog.exec() == QDialog.Accepted:
            # Apply visibility changes
            for header, checkbox in checkboxes.items():
                self.table.toggle_column_visibility(header, checkbox.isChecked())
                
    def _reset_layout(self):
        """Reset to responsive layout."""
        self.table.reset_to_responsive_view()
        
    def _load_languages(self):
        """Load languages into the form."""
        try:
            languages = self.language_service.get_languages()
            self.form.load_languages(languages)
        except Exception as e:
            self._show_error("Loading Languages", f"Failed to load languages: {e}")
            
    def _on_form_data_changed(self):
        """Handle form data changes."""
        if not self.reloading:
            self.save_btn.setEnabled(True)
            
    def _on_selection_changed(self):
        """Handle table selection changes."""
        selected_rows = self.table.selectionModel().selectedRows()
        
        if selected_rows:
            self.delete_btn.setEnabled(True)
            row = selected_rows[0].row()
            
            # Get session data for editing
            session_data = {}
            for col_idx, key in enumerate(TableConfig.KEYS):
                item = self.table.item(row, col_idx)
                if item:
                    session_data[key] = item.text()
            
            # Update status and populate form for editing
            session_id = session_data.get("id", "")
            self.selected_label.setText(f"✏️ Selected: Session #{session_id}")
            
            # Auto-populate form for editing
            self.form.set_form_data(session_data)
            self.editing_session_id = int(session_id) if session_id else None
            
        else:
            self.delete_btn.setEnabled(False)
            self.selected_label.setText("")
            self.editing_session_id = None
            
    def _update_columns_status(self):
        """Update status bar with column information."""
        visible_count = len(self.table.visible_columns)
        total_count = self.table.columnCount()
        hidden_columns = self.table.get_hidden_columns()
        
        status_text = f"Columns: {visible_count}/{total_count} visible"
        if hidden_columns:
            status_text += f" (Hidden: {', '.join(hidden_columns[:3])}"
            if len(hidden_columns) > 3:
                status_text += f" +{len(hidden_columns)-3} more"
            status_text += ")"
            
        self.columns_label.setText(status_text)
        
    def _auto_save_check(self):
        """Check if form needs auto-saving."""
        # Implement auto-save logic if needed
        pass
        
    def add_entry(self):
        """Add new entry mode."""
        self.editing_session_id = None
        self.form.clear_form()
        self.cancel_btn.show()
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
                
            # Find or create the work item first
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
        """Cancel current edit operation."""
        self.form.clear_form()
        self._reset_form_state()
        self.form.update_status_display("")
        
    def delete_entry(self):
        """Delete selected entry."""
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            return
            
        # Confirm deletion
        reply = QMessageBox.question(
            self, "Confirm Deletion", 
            "Are you sure you want to delete this entry?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                row = selected_rows[0].row()
                item = self.table.item(row, 0)
                if item:
                    session_id = int(item.text())
                    self.session_service.delete_session(session_id)
                    self.reload_table()
                    
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
                
        except Exception as e:
            self._show_error("Export Error", f"Failed to export data: {e}")
            
    def reload_table(self):
        """Reload table data."""
        try:
            self.reloading = True
            
            # Get sessions data
            sessions = self.session_service.get_sessions()
            
            # Update table
            self.table.setRowCount(len(sessions))
            
            # Map database query results to new table column order
            # Query returns: (id, date, language_code, type, canonical_name, status, hours_spent, notes, tags, difficulty, topic, points_awarded, progress_pct, item_id, target_hours)
            # New table order: ["id", "date", "type", "canonical_name", "notes", "status", "hours_spent", "tags", "language_code", "difficulty", "topic", "points_awarded", "progress_pct", "target_hours"]
            
            for row_idx, session_tuple in enumerate(sessions):
                # Convert tuple to dictionary matching new table structure
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
                
                for col_idx, key in enumerate(TableConfig.KEYS):
                    value = session_data.get(key, "")
                    if isinstance(value, (int, float)) and key != "id":
                        if key == "progress_pct":
                            value = f"{value:.1f}%" if value else "0.0%"
                        elif key in ["hours_spent", "points_awarded"]:
                            value = f"{value:.2f}" if value else "0.00"
                    
                    item = self.table.item(row_idx, col_idx)
                    if not item:
                        from PySide6.QtWidgets import QTableWidgetItem
                        item = QTableWidgetItem()
                        self.table.setItem(row_idx, col_idx, item)
                    
                    item.setText(str(value))
                    
            # Update status
            self.records_label.setText(f"📊 Records: {len(sessions)}")
            
        except Exception as e:
            self._show_error("Load Error", f"Failed to load data: {e}")
        finally:
            self.reloading = False
            
    def _reset_form_state(self):
        """Reset form to default state."""
        self.editing_session_id = None
        self.cancel_btn.hide()
        self.add_btn.setEnabled(True)
        self.save_btn.setEnabled(False)
        
    def _show_error(self, title: str, message: str):
        """Show error dialog."""
        QMessageBox.critical(self, title, message)
