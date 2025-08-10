from PySide6.QtWidgets import (
    QDialog, QStackedLayout, QPushButton,
    QVBoxLayout, QLabel, QWidget, QLineEdit
)

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Dialog")

        layout = QVBoxLayout(self)
        self.stack = QStackedLayout()

        # View 1: Greeting
        view1 = QWidget()
        v1_layout = QVBoxLayout()
        v1_layout.addWidget(QLabel("👋 Welcome"))
        btn_next = QPushButton("Enter")
        btn_next.clicked.connect(lambda: self.stack.setCurrentWidget(view2))
        v1_layout.addWidget(btn_next)
        view1.setLayout(v1_layout)

        # View 2: Credentials
        view2 = QWidget()
        v2_layout = QVBoxLayout()
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        btn_validate = QPushButton("Validate")
        btn_validate.clicked.connect(lambda: self.stack.setCurrentWidget(view3))
        v2_layout.addWidget(self.username)
        v2_layout.addWidget(self.password)
        v2_layout.addWidget(btn_validate)
        view2.setLayout(v2_layout)

        # View 3: Launch button
        view3 = QWidget()
        v3_layout = QVBoxLayout()
        v3_layout.addWidget(QLabel("✅ Login Success"))
        btn_launch = QPushButton("Launch App")
        btn_launch.clicked.connect(self.accept)
        v3_layout.addWidget(btn_launch)
        view3.setLayout(v3_layout)

        self.stack.addWidget(view1)
        self.stack.addWidget(view2)
        self.stack.addWidget(view3)

        layout.addLayout(self.stack)
        self.stack.setCurrentWidget(view1)
