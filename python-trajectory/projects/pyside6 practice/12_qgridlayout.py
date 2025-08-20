# NOTE:
# This demo uses PySide6 (Qt for Python).
# If you prefer PyQt5/PyQt6, you can switch imports accordingly.
# Each script is standalone: run with `python this_file.py`.

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QGridLayout demo")
        grid = QGridLayout(self)
        grid.addWidget(QLabel("R0C0"), 0, 0)
        grid.addWidget(QPushButton("R0C1"), 0, 1)
        grid.addWidget(QLabel("R1C0"), 1, 0)
        grid.addWidget(QLineEdit("R1C1"), 1, 1)

if __name__ == "__main__":
    app = QApplication([])
    w = Demo()
    w.resize(420, 200)
    w.show()
    sys.exit(app.exec())
