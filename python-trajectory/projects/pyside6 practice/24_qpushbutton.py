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
        self.setWindowTitle("QPushButton demo")
        lay = QVBoxLayout(self)
        btn = QPushButton("Press me")
        btn.clicked.connect(lambda: QMessageBox.information(self, "Clicked", "Button pressed"))
        lay.addWidget(btn)

if __name__ == "__main__":
    app = QApplication([])
    w = Demo()
    w.show()
    sys.exit(app.exec())
