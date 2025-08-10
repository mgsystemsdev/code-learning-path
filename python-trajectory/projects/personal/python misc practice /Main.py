from PySide6.QtWidgets import QMainWindow, QLabel

class MainWindow(QMainWindow):
    def __init__(self, mode):
        super().__init__()
        self.setWindowTitle("Main Application")
        self.setCentralWidget(QLabel(f"🧠 App running in mode: {mode}"))
