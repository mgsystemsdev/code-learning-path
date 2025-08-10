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
# DRILL 14: Reusable Button Callback
# -------------------------------------
# We're attaching the same method to multiple buttons, using sender()

class MultiTrigger(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drill 14 - Shared Slot")
        layout = QVBoxLayout()

        self.result = QLabel("Press any button")

        for label in ["A", "B", "C"]:
            btn = QPushButton(f"Button {label}")
            btn.clicked.connect(self.handle_click)
            layout.addWidget(btn)

        layout.addWidget(self.result)
        self.setLayout(layout)

    def handle_click(self):
        sender = self.sender()
        self.result.setText(f"You clicked: {sender.text()}")

app = QApplication(sys.argv)
window = MultiTrigger()
window.show()
sys.exit(app.exec())

# SUMMARY:
# - Used `self.sender()` to determine which button triggered event
# - Avoids needing one method per button
# - Key for DRY interaction logic