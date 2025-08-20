# login_dialog.py
# Three-stage unified QDialog with real login and correct layout clearing

import json
from PySide6.QtWidgets import (
    QDialog, QLabel, QPushButton, QVBoxLayout,
    QLineEdit, QMessageBox, QHBoxLayout
)

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Training Python Board")
        self.resize(400, 200)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.show_welcome()

    def clear_layout(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            child_layout = item.layout()

            if widget:
                widget.setParent(None)
            elif child_layout:
                while child_layout.count():
                    child = child_layout.takeAt(0)
                    if child.widget():
                        child.widget().setParent(None)

    def show_welcome(self):
        self.clear_layout()
        label = QLabel("Welcome to Training Python Board")
        btn = QPushButton("Enter")
        btn.clicked.connect(self.show_login)
        self.layout.addWidget(label)
        self.layout.addWidget(btn)

    def show_login(self):
        self.clear_layout()

        user_row = QHBoxLayout()
        user_label = QLabel("Username:")
        self.username_input = QLineEdit()
        user_row.addWidget(user_label)
        user_row.addWidget(self.username_input)

        pass_row = QHBoxLayout()
        pass_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        pass_row.addWidget(pass_label)
        pass_row.addWidget(self.password_input)

        btn = QPushButton("Enter")
        btn.clicked.connect(self.validate_login)

        self.password_input.returnPressed.connect(self.validate_login)  # ⏎ Enter key triggers login

        self.layout.addLayout(user_row)
        self.layout.addLayout(pass_row)
        self.layout.addWidget(btn)

    def validate_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        try:
            with open("system/users.json", "r", encoding="utf-8") as f:
                users = json.load(f)
        except Exception:
            users = {}

        if username in users and users[username] == password:
            self.username_input.clear()
            self.password_input.clear()
            self.show_mode_select()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
            self.username_input.clear()
            self.password_input.clear()
            self.username_input.setFocus()

    def show_mode_select(self):
        self.clear_layout()
        label = QLabel("Choose GUI Mode")
        btn_qt = QPushButton("PySide6 Showcase")
        btn_tk = QPushButton("Tkinter Showcase")
        btn_adv = QPushButton("🔧 Advanced GUI Projects")

        btn_qt.clicked.connect(lambda: self.set_mode("qt"))
        btn_tk.clicked.connect(lambda: self.set_mode("tk"))
        btn_adv.clicked.connect(self.show_advanced_dialog)

        self.layout.addWidget(label)
        self.layout.addWidget(btn_qt)
        self.layout.addWidget(btn_tk)
        self.layout.addWidget(btn_adv)

    def show_advanced_dialog(self):
        self.clear_layout()
        label = QLabel("🔧 Advanced GUI Projects")
        btn_canvas = QPushButton("🎨 QPainter Canvas")
        btn_qml = QPushButton("⚡ QML / QtQuick")

        btn_canvas.clicked.connect(lambda: self.show_coming_soon("QPainter Canvas"))
        btn_qml.clicked.connect(lambda: self.show_coming_soon("QML / QtQuick"))

        self.layout.addWidget(label)
        self.layout.addWidget(btn_canvas)
        self.layout.addWidget(btn_qml)

    def show_coming_soon(self, topic):
        QMessageBox.information(self, "Coming Soon", f"{topic} is coming soon!")

    def set_mode(self, mode):
        data = {
            "launch_target": mode,
            "api_mode": "none"
        }
        with open("system/modes.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        self.accept()
