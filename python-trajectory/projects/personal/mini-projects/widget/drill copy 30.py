
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit,
    QVBoxLayout, QHBoxLayout
)
import sys


# -------------------------------------
# DRILL 30: Output Value from Custom Widget
# -------------------------------------
# We're exposing component state so outside world can use it

class NameField(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Name"))
        self.input = QLineEdit()
        layout.addWidget(self.input)
        self.setLayout(layout)

    def get_name(self):
        return self.input.text()

app = QApplication(sys.argv)
form = NameField()
form.setWindowTitle("Drill 30 - Exposed Value")
form.show()
sys.exit(app.exec())

# SUMMARY:
# - Defined a public method to read internal widget state
# - Balances encapsulation and access
# - Enables safe logic access from controller or host
