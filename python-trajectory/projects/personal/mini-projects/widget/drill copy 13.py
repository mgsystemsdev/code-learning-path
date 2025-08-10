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
# DRILL 13: @Slot Decorator (Explicit)
# -------------------------------------
# We're using `@Slot` to make our methods explicitly Qt-compatible

class SlotDecorated(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drill 13 - Explicit Slot")
        layout = QVBoxLayout()

        self.input = QLineEdit()
        self.input.textChanged.connect(self.handle_change)

        layout.addWidget(self.input)
        self.setLayout(layout)

    @Slot(str)
    def handle_change(self, text):
        print(f"Decorated slot received: {text}")

app = QApplication(sys.argv)
window = SlotDecorated()
window.show()
sys.exit(app.exec())

# SUMMARY:
# - Used `@Slot(type)` to clarify signal compatibility
# - Best practice for larger apps or performance tuning
# - Not required but strengthens design discipline