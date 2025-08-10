# report_dialog.py

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QListWidget,
    QTextEdit, QHBoxLayout, QListWidgetItem, QMessageBox,
    QComboBox, QLineEdit, QCheckBox, QGroupBox, QScrollArea,
    QTableView, QFormLayout, QDateEdit, QRadioButton, QButtonGroup, QFileDialog, QApplication
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QStandardItemModel, QStandardItem
import pandas as pd
import numpy as np
import sys


class QuickReportDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📊 Quick Report Export")
        self.setMinimumSize(900, 600)

        # Setup mock data
        self.df_full = self.generate_mock_data()
        self.filtered_df = self.df_full.copy()

        self.selected_columns = list(self.df_full.columns)
        self.sort_field = "Move-Out Date"
        self.sort_ascending = False

        self.init_ui()
        self.refresh_preview()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Filter bar
        filter_layout = QFormLayout()
        self.property_filter = QComboBox()
        self.property_filter.addItem("All")
        self.property_filter.addItems(sorted(self.df_full["Property"].unique()))
        self.property_filter.currentTextChanged.connect(self.refresh_preview)

        self.lifecycle_filter = QComboBox()
        self.lifecycle_filter.addItem("All")
        self.lifecycle_filter.addItems(sorted(self.df_full["Lifecycle Stage"].unique()))
        self.lifecycle_filter.currentTextChanged.connect(self.refresh_preview)

        self.status_filter = QComboBox()
        self.status_filter.addItem("All")
        self.status_filter.addItems(sorted(self.df_full["Turn Status"].unique()))
        self.status_filter.currentTextChanged.connect(self.refresh_preview)

        self.delayed_check = QCheckBox("Only Show Delayed")
        self.delayed_check.stateChanged.connect(self.refresh_preview)

        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.setDate(QDate(2025, 7, 1))
        self.date_from.dateChanged.connect(self.refresh_preview)

        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.setDate(QDate(2025, 7, 20))
        self.date_to.dateChanged.connect(self.refresh_preview)

        filter_layout.addRow("Property:", self.property_filter)
        filter_layout.addRow("Lifecycle Stage:", self.lifecycle_filter)
        filter_layout.addRow("Turn Status:", self.status_filter)
        filter_layout.addRow("Move-Out Date From:", self.date_from)
        filter_layout.addRow("To:", self.date_to)
        filter_layout.addRow("", self.delayed_check)
        layout.addLayout(filter_layout)

        # Main UI layout
        content_layout = QHBoxLayout()

        # Column selector
        self.field_scroll = QScrollArea()
        self.field_scroll.setWidgetResizable(True)
        self.field_box = QGroupBox("Select Columns to Export")
        self.field_layout = QVBoxLayout(self.field_box)
        self.field_scroll.setWidget(self.field_box)

        self.field_checks = {}
        for col in self.df_full.columns:
            cb = QCheckBox(col)
            cb.setChecked(True)
            cb.stateChanged.connect(self.update_selected_columns)
            self.field_checks[col] = cb
            self.field_layout.addWidget(cb)

        content_layout.addWidget(self.field_scroll, 1)

        # Table preview
        self.table_view = QTableView()
        content_layout.addWidget(self.table_view, 3)

        layout.addLayout(content_layout)

        # Export controls (moved to top, organized professionally)
        export_layout = QHBoxLayout()

        export_config_layout = QVBoxLayout()

        # First row: Filename and Format
        filename_layout = QHBoxLayout()
        filename_layout.addWidget(QLabel("Filename:"))
        self.filename_input = QLineEdit("TurnExport.xlsx")
        filename_layout.addWidget(self.filename_input)
        filename_layout.addWidget(QLabel("Format:"))
        self.format_picker = QComboBox()
        self.format_picker.addItems(["Excel (.xlsx)", "CSV (.csv)"])
        filename_layout.addWidget(self.format_picker)
        export_config_layout.addLayout(filename_layout)

        # Second row: Scope and Sort
        options_layout = QHBoxLayout()
        self.scope_all = QRadioButton("Export All Rows")
        self.scope_filtered = QRadioButton("Export Filtered Only")
        self.scope_filtered.setChecked(True)
        scope_group = QButtonGroup(self)
        scope_group.addButton(self.scope_all)
        scope_group.addButton(self.scope_filtered)

        options_layout.addWidget(self.scope_all)
        options_layout.addWidget(self.scope_filtered)
        options_layout.addWidget(QLabel("Sort by:"))
        self.sort_field_combo = QComboBox()
        self.sort_field_combo.addItems(self.df_full.columns)
        self.sort_field_combo.setCurrentText("Move-Out Date")
        self.sort_field_combo.currentTextChanged.connect(self.sort_updated)
        options_layout.addWidget(self.sort_field_combo)
        self.sort_dir_combo = QComboBox()
        self.sort_dir_combo.addItems(["Descending", "Ascending"])
        self.sort_dir_combo.currentTextChanged.connect(self.sort_updated)
        options_layout.addWidget(self.sort_dir_combo)

        export_config_layout.addLayout(options_layout)

        # Final button, aligned right
        self.export_button = QPushButton("Export")
        export_layout.addLayout(export_config_layout)
        export_layout.addStretch()
        export_layout.addWidget(self.export_button)
        self.export_button.clicked.connect(self.export_data)

        layout.addLayout(export_layout)

    def update_selected_columns(self):
        self.selected_columns = [col for col, cb in self.field_checks.items() if cb.isChecked()]
        self.refresh_preview()

    def sort_updated(self):
        self.sort_field = self.sort_field_combo.currentText()
        self.sort_ascending = self.sort_dir_combo.currentText() == "Ascending"
        self.refresh_preview()

    def refresh_preview(self):
        df = self.df_full.copy()

        if self.property_filter.currentText() != "All":
            df = df[df["Property"] == self.property_filter.currentText()]
        if self.lifecycle_filter.currentText() != "All":
            df = df[df["Lifecycle Stage"] == self.lifecycle_filter.currentText()]
        if self.status_filter.currentText() != "All":
            df = df[df["Turn Status"] == self.status_filter.currentText()]
        if self.delayed_check.isChecked():
            df = df[df["Delayed?"] == "Yes"]
        df = df[
            (df["Move-Out Date"] >= pd.to_datetime(self.date_from.date().toPython()))
            & (df["Move-Out Date"] <= pd.to_datetime(self.date_to.date().toPython()))
        ]

        df = df.sort_values(by=self.sort_field, ascending=self.sort_ascending)

        if self.selected_columns:
            df = df[self.selected_columns]

        self.filtered_df = df

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(df.columns.tolist())
        for row in df.head(10).itertuples(index=False):
            items = [QStandardItem(str(val)) for val in row]
            model.appendRow(items)
        self.table_view.setModel(model)

    def export_data(self):
        df = self.df_full if self.scope_all.isChecked() else self.filtered_df

        if not self.selected_columns:
            QMessageBox.warning(self, "Missing Columns", "Please select at least one column.")
            return

        df = df[self.selected_columns]

        filename = self.filename_input.text().strip()
        if not filename:
            QMessageBox.warning(self, "Missing Filename", "Please enter a filename.")
            return

        if self.format_picker.currentText().startswith("Excel"):
            if not filename.endswith(".xlsx"):
                filename += ".xlsx"
            df.to_excel(filename, index=False)
        else:
            if not filename.endswith(".csv"):
                filename += ".csv"
            df.to_csv(filename, index=False)

        QMessageBox.information(self, "Export Complete", f"Exported {len(df)} rows to {filename}")

    def generate_mock_data(self):
        np.random.seed(42)
        return pd.DataFrame({
            'Unit #': [f"Apt-{i}" for i in range(1, 21)],
            'Property': np.random.choice(['Northgate', 'Riverview', 'Parkside'], 20),
            'Floorplan': np.random.choice(['1B1B', '2B1B', '2B2B', 'Studio'], 20),
            'Square Footage': np.random.randint(450, 1200, 20),
            'Move-Out Date': pd.date_range('2025-07-01', periods=20),
            'Move-In Date': pd.date_range('2025-08-01', periods=20),
            'Ready Date': pd.date_range('2025-07-20', periods=20),
            'Final Walk Date': pd.date_range('2025-08-10', periods=20),
            'Lifecycle Stage': np.random.choice(['Vacant', 'In Turn', 'Occupied'], 20),
            'Turn Status': np.random.choice(['Not Started', 'In Progress', 'Completed'], 20),
            '% Complete': np.random.randint(0, 101, 20),
            'Delayed?': np.random.choice(['Yes', 'No'], 20),
            'Delay Reason': np.random.choice(['Vendor', 'Weather', 'Material', 'None'], 20),
            'Assigned Vendor': np.random.choice(['ACME Paint', 'BrightClean', 'FixItAll', 'None'], 20),
            'Assignment Type': np.random.choice(['Core', 'Regular', 'Optional'], 20),
            'Task Count Assigned': np.random.randint(0, 10, 20),
        })


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = QuickReportDialog()
    dialog.show()
    sys.exit(app.exec())
