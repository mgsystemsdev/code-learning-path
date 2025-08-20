# NOTE:
# This demo uses PySide6 (Qt for Python).
# If you prefer PyQt5/PyQt6, you can switch imports accordingly.
# Each script is standalone: run with `python this_file.py`.

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class DemoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QWidget demo")
        lay = QHBoxLayout(self)
        lay.addWidget(QLabel("A simple container"))
        lay.addWidget(QPushButton("Button"))

if __name__ == "__main__":
    app = QApplication([])
    w = DemoWidget()
    w.resize(420, 180)
    w.show()
    sys.exit(app.exec())
