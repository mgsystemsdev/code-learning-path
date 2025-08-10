from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
)
from PySide6.QtCore import Signal, Slot
import sys

# -------------------------------------
# DRILL 31: Create a Simple Custom Signal
# -------------------------------------
# We're declaring a custom signal inside a QWidget subclass

class ClickEmitter(QWidget):
    clicked = Signal()  # Declare signal

    def __init__(self):
        super().__init__()
        btn = QPushButton("Emit Signal")
        btn.clicked.connect(self.clicked.emit)  # Wire internal event to emit

        layout = QVBoxLayout()
        layout.addWidget(btn)
        self.setLayout(layout)

app = QApplication(sys.argv)
emitter = ClickEmitter()
emitter.clicked.connect(lambda: print("Signal received!"))
emitter.setWindowTitle("Drill 31 - Custom Signal")
emitter.show()
sys.exit(app.exec())

# SUMMARY:
# - Created a `Signal()` member
# - Connected it to a QPushButton internally
# - Broadcasts event that any outside listener can hook into
