
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QGroupBox, QLineEdit
)
import sys


# -------------------------------------
# DRILL 8: Pre-Named Widget Tree
# -------------------------------------
# We're declaring all widgets as attributes in a setup method

class ProfileWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drill 8 - Named Widget Tree")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.name_field = QLineEdit()
        self.name_field.setPlaceholderText("Enter name")

        self.email_field = QLineEdit()
        self.email_field.setPlaceholderText("Enter email")

        self.submit_button = QPushButton("Submit")

        layout.addWidget(self.name_field)
        layout.addWidget(self.email_field)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

app = QApplication(sys.argv)
window = ProfileWindow()
window.show()
sys.exit(app.exec())

# SUMMARY:
# - Structured widget tree inside a reusable class
# - All child widgets stored on self
# - Enables full state access and future logic injection