
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit,
    QVBoxLayout, QHBoxLayout
)
import sys


# -------------------------------------
# DRILL 27: Self-Updating Component
# -------------------------------------
# We're embedding logic directly inside a reusable component

class CounterWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()

        self.count = 0
        self.label = QLabel("0")
        button = QPushButton("Add")

        button.clicked.connect(self.increment)

        layout.addWidget(self.label)
        layout.addWidget(button)
        self.setLayout(layout)

    def increment(self):
        self.count += 1
        self.label.setText(str(self.count))

app = QApplication(sys.argv)
window = CounterWidget()
window.setWindowTitle("Drill 27 - Logic in Component")
window.show()
sys.exit(app.exec())

# SUMMARY:
# - Encapsulated behavior (counter) inside widget class
# - Exposed no internal state externally
# - Builds self-contained logic units