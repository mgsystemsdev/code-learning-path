from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QDateEdit,
    QTextEdit, QPushButton, QFormLayout, QGridLayout, QMessageBox, QWidget
)
from PySide6.QtCore import QDate
import datetime

class TaskFormDialog(QDialog):
    def __init__(self, unit_number=""):
        super().__init__()
        self.setWindowTitle("Make Ready - Full Unit Task Entry")
        self.setMinimumWidth(900)
        self.unit_number = unit_number

        layout = QVBoxLayout()

        # Header Section
        header_layout = QFormLayout()
        self.unit_input = QLineEdit(self.unit_number)
        self.property_input = QLineEdit()
        self.mo_date = QDateEdit()
        self.mo_date.setCalendarPopup(True)
        self.mi_date = QDateEdit()
        self.mi_date.setCalendarPopup(True)

        header_layout.addRow("Unit:", self.unit_input)
        header_layout.addRow("Property:", self.property_input)
        header_layout.addRow("Move-Out Date:", self.mo_date)
        header_layout.addRow("Move-In Date:", self.mi_date)
        layout.addLayout(header_layout)

        # Task Grid
        layout.addWidget(QLabel("Tasks:"))
        task_grid = QGridLayout()
        task_grid.addWidget(QLabel("Task"), 0, 0)
        task_grid.addWidget(QLabel("Vendor"), 0, 1)
        task_grid.addWidget(QLabel("Auto-Date"), 0, 2)
        task_grid.addWidget(QLabel("Status"), 0, 3)
        task_grid.addWidget(QLabel("Override Date"), 0, 4)

        self.task_rows = []
        tasks = [
            "Paint", "Carpet Clean", "Housekeeping", "Make Ready", "Tub Replacement",
            "Tub Acid Wash", "Sheetrock Repair", "Trash Out", "Appliance Check", "HVAC Check",
            "Baseboards", "Smoke Detector", "Caulking", "Cabinet Fix", "Door Repair",
            "Puck Light", "Flooring", "Carpet Quote", "Final Walk", "Stove Detail"
        ]

        for i, task in enumerate(tasks, start=1):
            task_label = QLabel(task)
            vendor_input = QComboBox()
            vendor_input.addItems(["", "Vendor A", "Vendor B", "Vendor C"])
            auto_date = QDateEdit()
            auto_date.setDate(QDate.currentDate())
            auto_date.setReadOnly(True)
            auto_date.setButtonSymbols(QDateEdit.NoButtons)
            status_input = QComboBox()
            status_input.addItems(["Not Started", "Scheduled", "In Progress", "Blocked", "✅ Done"])
            override_date = QDateEdit()
            override_date.setCalendarPopup(True)

            task_grid.addWidget(task_label, i, 0)
            task_grid.addWidget(vendor_input, i, 1)
            task_grid.addWidget(auto_date, i, 2)
            task_grid.addWidget(status_input, i, 3)
            task_grid.addWidget(override_date, i, 4)

            self.task_rows.append({
                "task": task,
                "vendor": vendor_input,
                "auto_date": auto_date,
                "status": status_input,
                "override_date": override_date
            })

        layout.addLayout(task_grid)

        # Comments
        layout.addWidget(QLabel("Comments:"))
        self.comment_box = QTextEdit()
        layout.addWidget(self.comment_box)

        # Submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_form)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def submit_form(self):
        print("Unit:", self.unit_input.text())
        print("Property:", self.property_input.text())
        print("Move-Out:", self.mo_date.date().toPython())
        print("Move-In:", self.mi_date.date().toPython())
        print("Tasks:")
        for row in self.task_rows:
            print(
                row["task"], "| Vendor:", row["vendor"].currentText(),
                "| Auto-Date:", row["auto_date"].date().toPython(),
                "| Status:", row["status"].currentText(),
                "| Override:", row["override_date"].date().toPython()
            )
        print("Comments:", self.comment_box.toPlainText())
        QMessageBox.information(self, "Saved", "Task data submitted!")
        self.accept()