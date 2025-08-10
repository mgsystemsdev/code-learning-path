from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QWidget

class NewWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ArtisanDesk — Dashboard Dialog")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("This is a new dialog window."))
        self.setLayout(layout)
