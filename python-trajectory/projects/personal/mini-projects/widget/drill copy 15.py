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
# DRILL 15: Inline Lambda Slot
# -------------------------------------
# We're wiring quick behavior inline for temporary or simple triggers

class InlineSlot(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drill 15 - Lambda Slot")
        layout = QVBoxLayout()

        label = QLabel("Waiting...")
        btn = QPushButton("Set Message")

        btn.clicked.connect(lambda: label.setText("Lambda Triggered"))

        layout.addWidget(label)
        layout.addWidget(btn)
        self.setLayout(layout)

app = QApplication(sys.argv)
window = InlineSlot()
window.show()
sys.exit(app.exec())

# SUMMARY:
# - Used `lambda` to inject logic without defining method
# - Great for tiny UIs or temporary events
# - Caution: Avoid for complex logic or reuse cases