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
        self.setWindowTitle("QProgressBar demo")
        lay = QVBoxLayout(self)
        self.bar = QProgressBar()
        lay.addWidget(self.bar)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(50)

    def tick(self):
        v = (self.bar.value() + 1) % 101
        self.bar.setValue(v)

if __name__ == "__main__":
    app = QApplication([])
    w = Demo()
    w.resize(300, 100)
    w.show()
    sys.exit(app.exec())
