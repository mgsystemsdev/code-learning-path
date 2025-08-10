# ============================================================
#  File:        gui_login.py
#  Author:      Miguel Gonzalez Almonte
#  Created:     2025-06-03
#  Description: Secure login dialog that launches multiple UI options
# ============================================================

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QApplication
)
from constants import VALID_USERS
from gui_main_tk import launch_tk_main_gui  # Safe: no PySide dependency


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Training Python 🐍 Board")
        self.setFixedSize(300, 350)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("🐍 Welcome to your Training Board!\nClick below to get started.")
        self.layout.addWidget(self.label)

        self.enter_button = QPushButton("Enter")
        self.enter_button.clicked.connect(self.show_login_fields)
        self.layout.addWidget(self.enter_button)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.check_login)

        self.qt_button = QPushButton("Launch PySide6 GUI")
        self.qt_button.clicked.connect(self.launch_qt)
        self.qt_button.hide()

        self.tk_button = QPushButton("Launch Tkinter GUI")
        self.tk_button.clicked.connect(self.launch_tk)
        self.tk_button.hide()

        self.qt_demo_button = QPushButton("Launch PySide6 Showcase")
        self.qt_demo_button.clicked.connect(self.launch_qt_demo)
        self.qt_demo_button.hide()

        self.tk_demo_button = QPushButton("Launch Tkinter Showcase")
        self.tk_demo_button.clicked.connect(self.launch_tk_demo)
        self.tk_demo_button.hide()

        self.user = None
        self.launch_target = None
        self.demo_window = None

    def show_login_fields(self):
        self.label.setText("🔐 Please enter your credentials:")
        self.enter_button.hide()
        self.layout.addWidget(self.username)
        self.layout.addWidget(self.password)
        self.layout.addWidget(self.login_button)

    def check_login(self):
        user = self.username.text()
        pw = self.password.text()

        if user in VALID_USERS and VALID_USERS[user] == pw:
            self.user = user
            self.label.setText(f"✅ Welcome, {user}!")
            self.username.hide()
            self.password.hide()
            self.login_button.hide()

            self.layout.addWidget(self.qt_button)
            self.layout.addWidget(self.tk_button)
            self.layout.addWidget(self.qt_demo_button)
            self.layout.addWidget(self.tk_demo_button)

            self.qt_button.show()
            self.tk_button.show()
            self.qt_demo_button.show()
            self.tk_demo_button.show()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

    def get_user(self):
        return self.user

    def launch_qt(self):
        self.launch_target = "qt"
        self.accept()

    def launch_tk(self):
        self.launch_target = "tk"
        self.accept()

        app = QApplication.instance()
        if app:
            app.exec()

    def launch_tk_demo(self):
        import subprocess
        subprocess.Popen(["python3", "gui_demo_tk.py"])
        self.hide()
