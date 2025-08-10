from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
)
from PySide6.QtCore import Signal, Slot
import sys

# -------------------------------------
# DRILL 34: Signal Triggered from Internal Slot
# -------------------------------------
# We're chaining slot → signal for internal processing before emitting

class NameBroadcaster(QWidget):
    nameEntered = Signal(str)

    def __init__(self):
        super().__init__()
        self.input = QPushButton("Submit 'Alice'")
        self.input.clicked.connect(self.process_input)

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        self.setLayout(layout)

    def process_input(self):
        name = "Alice"  # Simulated user input
        print("Internal prep logic")
        self.nameEntered.emit(name)

app = QApplication(sys.argv)
broadcaster = NameBroadcaster()
broadcaster.nameEntered.connect(lambda name: print("Name:", name))
broadcaster.setWindowTitle("Drill 34 - Slot Before Emit")
broadcaster.show()
sys.exit(app.exec())

# SUMMARY:
# - Introduced internal processing before signal emit
# - Keeps UI flexible — logic runs, then signal broadcasts
# - Supports smart emitters, not just forwarders