`from PySide6.QtWidgets import (
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
        self.setMinimumSize(1000, 650)

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

        # === Top Control Box ===
        top_controls = QGroupBox("Report Export Setup")
        top_layout = QVBoxLayout(top_controls)

        # --- Filter Section ---
        filter_group = QGroupBox("Filters")
        filter_layout = QHBoxLayout()

        def labeled_combo(label, combo):
            container = QHBoxLayout()
            label_widget = QLabel(label)
            label_widget.setContentsMargins(0, 0, 0, 0)
            combo.setContentsMargins(0, 0, 0, 0)
            container.setSpacing(2)
            container.addWidget(label_widget)
            container.addWidget(combo)
            container.setAlignment(Qt.AlignmentFlag.AlignLeft)
            return container

        self.property_filter = QComboBox()
        self.property_filter.addItem("All")
        self.property_filter.addItems(sorted(self.df_full["Property"].unique()))
        self.property_filter.currentTextChanged.connect(self.refresh_preview)
        prop_layout = labeled_combo("Property:", self.property_filter)

        self.lifecycle_filter = QComboBox()
        self.lifecycle_filter.addItem("All")
        self.lifecycle_filter.addItems(sorted(self.df_full["Lifecycle Stage"].unique()))
        self.lifecycle_filter.currentTextChanged.connect(self.refresh_preview)
        life_layout = labeled_combo("Lifecycle Stage:", self.lifecycle_filter)

        self.status_filter = QComboBox()
        self.status_filter.addItem("All")
        self.status_filter.addItems(sorted(self.df_full["Turn Status"].unique()))
        self.status_filter.currentTextChanged.connect(self.refresh_preview)
        status_layout = labeled_combo("Turn Status:", self.status_filter)

        self.vendor_filter = QComboBox()
        self.vendor_filter.addItem("All")
        self.vendor_filter.addItems(sorted(self.df_full["Assigned Vendor"].unique()))
        self.vendor_filter.currentTextChanged.connect(self.refresh_preview)
        vendor_layout = labeled_combo("Assigned Vendor:", self.vendor_filter)

        filter_layout.addLayout(prop_layout)
        filter_layout.addLayout(life_layout)
        filter_layout.addLayout(status_layout)
        filter_layout.addLayout(vendor_layout)

        filter_group.setLayout(filter_layout)
        top_layout.addWidget(filter_group)

        # --- Date and Delay Section ---
        date_group = QGroupBox("Date Range & Delay")
        date_layout = QHBoxLayout()
        self.date_from = QDateEdit()
        self.date_from.setDisplayFormat("MM/dd/yyyy")
        self.date_from.setCalendarPopup(True)
        self.date_from.setDate(QDate(2025, 7, 1))
        self.date_from.dateChanged.connect(self.refresh_preview)

        self.date_to = QDateEdit()
        self.date_to.setDisplayFormat("MM/dd/yyyy")
        self.date_to.setCalendarPopup(True)
        self.date_to.setDate(QDate(2025, 7, 20))
        self.date_to.dateChanged.connect(self.refresh_preview)

        self.delayed_check = QCheckBox("Only Show Delayed")
        self.delayed_check.stateChanged.connect(self.refresh_preview)

        date_layout.addWidget(QLabel("Move-Out From:"))
        date_layout.addWidget(self.date_from)
        date_layout.addWidget(QLabel("To:"))
        date_layout.addWidget(self.date_to)
        date_layout.addStretch()
        date_layout.addWidget(self.delayed_check)

        date_group.setLayout(date_layout)
        top_layout.addWidget(date_group)

        # --- Export Options Section ---
        export_group = QGroupBox("Export Options")
        export_layout = QHBoxLayout()

        self.filename_input = QLineEdit("TurnExport.xlsx")
        self.format_picker = QComboBox()
        self.format_picker.addItems(["Excel (.xlsx)", "CSV (.csv)"])

        self.scope_all = QRadioButton("Export All Rows")
        self.scope_filtered = QRadioButton("Export Filtered Only")
        self.scope_filtered.setChecked(True)
        scope_group = QButtonGroup(self)
        scope_group.addButton(self.scope_all)
        scope_group.addButton(self.scope_filtered)

        self.sort_field_combo = QComboBox()
        self.sort_field_combo.addItems(self.df_full.columns)
        self.sort_field_combo.setCurrentText("Move-Out Date")
        self.sort_field_combo.currentTextChanged.connect(self.sort_updated)

        self.sort_dir_combo = QComboBox()
        self.sort_dir_combo.addItems(["Descending", "Ascending"])
        self.sort_dir_combo.currentTextChanged.connect(self.sort_updated)

        self.export_button = QPushButton("Export")
        self.export_button.clicked.connect(self.export_data)

        export_layout.addWidget(QLabel("Filename:"))
        export_layout.addWidget(self.filename_input)
        export_layout.addWidget(QLabel("Format:"))
        export_layout.addWidget(self.format_picker)
        export_layout.addWidget(self.scope_all)
        export_layout.addWidget(self.scope_filtered)
        export_layout.addWidget(QLabel("Sort by:"))
        export_layout.addWidget(self.sort_field_combo)
        export_layout.addWidget(self.sort_dir_combo)
        export_layout.addStretch()
        export_layout.addWidget(self.export_button)

        export_group.setLayout(export_layout)
        top_layout.addWidget(export_group)

        layout.addWidget(top_controls)

        # === Main Body ===
        content_layout = QHBoxLayout()

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

        self.table_view = QTableView()
        content_layout.addWidget(self.table_view, 3)

        layout.addLayout(content_layout)

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
        if self.vendor_filter.currentText() != "All":
            df = df[df["Assigned Vendor"] == self.vendor_filter.currentText()]
        if self.delayed_check.isChecked():
            df = df[df["Delayed?"] == "Yes"]
        df = df[
            (df["Move-Out Date"] >= pd.to_datetime(self.date_from.date().toPython())) &
            (df["Move-Out Date"] <= pd.to_datetime(self.date_to.date().toPython()))
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
`
