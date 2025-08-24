

from PySide6.QtWidgets import QMainWindow, QStackedWidget, QPushButton,QVBoxLayout
from ui.screens.show_new_window import NewWindow 
class MainAppWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ArtisanDesk – Dashboard")

        self.stack = QStackedWidget()

        self.btn = QPushButton("New Window")
        self.btn.clicked.connect(self.open_new_window)
        layout = QVBoxLayout()
        layout.addWidget(self.btn)


        self.stack.addWidget(self.btn)  # Adds button as first screen
        self.setCentralWidget(self.stack)

    def open_new_window(self):
        dlg = NewWindow()
        dlg.show()


