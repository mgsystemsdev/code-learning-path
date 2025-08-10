from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
)
from PySide6.QtCore import Signal, Slot
import sys

# -------------------------------------
# DRILL 32: Signal with Data Argument
# -------------------------------------
# We're sending data along with the signal

class DataSender(QWidget):
    messageSent = Signal(str)  # Custom signal with data

    def __init__(self):
        super().__init__()
        self.label = QLabel("No message yet")
        btn = QPushButton("Send Hello")
        btn.clicked.connect(self.send_message)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(btn)
        self.setLayout(layout)

    def send_message(self):
        self.messageSent.emit("Hello from component")

app = QApplication(sys.argv)
sender = DataSender()
sender.messageSent.connect(lambda msg: print("Received:", msg))
sender.setWindowTitle("Drill 32 - Signal with Data")
sender.show()
sys.exit(app.exec())

# SUMMARY:
# - Custom signal now sends string payload
# - External systems can respond contextually
# - Enables UI to emit event-driven data