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
        self.setWindowTitle("QMenu demo (context menu)")
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_menu)
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel("Right-click to open a QMenu"))

    def show_menu(self, pos):
        menu = QMenu(self)
        menu.addAction("Action A", lambda: QMessageBox.information(self, "Action", "A"))
        menu.addAction("Action B", lambda: QMessageBox.information(self, "Action", "B"))
        menu.exec(self.mapToGlobal(pos))

if __name__ == "__main__":
    app = QApplication([])
    w = Demo()
    w.resize(420, 200)
    w.show()
    sys.exit(app.exec())
