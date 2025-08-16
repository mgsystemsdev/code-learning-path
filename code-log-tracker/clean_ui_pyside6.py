# clean_ui_pyside6.py
"""
Clean UI-only PySide6 dashboard ready for emitter connections:
- Pure UI components with no business logic
- Placeholder data removed
- Ready to connect to external emitters/controllers
- All UI styling and layout preserved

Run:  python clean_ui_pyside6.py
Requires: PySide6
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSplitter, QFrame, QStatusBar,
    QTableWidget, QTableWidgetItem, QLineEdit, QComboBox, QSpinBox,
    QSizePolicy, QDateEdit, QDoubleSpinBox, QGridLayout, QGroupBox,
    QCompleter
)
from PySide6.QtCore import Qt, QTimer, QDate, Signal
from PySide6.QtGui import QStandardItemModel, QStandardItem

# ---------------------------
# Embedded CompactForm (UI-only)
# ---------------------------
class CompactForm(QWidget):
    """Ultra-compact Learning Session Entry form with advanced widgets."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.inputs = {}
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
        
        # Apply styling with our existing color scheme
        self._apply_form_styling()
        
    def _create_form_fields(self, grid_layout: QGridLayout):
        """Create all form fields in optimized horizontal layout."""
        
        # ROW 1: Core Data (Date, Language, Type, Work Item, Status)
        
        # Date field with calendar popup
        self.inputs["date"] = QDateEdit()
        self.inputs["date"].setCalendarPopup(True)
        self.inputs["date"].setDisplayFormat("MM/dd/yy")
        self.inputs["date"].setDate(QDate.currentDate())
        self.inputs["date"].setMinimumHeight(32)
        grid_layout.addWidget(self.create_label("Date:"), 0, 0)
        grid_layout.addWidget(self.inputs["date"], 0, 1)
        
        # Language ComboBox with red square and white arrowhead
        self.inputs["language"] = self._create_scrollable_combo([
            "Python", "JavaScript", "HTML", "CSS"
        ], editable=True)
        self.inputs["language"].setMinimumHeight(32)
        self.inputs["language"].setStyleSheet("QComboBox::down-arrow { width: 12px; height: 12px; background-color: red; color: white; padding-right: 6px; }")
        grid_layout.addWidget(self.create_label("Language:"), 0, 2)
        grid_layout.addWidget(self.inputs["language"], 0, 3)
        
        # Type ComboBox with red square and white arrowhead
        self.inputs["type"] = self._create_scrollable_combo([
            "Reading", "Practice", "Project", "Tutorial"
        ], editable=True)
        self.inputs["type"].setMinimumHeight(32)
        self.inputs["type"].setStyleSheet("QComboBox::down-arrow { width: 12px; height: 12px; background-color: red; color: white; padding-right: 6px; }")
        self.inputs["type"].currentTextChanged.connect(self._on_type_changed)
        grid_layout.addWidget(self.create_label("Type:"), 0, 4)
        grid_layout.addWidget(self.inputs["type"], 0, 5)
        
        # Work Item (combo box with type-to-save)
        self.inputs["work_item"] = self._create_scrollable_combo([
            "My First Python Project", "JavaScript Tutorial", "HTML/CSS Practice", "Learning Git"
        ], editable=True)
        self.inputs["work_item"].setPlaceholderText("Project or resource name…")
        self.inputs["work_item"].setMinimumHeight(32)
        self.inputs["work_item"].setStyleSheet("QComboBox::down-arrow { width: 12px; height: 12px; background-color: red; color: white; padding-right: 6px; }")
        grid_layout.addWidget(self.create_label("Work Item:"), 0, 6)
        grid_layout.addWidget(self.inputs["work_item"], 0, 7, 1, 3)  # Span 3 columns
        
        # Status ComboBox with red square and white arrowhead
        self.inputs["status"] = self._create_scrollable_combo([
            "In Progress", "Completed", "On Hold", "Pending", "Not Started"
        ])
        self.inputs["status"].setCurrentText("In Progress")
        self.inputs["status"].setMinimumHeight(32)
        self.inputs["status"].setStyleSheet("QComboBox::down-arrow { width: 12px; height: 12px; background-color: red; color: white; padding-right: 6px; }")
        grid_layout.addWidget(self.create_label("Status:"), 0, 10)
        grid_layout.addWidget(self.inputs["status"], 0, 11)
        
        # ROW 2: Details & Effort
        
        # Topic ComboBox with red square and white arrowhead
        self.inputs["topic"] = self._create_scrollable_combo([
            "Variables", "Loops", "Functions", "Debugging"
        ], editable=True)
        self.inputs["topic"].setPlaceholderText("Enter topic...")
        self.inputs["topic"].setMinimumHeight(32)
        self.inputs["topic"].setStyleSheet("QComboBox::down-arrow { width: 12px; height: 12px; background-color: red; color: white; padding-right: 6px; }")
        grid_layout.addWidget(self.create_label("Topic:"), 1, 0)
        grid_layout.addWidget(self.inputs["topic"], 1, 1, 1, 3)  # Span 3 columns
        
        # Difficulty ComboBox with red square and white arrowhead
        self.inputs["difficulty"] = self._create_scrollable_combo([
            "Easy", "Medium", "Hard", "Expert"
        ])
        self.inputs["difficulty"].setMinimumHeight(32)
        self.inputs["difficulty"].setStyleSheet("QComboBox::down-arrow { width: 12px; height: 12px; background-color: red; color: white; padding-right: 6px; }")
        grid_layout.addWidget(self.create_label("Difficulty:"), 1, 4)
        grid_layout.addWidget(self.inputs["difficulty"], 1, 5)
        
        # Hours field with red square and white arrowhead steppers
        self.inputs["hours"] = QDoubleSpinBox()
        self.inputs["hours"].setDecimals(2)
        self.inputs["hours"].setRange(0, 24)
        self.inputs["hours"].setSingleStep(0.5)
        self.inputs["hours"].setMinimumHeight(32)
        self.inputs["hours"].setStyleSheet("QDoubleSpinBox::up-button { width: 12px; height: 12px; background-color: red; color: white; } QDoubleSpinBox::down-button { width: 12px; height: 12px; background-color: red; color: white; }")
        grid_layout.addWidget(self.create_label("Hours:"), 1, 6)
        grid_layout.addWidget(self.inputs["hours"], 1, 7)
        
        # Target Time field with red square and white arrowhead steppers
        self.inputs["target_time"] = QDoubleSpinBox()
        self.inputs["target_time"].setDecimals(2)
        self.inputs["target_time"].setRange(0, 200)
        self.inputs["target_time"].setSingleStep(0.5)
        self.inputs["target_time"].setMinimumHeight(32)
        self.inputs["target_time"].setStyleSheet("QDoubleSpinBox::up-button { width: 12px; height: 12px; background-color: red; color: white; } QDoubleSpinBox::down-button { width: 12px; height: 12px; background-color: red; color: white; }")
        grid_layout.addWidget(self.create_label("Target:"), 1, 8)
        grid_layout.addWidget(self.inputs["target_time"], 1, 9)
        
        # Tags ComboBox with red square and white arrowhead
        self.inputs["tags"] = self._create_checkable_combo([
            "basics", "coding", "practice", "challenge"
        ])
        self.inputs["tags"].setMinimumHeight(32)
        self.inputs["tags"].setStyleSheet("QComboBox::down-arrow { width: 12px; height: 12px; background-color: red; color: white; padding-right: 6px; }")
        grid_layout.addWidget(self.create_label("Tags:"), 1, 10)
        grid_layout.addWidget(self.inputs["tags"], 1, 11)
        
        # Notes field (multiline input bar)
        self.inputs["notes"] = QLineEdit()
        self.inputs["notes"].setObjectName("notes")  # For special CSS targeting
        self.inputs["notes"].setPlaceholderText("Quick notes about this session…")
        self.inputs["notes"].setMinimumHeight(32)
        grid_layout.addWidget(self.create_label("Notes:"), 2, 0)
        grid_layout.addWidget(self.inputs["notes"], 2, 1, 1, 11)  # Span the entire row
        
    def _create_scrollable_combo(self, items, editable=False):
        """Create a QComboBox with proper scrolling and type-ahead."""
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
        
        return combo
        
    def _create_checkable_combo(self, items):
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
        
    def _update_tags_display(self, combo):
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
        
    def _apply_form_styling(self):
        """Apply cohesive gray-black theme with subtle tonal differences."""
        self.setStyleSheet("""
            QGroupBox#entryGroup { 
                border: 1px solid #3a3a3a; 
                border-radius: 8px; 
                margin-top: 12px; 
                padding: 16px;
                font-weight: bold;
                background-color: #1c1c1c;
            }
            QGroupBox::title { 
                subcontrol-origin: margin;
                left: 8px; 
                padding: 0 8px;
                color: #ffffff;
                font-size: 12px;
            }
            QLabel {
                color: #e0e0e0;
                font-size: 10px;
                padding-right: 4px;
            }
            QComboBox, QLineEdit, QDateEdit, QDoubleSpinBox {
                min-height: 32px; 
                padding: 4px 8px;
                border: 1px solid #3a3a3a; 
                border-radius: 4px;
                background-color: #2a2a2a;
                color: #ffffff;
                font-size: 11px;
            }
            QComboBox:focus, QLineEdit:focus, QDateEdit:focus, QDoubleSpinBox:focus,
            QComboBox:hover, QLineEdit:hover, QDateEdit:hover, QDoubleSpinBox:hover {
                border-color: #404040;
                background-color: #303030;
            }
            QLineEdit#notes {
                background-color: #353535;
            }
            QLineEdit#notes:focus, QLineEdit#notes:hover {
                background-color: #404040;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 8px;
                background-color: #2a2a2a;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
            QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
                border: none;
                padding: 2px 4px;
                background-color: #2a2a2a;
            }
            QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {
                background-color: #404040;
            }
            QComboBox QAbstractItemView { 
                min-width: 200px;
                background-color: #2a2a2a;
                border: 1px solid #3a3a3a;
                selection-background-color: #404040;
                color: #ffffff;
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
    
    def get_form_data(self):
        """Get current form data."""
        data = {}
        if "date" in self.inputs:
            data["date"] = self.inputs["date"].date().toString("yyyy-MM-dd")
        if "language" in self.inputs:
            data["language"] = self.inputs["language"].currentText()
        if "type" in self.inputs:
            data["type"] = self.inputs["type"].currentText()
        if "work_item" in self.inputs:
            data["work_item"] = self.inputs["work_item"].currentText()
        if "topic" in self.inputs:
            data["topic"] = self.inputs["topic"].currentText()
        if "difficulty" in self.inputs:
            data["difficulty"] = self.inputs["difficulty"].currentText()
        if "status" in self.inputs:
            data["status"] = self.inputs["status"].currentText()
        if "tags" in self.inputs:
            data["tags"] = self.inputs["tags"].currentText()
        if "hours" in self.inputs:
            data["hours"] = self.inputs["hours"].value()
        if "target_time" in self.inputs:
            data["target_time"] = self.inputs["target_time"].value()
        if "notes" in self.inputs:
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

# ---------------------------
# Clean DashboardTable (UI-only)
# ---------------------------
class DashboardTable(QWidget):
    """A clean table with 14 columns ready for data connection."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.columns = [
            "Date", "Language", "Type", "Work Item Name", "Topic", "Difficulty",
            "Status", "Tags", "Hours", "Target Time", "Points", "Progress %", "ID", "Notes"
        ]

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
        root.addWidget(self.table, 1)

# ---------------------------
# Main Dashboard Window (Clean UI-only)
# ---------------------------
class DashboardWindow(QMainWindow):
    """Clean dashboard ready for emitter connections."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Smart Learning Tracker - Dashboard")
        self.resize(1400, 820)  # Proper size for all 14 columns

        # Import simplified services
        from simple_db import SimpleSessionService, SimpleLanguageService, init_simple_db
        
        # Initialize simple database and services
        init_simple_db()
        self.session_service = SimpleSessionService()
        self.language_service = SimpleLanguageService()
        self.editing_session_id = None

        self._create_toolbar()
        self._create_status_bar()
        self._build_layout()
        self._wire_up_connections()
        self._load_initial_data()

    # ---- Top toolbar (Clean UI only) ----
    def _create_toolbar(self):
        self.toolbar = QFrame()
        self.toolbar.setFrameStyle(QFrame.StyledPanel)
        self.toolbar.setFixedHeight(52)
        self.toolbar.setStyleSheet(
            "QFrame {{ background-color:#1e293b; border-bottom:2px solid #475569; }}"
        )
        hl = QHBoxLayout(self.toolbar)
        hl.setContentsMargins(12, 8, 12, 8)
        hl.setSpacing(10)

        self.add_btn = QPushButton("➕ Add")
        self.save_btn = QPushButton("💾 Save")
        self.cancel_btn = QPushButton("↩️ Cancel")
        self.clear_filters_btn = QPushButton("🔍 Clear Filters")
        self.delete_btn = QPushButton("🗑️ Delete")

        for b in (self.add_btn, self.save_btn, self.cancel_btn, self.clear_filters_btn, self.delete_btn):
            b.setFixedHeight(34)

        hl.addWidget(self.add_btn)
        hl.addWidget(self.save_btn)
        hl.addWidget(self.cancel_btn)
        hl.addStretch(1)
        hl.addWidget(self.clear_filters_btn)
        hl.addWidget(self.delete_btn)

    # ---- Status bar ----
    def _create_status_bar(self):
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.records_label = QLabel("📊 Records: 0")
        self.status_label = QLabel("")
        self.status.addPermanentWidget(self.records_label)
        self.status.addWidget(self.status_label, 1)

    # ---- Central layout ----
    def _build_layout(self):
        central = QWidget()
        v = QVBoxLayout(central)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(0)

        v.addWidget(self.toolbar)

        splitter = QSplitter(Qt.Vertical)
        splitter.setChildrenCollapsible(False)

        # Top: table
        self.table = DashboardTable()
        splitter.addWidget(self.table)

        # Bottom: compact form
        self.form = CompactForm()
        splitter.addWidget(self.form)

        # Set proportions
        splitter.setStretchFactor(0, 3)  # table
        splitter.setStretchFactor(1, 1)  # form

        v.addWidget(splitter, 1)
        self.setCentralWidget(central)
    
    def _wire_up_connections(self):
        """Wire up the business logic to UI events."""
        # Button connections
        self.add_btn.clicked.connect(self._add_session)
        self.save_btn.clicked.connect(self._save_session)
        self.cancel_btn.clicked.connect(self._cancel_edit)
        self.delete_btn.clicked.connect(self._delete_session)
        self.clear_filters_btn.clicked.connect(self._clear_filters)
        
        # Form data change tracking
        for field_name, widget in self.form.inputs.items():
            if hasattr(widget, 'currentTextChanged'):
                widget.currentTextChanged.connect(self._on_form_changed)
            elif hasattr(widget, 'textChanged'):
                widget.textChanged.connect(self._on_form_changed)
            elif hasattr(widget, 'valueChanged'):
                widget.valueChanged.connect(self._on_form_changed)
            elif hasattr(widget, 'dateChanged'):
                widget.dateChanged.connect(self._on_form_changed)
        
        # Table selection
        self.table.table.itemSelectionChanged.connect(self._on_selection_changed)
        
        # Initially disable editing buttons
        self.save_btn.setEnabled(False)
        self.cancel_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)
    
    def _load_initial_data(self):
        """Load languages and table data."""
        try:
            # Load languages into form
            languages = self.language_service.get_languages()
            language_combo = self.form.inputs.get("language")
            if language_combo:
                language_combo.clear()
                for code, name, _color in languages:
                    language_combo.addItem(name, code)
            
            # Load table data
            self._reload_table()
            
        except Exception as e:
            print(f"Error loading initial data: {e}")
    
    def _reload_table(self):
        """Reload table data from database."""
        try:
            sessions = self.session_service.get_sessions()
            
            # Clear and populate table
            self.table.table.setRowCount(len(sessions))
            
            for row_idx, session in enumerate(sessions):
                # Map session tuple to table columns  
                session_data = [
                    session[1],  # Date
                    session[2],  # Language
                    session[3],  # Type  
                    session[4],  # Work Item Name
                    session[5],  # Topic
                    session[6],  # Difficulty
                    session[7],  # Status
                    session[8],  # Tags
                    f"{float(session[9]):.2f}",  # Hours
                    f"{float(session[10]):.1f}",  # Target Time
                    f"{float(session[11]):.1f}",  # Points
                    f"{float(session[12]):.1f}%",  # Progress %
                    str(session[0]),  # ID
                    session[13]   # Notes
                ]
                
                # Fill table row
                for col_idx, value in enumerate(session_data):
                    item = QTableWidgetItem(str(value))
                    self.table.table.setItem(row_idx, col_idx, item)
            
            self.records_label.setText(f"📊 Records: {len(sessions)}")
            
        except Exception as e:
            print(f"Error loading sessions: {e}")
    
    def _on_selection_changed(self):
        """Handle table selection changes."""
        current_row = self.table.table.currentRow()
        if current_row >= 0:
            self.delete_btn.setEnabled(True)
            self._populate_form_from_table(current_row)
        else:
            self.delete_btn.setEnabled(False)
            self.editing_session_id = None
    
    def _populate_form_from_table(self, row_idx: int):
        """Populate form with data from selected table row."""
        # Get data from table
        if row_idx < self.table.table.rowCount():
            date_item = self.table.table.item(row_idx, 0)
            lang_item = self.table.table.item(row_idx, 1)
            type_item = self.table.table.item(row_idx, 2)
            work_item = self.table.table.item(row_idx, 3)
            topic_item = self.table.table.item(row_idx, 4)
            diff_item = self.table.table.item(row_idx, 5)
            status_item = self.table.table.item(row_idx, 6)
            tags_item = self.table.table.item(row_idx, 7)
            hours_item = self.table.table.item(row_idx, 8)
            target_item = self.table.table.item(row_idx, 9)
            id_item = self.table.table.item(row_idx, 12)
            notes_item = self.table.table.item(row_idx, 13)
            
            # Populate form
            if date_item:
                date = QDate.fromString(date_item.text(), "yyyy-MM-dd")
                self.form.inputs["date"].setDate(date)
            if lang_item:
                self.form.inputs["language"].setCurrentText(lang_item.text())
            if type_item:
                self.form.inputs["type"].setCurrentText(type_item.text())
            if work_item:
                self.form.inputs["work_item"].setCurrentText(work_item.text())
            if status_item:
                self.form.inputs["status"].setCurrentText(status_item.text())
            if topic_item:
                self.form.inputs["topic"].setCurrentText(topic_item.text())
            if diff_item:
                self.form.inputs["difficulty"].setCurrentText(diff_item.text())
            if hours_item:
                try:
                    self.form.inputs["hours"].setValue(float(hours_item.text()))
                except ValueError:
                    pass
            if target_item:
                try:
                    self.form.inputs["target_time"].setValue(float(target_item.text()))
                except ValueError:
                    pass
            if tags_item:
                self.form.inputs["tags"].setCurrentText(tags_item.text())
            if notes_item:
                self.form.inputs["notes"].setText(notes_item.text())
            
            # Set editing mode
            if id_item:
                self.editing_session_id = int(id_item.text())
    
    def _on_form_changed(self):
        """Handle form data changes."""
        self.save_btn.setEnabled(True)
        self.cancel_btn.setEnabled(True)
    
    def _add_session(self):
        """Start adding a new session."""
        self.form.clear_form()
        self.editing_session_id = None
        self.save_btn.setEnabled(True)
        self.cancel_btn.setEnabled(True)
        self.form.inputs["date"].setFocus()
    
    def _save_session(self):
        """Save the current session."""
        try:
            form_data = self.form.get_form_data()
            
            # Convert form data to database format
            db_data = {
                'date': form_data.get('date', ''),
                'language_code': form_data.get('language', ''),
                'type': form_data.get('type', ''),
                'canonical_name': form_data.get('work_item', ''),
                'status': form_data.get('status', ''),
                'hours_spent': form_data.get('hours', 0),
                'notes': form_data.get('notes', ''),
                'tags': form_data.get('tags', ''),
                'difficulty': form_data.get('difficulty', ''),
                'topic': form_data.get('topic', ''),
                'target_hours': form_data.get('target_time', 0)
            }
            
            # Validate required fields
            if not all([db_data['date'], db_data['language_code'], db_data['type'], db_data['canonical_name']]):
                self.status_label.setText("Please fill in required fields")
                return
            
            if db_data['hours_spent'] <= 0:
                self.status_label.setText("Hours must be greater than 0")
                return
            
            # Find or create item and save session
            item_id, suggestions = self.session_service.find_or_create_item(
                db_data['language_code'], db_data['type'], db_data['canonical_name']
            )
            db_data['item_id'] = item_id
            
            session_id = self.session_service.save_session(db_data, self.editing_session_id)
            
            # Success feedback
            if self.editing_session_id:
                self.status_label.setText(f"Session #{session_id} updated")
            else:
                self.status_label.setText(f"Session #{session_id} saved")
            
            # Refresh and reset
            self._reload_table()
            self.form.clear_form()
            self.editing_session_id = None
            self.save_btn.setEnabled(False)
            self.cancel_btn.setEnabled(False)
            
        except Exception as e:
            self.status_label.setText(f"Save failed: {e}")
    
    def _cancel_edit(self):
        """Cancel current edit."""
        self.form.clear_form()
        self.editing_session_id = None
        self.save_btn.setEnabled(False)
        self.cancel_btn.setEnabled(False)
        self.status_label.setText("Edit cancelled")
    
    def _delete_session(self):
        """Delete selected session."""
        current_row = self.table.table.currentRow()
        if current_row >= 0:
            # Get session ID from table
            id_item = self.table.table.item(current_row, self.table.columns.index("ID"))
            if id_item:
                session_id = int(id_item.text())
                try:
                    self.session_service.delete_session(session_id)
                    self.status_label.setText(f"Session #{session_id} deleted")
                    self._reload_table()
                    self.form.clear_form()
                    self.editing_session_id = None
                    self.delete_btn.setEnabled(False)
                    self.save_btn.setEnabled(False)
                    self.cancel_btn.setEnabled(False)
                except Exception as e:
                    self.status_label.setText(f"Delete failed: {e}")
    
    def _clear_filters(self):
        """Clear all filters and reload."""
        self._reload_table()
        self.status_label.setText("Filters cleared")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = DashboardWindow()
    win.show()  # Use normal window size instead of maximized
    sys.exit(app.exec())
