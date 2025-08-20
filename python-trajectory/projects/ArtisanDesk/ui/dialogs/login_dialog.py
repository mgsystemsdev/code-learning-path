
# Created:     2025-05-20
# File:        login.py
# Description: Entry screen with login form; unlocks launch options after authentication

from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox
)
from main import MainAppWindow  # ✅ Fixed path (no circular import)


class LoginScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Unit Turn - Login")
        self.setFixedSize(220, 150)

        self.label = QLabel("Welcome to Unit Turn")

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.login_button = QPushButton("Log In")
        self.login_button.clicked.connect(self.verify_login)
        self.login_button.setDefault(True)

        self.launch_button = QPushButton("Launch App")
        self.launch_button.clicked.connect(self.launch_main_app)

        self.coming_soon_button = QPushButton("Coming Soon")
        self.coming_soon_button.clicked.connect(self.show_coming_soon)

        self.launch_button.hide()
        self.coming_soon_button.hide()

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.username)
        layout.addWidget(self.login_button)
        layout.addWidget(self.launch_button)
        layout.addWidget(self.coming_soon_button)

        self.setLayout(layout)

    def verify_login(self):
        if self.username.text() == "admin":
            self.username.hide()
            self.login_button.hide()
            self.label.setText("Welcome Admin")

            self.launch_button.show()
            self.coming_soon_button.show()

    def show_coming_soon(self):
        msg = QMessageBox()
        msg.setWindowTitle("Coming Soon")
        msg.setText("This feature is not available yet.")
        msg.setIcon(QMessageBox.Information)
        msg.exec()

    def launch_main_app(self):
        self.main_window = MainAppWindow()
        self.main_window.show()
        self.close()
