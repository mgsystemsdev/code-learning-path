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
        self.setWindowTitle("QMenuBar demo")
        bar = QMenuBar(self)
        self.setMenuBar(bar)
        file_menu = bar.addMenu("File")
        file_menu.addAction("Say Hi", lambda: QMessageBox.information(self, "Hi", "Hello from QMenuBar"))
        file_menu.addAction("Exit", self.close)
        self.setCentralWidget(QLabel("See the menubar above"))

if __name__ == "__main__":
    app = QApplication([])
    win = Demo()
    win.resize(420, 200)
    win.show()
    sys.exit(app.exec())
