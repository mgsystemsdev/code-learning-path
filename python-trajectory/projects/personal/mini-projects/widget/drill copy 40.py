from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
)
from PySide6.QtCore import Signal, Slot
import sys


# -------------------------------------
# DRILL 40: Behavior Injection per Instance
# -------------------------------------
# We're using one widget class but injecting different logic per use

class ActionButton(QWidget):
    def __init__(self, label, on_click):
        super().__init__()
        btn = QPushButton(label)
        btn.clicked.connect(on_click)

        layout = QVBoxLayout()
        layout.addWidget(btn)
        self.setLayout(layout)

def alert_one():
    print("Logic 1 activated!")

def alert_two():
    print("Logic 2 activated!")

app = QApplication(sys.argv)
w1 = ActionButton("Run 1", alert_one)
w2 = ActionButton("Run 2", alert_two)

host = QWidget()
layout = QVBoxLayout()
layout.addWidget(w1)
layout.addWidget(w2)
host.setLayout(layout)
host.setWindowTitle("Drill 40 - Behavior Per Instance")
host.show()
sys.exit(app.exec())

# SUMMARY:
# - Same view logic, different behavior per instantiation
# - Promotes true component reuse
# - Precursor to factory or DI-based architecture