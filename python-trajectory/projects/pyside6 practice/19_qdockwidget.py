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
        self.setWindowTitle("QDockWidget demo")
        self.setCentralWidget(QTextEdit("Central"))
        dock = QDockWidget("Dock", self)
        dock.setWidget(QListWidget())
        self.addDockWidget(Qt.RightDockWidgetArea, dock)

if __name__ == "__main__":
    app = QApplication([])
    win = Demo()
    win.resize(600, 360)
    win.show()
    sys.exit(app.exec())
