# NOTE:
# This demo uses PySide6 (Qt for Python).
# If you prefer PyQt5/PyQt6, you can switch imports accordingly.
# Each script is standalone: run with `python this_file.py`.

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class MinimalWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QApplication demo")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("This script shows the minimal QApplication + QWidget."))
        layout.addWidget(QPushButton("OK"))

if __name__ == "__main__":
    app = QApplication([])
    w = MinimalWindow()
    w.resize(360, 160)
    w.show()
    sys.exit(app.exec())
