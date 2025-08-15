# app/main_window.py
"""
MainWindow for Smart Learning Tracker - UI Layer Only.

Responsibilities:
- Build table + input form UI components
- Handle user interactions and events
- Display data received from business layer
- Delegate business operations to services
"""

from __future__ import annotations

from typing import Dict, Any, List, Optional

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QComboBox,
    QDoubleSpinBox,
    QLineEdit,
    QMessageBox,
    QFileDialog,
    QDateEdit,
    QAbstractItemView,
    QHeaderView,
    QGroupBox,
)
from PySide6.QtCore import Qt, QDate

from app.dialogs import (
    SuggestionDialog,
    TargetTimeDialog,
    DateDelegate,
    HoursDelegate,
    ComboDelegate,
)
from app.services.session_service import SessionService
from app.services.language_service import LanguageService
from app.services.ui_state_service import UIStateService
from app.config.table_config import TableConfig


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Learning Tracker")
        self.resize(1400, 800)

        # Services
        self.session_service = SessionService()
        self.language_service = LanguageService()
        self.ui_state_service = UIStateService()
        
        # UI State
        self.reloading = False
        self.updating_template = False
        self.editing_session_id: Optional[int] = None

        self._build_ui()
        self.reload_table()

    # ===== UI Construction =====
    def _build_ui(self):
        """Build the complete UI layout."""
        self._build_table()
        self._build_toolbar()
        self._build_input_form()
        self._setup_layout()

    def _build_table(self):
        """Create and configure the main data table."""
        self.table = QTableWidget(0, len(TableConfig.HEADERS))
        self.table.setHorizontalHeaderLabels(TableConfig.HEADERS)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setWordWrap(False)
        self.table.setEditTriggers(
            QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked
        )
        self.table.setStyleSheet(
            """
            QTableWidget::item:selected { background: #dbeafe; color: black; }
            QTableWidget { gridline-color: #e5e7eb; selection-background-color: #dbeafe; }
            """
        )

        # Configure column widths
        hdr = self.table.horizontalHeader()
        hdr.setSectionResizeMode(QHeaderView.Interactive)
        hdr.setStretchLastSection(True)
        for i, width in enumerate(TableConfig.COLUMN_WIDTHS):
            hdr.resizeSection(i, width)

        # Install delegates for special editing
        self._install_delegates()
        
        # Connect signals
        self.table.itemChanged.connect(self.on_cell_changed)

    def _install_delegates(self):
        """Install custom delegates for special column editing."""
        col_map = {h: i for i, h in enumerate(TableConfig.HEADERS)}
        
        if "Date" in col_map:
            self.table.setItemDelegateForColumn(
                col_map["Date"], DateDelegate(self.table)
            )
        if "Status" in col_map:
            self.table.setItemDelegateForColumn(
                col_map["Status"],
                ComboDelegate(
                    lambda: ["Planned", "In Progress", "Completed", "Blocked"], 
                    parent=self.table
                ),
            )
        if "Difficulty" in col_map:
            self.table.setItemDelegateForColumn(
                col_map["Difficulty"],
                ComboDelegate(
                    lambda: ["Beginner", "Intermediate", "Advanced", "Expert"], 
                    parent=self.table
                ),
            )
        if "Hours" in col_map:
            self.table.setItemDelegateForColumn(
                col_map["Hours"], HoursDelegate(self.table)
            )

    def _build_toolbar(self):
        """Create the toolbar with action buttons."""
        self.toolbar_layout = QHBoxLayout()

        # Create buttons
        self.add_btn = QPushButton("Add Entry")
        self.save_btn = QPushButton("Save Entry")
        self.del_btn = QPushButton("Delete Entry")
        self.export_btn = QPushButton("Export CSV")

        # Style buttons
        button_style = """
            QPushButton { 
                padding: 8px 16px; 
                font-weight: bold; 
                border-radius: 4px; 
            }
            QPushButton:hover { 
                background-color: #f0f9ff; 
            }
        """
        for btn in (self.add_btn, self.save_btn, self.del_btn, self.export_btn):
            btn.setStyleSheet(button_style)

        # Connect signals
        self.add_btn.clicked.connect(self.add_entry)
        self.save_btn.clicked.connect(self.save_entry)
        self.del_btn.clicked.connect(self.delete_entry)
        self.export_btn.clicked.connect(self.export_csv)

        # Layout buttons
        self.toolbar_layout.addWidget(self.add_btn)
        self.toolbar_layout.addWidget(self.save_btn)
        self.toolbar_layout.addWidget(self.del_btn)
        self.toolbar_layout.addStretch()
        self.toolbar_layout.addWidget(self.export_btn)

    def _build_input_form(self):
        """Create the input form for new entries."""
        self.input_group = QGroupBox("Add New Learning Entry")
        form_layout = QVBoxLayout()

        # Create input rows
        row1 = self._create_input_row1()
        row2 = self._create_input_row2()
        
        form_layout.addLayout(row1)
        form_layout.addLayout(row2)

        # Status label
        self.status_label = QLabel("")
        self.status_label.setStyleSheet(
            "color: #666; font-style: italic; padding: 4px;"
        )
        form_layout.addWidget(self.status_label)

        self.input_group.setLayout(form_layout)

    def _create_input_row1(self) -> QHBoxLayout:
        """Create the first row of input fields."""
        row = QHBoxLayout()
        self.inputs: Dict[str, Any] = {}

        # Date input
        date_layout = QVBoxLayout()
        date_layout.addWidget(QLabel("Date *"))
        self.inputs["date"] = QDateEdit()
        self.inputs["date"].setCalendarPopup(True)
        self.inputs["date"].setDate(QDate.currentDate())
        self.inputs["date"].setMinimumWidth(120)
        date_layout.addWidget(self.inputs["date"])
        row.addLayout(date_layout)

        # Language input
        lang_layout = QVBoxLayout()
        lang_layout.addWidget(QLabel("Language *"))
        self.inputs["language"] = QComboBox()
        self.inputs["language"].setMinimumWidth(160)
        self._load_languages()
        self.inputs["language"].currentTextChanged.connect(self.on_language_changed)
        lang_layout.addWidget(self.inputs["language"])
        row.addLayout(lang_layout)

        # Type input
        type_layout = QVBoxLayout()
        type_layout.addWidget(QLabel("Type *"))
        self.inputs["type"] = QComboBox()
        self.inputs["type"].addItems(["", "Exercise", "Project"])
        self.inputs["type"].setMinimumWidth(110)
        type_layout.addWidget(self.inputs["type"])
        row.addLayout(type_layout)

        # Work Item input
        item_layout = QVBoxLayout()
        item_layout.addWidget(QLabel("Work Item Name *"))
        self.inputs["work_item"] = QComboBox()
        self.inputs["work_item"].setEditable(True)
        self.inputs["work_item"].setMinimumWidth(280)
        self.inputs["work_item"].lineEdit().textChanged.connect(self.on_work_item_changed)
        item_layout.addWidget(self.inputs["work_item"])
        row.addLayout(item_layout)

        # Hours input
        hours_layout = QVBoxLayout()
        hours_layout.addWidget(QLabel("Hours *"))
        self.inputs["hours"] = QDoubleSpinBox()
        self.inputs["hours"].setRange(0, 24)
        self.inputs["hours"].setSingleStep(0.25)
        self.inputs["hours"].setDecimals(2)
        self.inputs["hours"].setMinimumWidth(90)
        hours_layout.addWidget(self.inputs["hours"])
        row.addLayout(hours_layout)

        return row

    def _create_input_row2(self) -> QHBoxLayout:
        """Create the second row of input fields."""
        row = QHBoxLayout()

        # Status input
        status_layout = QVBoxLayout()
        status_layout.addWidget(QLabel("Status"))
        self.inputs["status"] = QComboBox()
        self.inputs["status"].addItems(["", "Planned", "In Progress", "Completed", "Blocked"])
        self.inputs["status"].setCurrentText("In Progress")
        self.inputs["status"].setMinimumWidth(140)
        status_layout.addWidget(self.inputs["status"])
        row.addLayout(status_layout)

        # Difficulty input
        diff_layout = QVBoxLayout()
        diff_layout.addWidget(QLabel("Difficulty"))
        self.inputs["difficulty"] = QComboBox()
        self.inputs["difficulty"].addItems(["", "Beginner", "Intermediate", "Advanced", "Expert"])
        self.inputs["difficulty"].setMinimumWidth(140)
        diff_layout.addWidget(self.inputs["difficulty"])
        row.addLayout(diff_layout)

        # Topic input
        topic_layout = QVBoxLayout()
        topic_layout.addWidget(QLabel("Topic"))
        self.inputs["topic"] = QComboBox()
        self.inputs["topic"].setEditable(True)
        self.inputs["topic"].setMinimumWidth(180)
        topic_layout.addWidget(self.inputs["topic"])
        row.addLayout(topic_layout)

        # Notes input
        notes_layout = QVBoxLayout()
        notes_layout.addWidget(QLabel("Notes"))
        self.inputs["notes"] = QLineEdit()
        self.inputs["notes"].setPlaceholderText("What did you do?")
        self.inputs["notes"].setMinimumWidth(260)
        self.inputs["notes"].textChanged.connect(self.auto_fill_from_text)
        notes_layout.addWidget(self.inputs["notes"])
        row.addLayout(notes_layout)

        # Tags input
        tags_layout = QVBoxLayout()
        tags_layout.addWidget(QLabel("Tags"))
        self.inputs["tags"] = QLineEdit()
        self.inputs["tags"].setPlaceholderText("comma, separated, tags")
        self.inputs["tags"].setMinimumWidth(180)
        tags_layout.addWidget(self.inputs["tags"])
        row.addLayout(tags_layout)

        return row

    def _setup_layout(self):
        """Setup the main window layout."""
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.toolbar_layout)
        main_layout.addWidget(self.table, 1)
        main_layout.addWidget(self.input_group)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    # ===== Event Handlers =====
    def _load_languages(self):
        """Load available languages into the combo box."""
        try:
            languages = self.language_service.get_languages()
            self.inputs["language"].clear()
            self.inputs["language"].addItem("")
            
            for code, name, _color in languages:
                self.inputs["language"].addItem(name, code)
        except Exception as e:
            self._show_error("Loading Languages", f"Failed to load languages: {e}")

    def on_language_changed(self):
        """Handle language selection change."""
        if self.updating_template:
            return
            
        language_code = self.inputs["language"].currentData()
        if not language_code:
            return
            
        try:
            self.language_service.load_language_pack(language_code)
            self._update_topic_suggestions()
            self._update_work_item_suggestions()
        except Exception as e:
            print(f"Warning: Failed to load language pack: {e}")

    def _update_topic_suggestions(self):
        """Update topic combo box with language-specific suggestions."""
        topics = self.language_service.get_topics()
        self.inputs["topic"].clear()
        self.inputs["topic"].addItem("")
        if topics:
            self.inputs["topic"].addItems(topics)

    def _update_work_item_suggestions(self):
        """Update work item suggestions based on language and type."""
        language_code = self.inputs["language"].currentData()
        item_type = self.inputs["type"].currentText().strip()
        
        if not language_code or not item_type:
            return
            
        try:
            items = self.session_service.search_items(language_code, item_type, limit=20)
            self.inputs["work_item"].clear()
            self.inputs["work_item"].addItem("")
            
            for item in items:
                display_text = item['name']
                if item.get("total_hours", 0) > 0:
                    display_text += f" ({item['total_hours']:.1f}h logged)"
                self.inputs["work_item"].addItem(display_text, item.get("id"))
        except Exception as e:
            print(f"Warning: Failed to update work item suggestions: {e}")

    def on_work_item_changed(self):
        """Handle work item selection change."""
        if self.updating_template:
            return
            
        current_id = self.inputs["work_item"].currentData()
        if current_id:
            try:
                item = self.session_service.get_item_by_id(current_id)
                if item:
                    self.inputs["difficulty"].setCurrentText(item.get("default_difficulty", ""))
                    self.inputs["topic"].setCurrentText(item.get("default_topic", ""))
                    self._update_status_display(item)
                    return
            except Exception as e:
                print(f"Warning: Failed to get item details: {e}")
        
        self.auto_fill_from_text()

    def auto_fill_from_text(self):
        """Auto-fill fields based on work item and notes text."""
        if self.updating_template:
            return
            
        text = " ".join([
            self.inputs["work_item"].currentText(),
            self.inputs["notes"].text()
        ]).lower()
        
        if not text.strip():
            return
            
        try:
            suggestions = self.language_service.get_suggestions_from_text(text)
            if suggestions.get("topic"):
                self.inputs["topic"].setCurrentText(suggestions["topic"])
            if suggestions.get("difficulty"):
                self.inputs["difficulty"].setCurrentText(suggestions["difficulty"])
        except Exception as e:
            print(f"Warning: Auto-fill failed: {e}")

    def _update_status_display(self, item: Optional[Dict[str, Any]] = None):
        """Update the status display label with item information."""
        if not item:
            self.status_label.setText("")
            return
            
        try:
            status_parts = self.ui_state_service.format_item_status(item)
            self.status_label.setText(" | ".join(status_parts))
        except Exception as e:
            print(f"Warning: Failed to update status display: {e}")

    # ===== Form Actions =====
    def clear_form(self):
        """Clear all form inputs and reset to defaults."""
        self.updating_template = True
        try:
            self.inputs["date"].setDate(QDate.currentDate())
            self.inputs["hours"].setValue(0.0)
            self.inputs["notes"].clear()
            self.inputs["tags"].clear()
            self.inputs["status"].setCurrentText("In Progress")
            
            for field in ["language", "type", "work_item", "difficulty", "topic"]:
                self.inputs[field].setCurrentIndex(0)
            
            self.status_label.setText("")
            self.editing_session_id = None
        finally:
            self.updating_template = False

    def add_entry(self):
        """Start adding a new entry by clearing the form."""
        self.clear_form()

    def save_entry(self):
        """Save the current form data as a new or updated session."""
        try:
            # Validate and collect form data
            form_data = self._collect_form_data()
            if not form_data:
                return  # Validation failed
            
            # Handle suggestions dialog if needed
            item_id = self._handle_item_suggestions(form_data)
            if item_id is None:
                return  # User cancelled
                
            # Save the session
            session_data = self._prepare_session_data(form_data, item_id)
            self.session_service.save_session(session_data, self.editing_session_id)
            
            # Update UI
            self.reload_table()
            self.clear_form()
            self._show_success("Entry saved successfully!")
            
        except Exception as e:
            self._show_error("Save Entry", f"Failed to save entry: {e}")

    def delete_entry(self):
        """Delete the selected session entry."""
        try:
            session_id = self._get_selected_session_id()
            if session_id is None:
                self._show_info("Please select a row to delete.")
                return
                
            if not self._confirm_delete(session_id):
                return
                
            self.session_service.delete_session(session_id)
            self.reload_table()
            self._show_success("Entry deleted successfully!")
            
        except Exception as e:
            self._show_error("Delete Entry", f"Failed to delete entry: {e}")

    def export_csv(self):
        """Export all sessions to a CSV file."""
        try:
            file_path = self._get_export_file_path()
            if not file_path:
                return
                
            session_count = self.session_service.export_to_csv(file_path)
            self._show_success(f"Exported {session_count} sessions to {file_path}")
            
        except Exception as e:
            self._show_error("Export CSV", f"Failed to export CSV: {e}")

    # ===== Table Operations =====
    def reload_table(self):
        """Reload the table with fresh data from the database."""
        self.reloading = True
        try:
            sessions = self.session_service.get_sessions(limit=1000)
            self._populate_table(sessions)
            self.table.resizeRowsToContents()
        except Exception as e:
            self._show_error("Load Data", f"Failed to load data: {e}")
        finally:
            self.reloading = False

    def _populate_table(self, sessions: List[tuple]):
        """Populate the table with session data."""
        self.table.setRowCount(0)
        
        for session in sessions:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            display_data = self._format_session_for_display(session)
            
            for col, value in enumerate(display_data):
                item = QTableWidgetItem("" if value is None else str(value))
                
                # Set read-only flags for computed columns
                if col in TableConfig.READONLY_COLUMNS:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                
                self.table.setItem(row, col, item)

    def _format_session_for_display(self, session: tuple) -> List[str]:
        """Format a session tuple for table display."""
        return [
            str(session[0]),  # ID
            session[1],       # Date
            session[2],       # Language
            session[3],       # Type
            session[4],       # Work Item Name
            "",               # Target Time (separate query if needed)
            session[5],       # Status
            f"{float(session[6]):.2f}" if session[6] is not None else "0.00",  # Hours
            session[7],       # Notes
            session[8],       # Tags
            session[9],       # Difficulty
            session[10],      # Topic
            f"{float(session[11]):.2f}" if session[11] is not None else "0.00",  # Points
            f"{float(session[12]):.1f}%" if session[12] not in (None, "", 0) else "",  # Progress
        ]

    def on_cell_changed(self, item: QTableWidgetItem):
        """Handle inline cell editing."""
        if self.reloading:
            return
            
        try:
            row_data = self._collect_row_data(item.row())
            if not row_data:
                return
                
            # Update the session
            updated_points = self.session_service.update_session_inline(row_data)
            
            # Update points display
            self._update_points_display(item.row(), updated_points)
            
            # Reload if hours or status changed (affects summaries)
            if item.column() in [TableConfig.get_column_index("Hours"), 
                               TableConfig.get_column_index("Status")]:
                self.reload_table()
                
        except Exception as e:
            print(f"Warning: Cell update failed: {e}")

    # ===== Helper Methods =====
    def _collect_form_data(self) -> Optional[Dict[str, Any]]:
        """Collect and validate form data."""
        try:
            data = {
                "language_code": self.inputs["language"].currentData(),
                "item_type": self.inputs["type"].currentText().strip(),
                "work_item": self.inputs["work_item"].currentText().strip(),
                "date_str": self.inputs["date"].date().toString("yyyy-MM-dd"),
                "hours": float(self.inputs["hours"].value()),
                "notes": self.inputs["notes"].text().strip(),
                "tags": self.inputs["tags"].text().strip(),
                "difficulty": self.inputs["difficulty"].currentText() or "Beginner",
                "topic": self.inputs["topic"].currentText().strip(),
                "status": self.inputs["status"].currentText() or "In Progress",
            }
            
            # Validation
            if not data["language_code"]:
                self._show_warning("Please select a language.")
                return None
            if not data["work_item"]:
                self._show_warning("Please enter the exercise or project name.")
                return None
            if data["item_type"] not in {"Exercise", "Project"}:
                self._show_warning("Please choose a Type: Exercise or Project.")
                return None
                
            return data
            
        except Exception as e:
            self._show_error("Form Validation", f"Invalid form data: {e}")
            return None

    def _handle_item_suggestions(self, form_data: Dict[str, Any]) -> Optional[int]:
        """Handle item creation with similarity suggestions."""
        item_id, suggestions = self.session_service.find_or_create_item(
            form_data["language_code"], 
            form_data["item_type"], 
            form_data["work_item"]
        )
        
        if suggestions:
            dialog = SuggestionDialog(suggestions, form_data["work_item"], self)
            if dialog.exec():
                if dialog.create_new:
                    item_id, _ = self.session_service.find_or_create_item(
                        form_data["language_code"], 
                        form_data["item_type"], 
                        form_data["work_item"]
                    )
                else:
                    item_id = dialog.selected_item_id or item_id
            else:
                return None  # User cancelled
                
        return item_id

    def _prepare_session_data(self, form_data: Dict[str, Any], item_id: int) -> Dict[str, Any]:
        """Prepare session data for saving."""
        return {
            "item_id": item_id,
            "date": form_data["date_str"],
            "status": form_data["status"],
            "hours_spent": form_data["hours"],
            "notes": form_data["notes"],
            "tags": form_data["tags"],
            "difficulty": form_data["difficulty"],
            "topic": form_data["topic"],
        }

    def _collect_row_data(self, row: int) -> Optional[Dict[str, Any]]:
        """Collect data from a table row."""
        try:
            def get_cell(header: str) -> str:
                col = TableConfig.get_column_index(header)
                item = self.table.item(row, col)
                return "" if item is None else item.text().strip()

            # Get session ID
            id_item = self.table.item(row, 0)
            if not id_item or not id_item.text().strip():
                return None
            session_id = int(id_item.text())

            # Parse hours safely
            try:
                hours = float(get_cell("Hours") or "0")
            except ValueError:
                hours = 0.0
                # Fix invalid hours in UI
                self.reloading = True
                try:
                    self.table.item(row, TableConfig.get_column_index("Hours")).setText("0.00")
                finally:
                    self.reloading = False

            return {
                "id": session_id,
                "date": get_cell("Date") or QDate.currentDate().toString("yyyy-MM-dd"),
                "status": get_cell("Status") or "In Progress",
                "hours_spent": hours,
                "notes": get_cell("Notes"),
                "tags": get_cell("Tags"),
                "difficulty": get_cell("Difficulty") or "Beginner",
                "topic": get_cell("Topic"),
            }
            
        except Exception as e:
            print(f"Error collecting row data: {e}")
            return None

    def _get_selected_session_id(self) -> Optional[int]:
        """Get the ID of the currently selected session."""
        row = self.table.currentRow()
        if row < 0:
            return None
            
        id_item = self.table.item(row, 0)
        if not id_item or not id_item.text().strip():
            return None
            
        try:
            return int(id_item.text())
        except ValueError:
            return None

    def _update_points_display(self, row: int, points: float):
        """Update the points display for a specific row."""
        self.reloading = True
        try:
            points_col = TableConfig.get_column_index("Points")
            self.table.item(row, points_col).setText(f"{points:.2f}")
        finally:
            self.reloading = False

    def _get_export_file_path(self) -> Optional[str]:
        """Get file path for CSV export."""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export CSV", "learning_sessions.csv", "CSV Files (*.csv)"
        )
        return file_path if file_path else None

    def _confirm_delete(self, session_id: int) -> bool:
        """Show delete confirmation dialog."""
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete session {session_id}?",
            QMessageBox.Yes | QMessageBox.No,
        )
        return reply == QMessageBox.Yes

    # ===== Message Display Methods =====
    def _show_error(self, title: str, message: str):
        """Show error message dialog."""
        QMessageBox.critical(self, title, message)

    def _show_warning(self, message: str):
        """Show warning message dialog."""
        QMessageBox.warning(self, "Validation", message)

    def _show_info(self, message: str):
        """Show info message dialog."""
        QMessageBox.information(self, "Info", message)

    def _show_success(self, message: str):
        """Show success message dialog."""
        QMessageBox.information(self, "Success", message)