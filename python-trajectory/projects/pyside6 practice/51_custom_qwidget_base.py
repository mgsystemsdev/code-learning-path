# NOTE:
# This demo uses PySide6 (Qt for Python).
# If you prefer PyQt5/PyQt6, you can switch imports accordingly.
# Each script is standalone: run with `python this_file.py`.

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class CustomWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom QWidget base demo")
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel("Subclass QWidget for custom behavior"))
        btn = QPushButton("Do custom thing")
        btn.clicked.connect(lambda: QMessageBox.information(self, "Custom", "Hello from subclass"))
        lay.addWidget(btn)

if __name__ == "__main__":
    app = QApplication([])
    w = CustomWidget()
    w.resize(420, 220)
    w.show()
    sys.exit(app.exec())
