# ===============================
# DRILL BLOCK: SK31-B03
# Logic Injection via Signals & Slots
# ===============================

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit
)
from PySide6.QtCore import Slot
import sys


# -------------------------------------
# DRILL 12: Updating Label from LineEdit
# -------------------------------------
# We're triggering updates based on user input in QLineEdit

class InputReflector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drill 12 - Reflect Text")
        layout = QVBoxLayout()

        self.input = QLineEdit()
        self.output = QLabel("Waiting for input")

        self.input.textChanged.connect(self.update_output)

        layout.addWidget(self.input)
        layout.addWidget(self.output)
        self.setLayout(layout)

    def update_output(self, text):
        self.output.setText(f"Entered: {text}")

app = QApplication(sys.argv)
window = InputReflector()
window.show()
sys.exit(app.exec())

# SUMMARY:
# - Bound `textChanged` signal to a label update
# - Captured signal arguments (text)
# - Reinforces reactive UI building