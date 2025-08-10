# Author:      Miguel Gonzalez Almonte  
# Created:     2025-05-24  
# File:        main.py  
# Description: Main application window shell

from PySide6.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout

class MainAppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Application")
        self.resize(500, 900)

        central_widget = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Welcome to the main app screen")
        layout.addWidget(label)


        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
