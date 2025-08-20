# NOTE:
# This demo uses PySide6 (Qt for Python).
# If you prefer PyQt5/PyQt6, you can switch imports accordingly.
# Each script is standalone: run with `python this_file.py`.

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class Demo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QMdiSubWindow within QMdiArea")
        mdi = QMdiArea()
        self.setCentralWidget(mdi)
        sub1 = QMdiSubWindow()
        sub1.setWidget(QTextEdit("Subwindow 1"))
        mdi.addSubWindow(sub1)
        sub1.show()

if __name__ == "__main__":
    app = QApplication([])
    win = Demo()
    win.resize(600, 380)
    win.show()
    sys.exit(app.exec())
