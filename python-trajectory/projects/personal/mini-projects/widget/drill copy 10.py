
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QGroupBox, QLineEdit
)
import sys

# -------------------------------------
# DRILL 10: Utility Method for Widget Creation
# -------------------------------------
# We're abstracting widget creation into reusable helper methods

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drill 10 - Utility Creation")
        self.setup_ui()

    def make_line_edit(self, placeholder):
        line = QLineEdit()
        line.setPlaceholderText(placeholder)
        return line

    def setup_ui(self):
        layout = QVBoxLayout()
        self.user = self.make_line_edit("Username")
        self.passw = self.make_line_edit("Password")
        login_btn = QPushButton("Login")

        layout.addWidget(self.user)
        layout.addWidget(self.passw)
        layout.addWidget(login_btn)
        self.setLayout(layout)

app = QApplication(sys.argv)
window = LoginWindow()
window.show()
sys.exit(app.exec())

# SUMMARY:
# - Abstracted common widget creation into helper
# - Reduces duplication, improves consistency
# - Builds foundation for component-based design