from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
)
from PySide6.QtCore import Signal, Slot
import sys


# -------------------------------------
# DRILL 35: Forward Signal from One Widget to Another
# -------------------------------------
# We're relaying an internal signal outward for chaining

class SignalRelay(QWidget):
    output = Signal(str)

    def __init__(self):
        super().__init__()
        self.inner = DataSender()
        self.inner.messageSent.connect(self.output)  # Relay pattern

        layout = QVBoxLayout()
        layout.addWidget(self.inner)
        self.setLayout(layout)

app = QApplication(sys.argv)
relayer = SignalRelay()
relayer.output.connect(lambda msg: print("Relayed:", msg))
relayer.setWindowTitle("Drill 35 - Signal Relay")
relayer.show()
sys.exit(app.exec())