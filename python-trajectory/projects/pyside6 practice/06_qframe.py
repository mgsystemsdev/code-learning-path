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
        self.setWindowTitle("QFrame demo")
        lay = QVBoxLayout(self)
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setFrameShadow(QFrame.Sunken)
        fl = QVBoxLayout(frame)
        fl.addWidget(QLabel("Inside a framed area"))
        fl.addWidget(QPushButton("Do thing"))
        lay.addWidget(frame)

if __name__ == "__main__":
    app = QApplication([])
    w = Demo()
    w.resize(420, 220)
    w.show()
    sys.exit(app.exec())
