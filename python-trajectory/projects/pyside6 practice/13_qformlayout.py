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
        self.setWindowTitle("QFormLayout demo")
        form = QFormLayout(self)
        form.addRow("Name:", QLineEdit())
        form.addRow("Age:", QSpinBox())
        form.addRow("Subscribe:", QCheckBox("Yes"))

if __name__ == "__main__":
    app = QApplication([])
    w = Demo()
    w.resize(360, 180)
    w.show()
    sys.exit(app.exec())
