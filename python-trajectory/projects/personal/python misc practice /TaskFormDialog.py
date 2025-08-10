from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox,
    QDateEdit, QTextEdit, QPushButton, QFormLayout, QMessageBox
)
from PySide6.QtCore import QDate
import datetime

class TaskFormDialog(QDialog):
    def __init__(self, unit_number=""):
        super().__init__()
        self.setWindowTitle("Start Make Ready – Task Entry")
        self.setMinimumWidth(400)
        self.unit_number = unit_number

        layout = QVBoxLayout()
        form = QFormLayout()

        # Header fields
        self.unit_input = QLineEdit(self.unit_number)
        self.property_input = QLineEdit()
        self.mo_date = QDateEdit()
        self.mo_date.setCalendarPopup(True)
        self.mi_date = QDateEdit()
        self.mi_date.setCalendarPopup(True)

        form.addRow("Unit:", self.unit_input)
        form.addRow("Property:", self.property_input)
        form.addRow("Move-Out Date:", self.mo_date)
        form.addRow("Move-In Date:", self.mi_date)

        # Task row: Paint (example, others can be added same way)
        self.paint_status = QComboBox()
        self.paint_status.addItems(["Not Started", "Scheduled", "In Progress", "Blocked", "✅ Done"])

        self.paint_vendor = QLineEdit()
        self.paint_date = QDateEdit()
        self.paint_date.setCalendarPopup(True)
        self.paint_date.setDate(QDate.currentDate())

        form.addRow("Paint – Status:", self.paint_status)
        form.addRow("Paint – Vendor:", self.paint_vendor)
        form.addRow("Paint – Date:", self.paint_date)

        # Comment box
        self.comment_box = QTextEdit()
        form.addRow("Comments:", self.comment_box)

        # Submit button
        self.submit_button = QPushButton("Submit Task Form")
        self.submit_button.clicked.connect(self.submit_form)

        layout.addLayout(form)
        layout.addWidget(self.submit_button)
        self.setLayout(layout)

    def submit_form(self):
        unit = self.unit_input.text().strip()
        property_name = self.property_input.text().strip()
        mo = self.mo_date.date().toPython()
        mi = self.mi_date.date().toPython()
        paint_status = self.paint_status.currentText()
        paint_vendor = self.paint_vendor.text().strip()
        paint_date = self.paint_date.date().toPython()
        comment = self.comment_box.toPlainText().strip()

        if not unit or not property_name:
            QMessageBox.warning(self, "Missing Info", "Unit and Property are required.")
            return

        # Placeholder save action
        print("Saving form data:")
        print(f"Unit: {unit}, Property: {property_name}")
        print(f"Move-Out: {mo}, Move-In: {mi}")
        print(f"Paint: {paint_status}, {paint_vendor}, {paint_date}")
        print(f"Comment: {comment}")
        QMessageBox.information(self, "Success", "Form submitted successfully!")
        self.accept()