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
        self.setWindowTitle("QTreeWidget demo")
        lay = QVBoxLayout(self)
        tw = QTreeWidget()
        tw.setHeaderLabels(["Name", "Value"])
        parent = QTreeWidgetItem(["Settings", ""])
        child = QTreeWidgetItem(["Theme", "Dark"])
        parent.addChild(child)
        tw.addTopLevelItem(parent)
        lay.addWidget(tw)

if __name__ == "__main__":
    app = QApplication([])
    w = Demo()
    w.resize(420, 260)
    w.show()
    sys.exit(app.exec())
