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
# DRILL 11: Button Connected to Method
# -------------------------------------
# We're connecting a QPushButton to a method using `.clicked.connect(...)`

class ClickWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drill 11 - Basic Slot")
        layout = QVBoxLayout()

        self.label = QLabel("Press the button")
        self.button = QPushButton("Click Me")
        self.button.clicked.connect(self.on_button_clicked)

        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def on_button_clicked(self):
        self.label.setText("Button was clicked!")

app = QApplication(sys.argv)
window = ClickWindow()
window.show()
sys.exit(app.exec())

# SUMMARY:
# - Connected QPushButton click to custom method
# - Modified QLabel inside slot
# - Introduced the "signal-to-slot" pattern for UI behavior injection