from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
)
from PySide6.QtCore import Signal, Slot
import sys


# -------------------------------------
# DRILL 33: Cross-Component Communication
# -------------------------------------
# We're connecting one widget's signal to another's method

class InputField(QWidget):
    valueChanged = Signal(str)

    def __init__(self):
        super().__init__()
        self.input = QPushButton("Send 'Hi'")
        self.input.clicked.connect(lambda: self.valueChanged.emit("Hi"))

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        self.setLayout(layout)

class MirrorDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel("Waiting...")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    @Slot(str)
    def update_label(self, text):
        self.label.setText(text)

app = QApplication(sys.argv)
sender = InputField()
receiver = MirrorDisplay()

# Connect cross-component
sender.valueChanged.connect(receiver.update_label)

# Host both widgets
host = QWidget()
layout = QVBoxLayout()
layout.addWidget(sender)
layout.addWidget(receiver)
host.setLayout(layout)
host.setWindowTitle("Drill 33 - Cross-Component Signal")
host.show()
sys.exit(app.exec())

# SUMMARY:
# - Connected emitter to receiver across components
# - Achieved clean, logic-free glue layer
# - UI now composes like a system, not a page