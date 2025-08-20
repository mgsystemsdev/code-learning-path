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
        self.setWindowTitle("QStackedLayout demo")
        outer = QVBoxLayout(self)
        self.stack = QStackedLayout()
        self.stack.addWidget(QLabel("Page 1"))
        self.stack.addWidget(QLabel("Page 2"))
        outer.addLayout(self.stack)
        btn = QPushButton("Next")
        btn.clicked.connect(self.next_page)
        outer.addWidget(btn)

    def next_page(self):
        self.stack.setCurrentIndex((self.stack.currentIndex() + 1) % self.stack.count())

if __name__ == "__main__":
    app = QApplication([])
    w = Demo()
    w.resize(300, 200)
    w.show()
    sys.exit(app.exec())
