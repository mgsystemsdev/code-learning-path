# NOTE:
# This demo uses PySide6 (Qt for Python).
# If you prefer PyQt5/PyQt6, you can switch imports accordingly.
# Each script is standalone: run with `python this_file.py`.

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class DemoMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QMainWindow demo")
        # Built-ins
        self.setMenuBar(QMenuBar())
        file_menu = self.menuBar().addMenu("File")
        file_menu.addAction("Exit", self.close)

        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        toolbar.addAction("Hello", lambda: self.statusBar().showMessage("Hello"))

        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Ready")

        # Central widget + layout + sample widgets
        central = QWidget()
        lay = QVBoxLayout(central)
        lay.addWidget(QLabel("Central area"))
        lay.addWidget(QPushButton("Click me"))
        self.setCentralWidget(central)

        # Dock
        dock = QDockWidget("Dock", self)
        dock.setWidget(QLabel("Dockable panel"))
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

if __name__ == "__main__":
    app = QApplication([])
    win = DemoMainWindow()
    win.resize(520, 320)
    win.show()
    sys.exit(app.exec())
