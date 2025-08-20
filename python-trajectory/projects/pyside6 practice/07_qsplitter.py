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
        self.setWindowTitle("QSplitter demo")
        lay = QVBoxLayout(self)
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(QTextEdit("Left"))
        splitter.addWidget(QTextEdit("Right"))
        lay.addWidget(splitter)

if __name__ == "__main__":
    app = QApplication([])
    w = Demo()
    w.resize(520, 320)
    w.show()
    sys.exit(app.exec())
