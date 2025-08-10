
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QGroupBox, QLineEdit
)
import sys


# -------------------------------------
# DRILL 9: Deep Nesting with Multiple GroupBoxes
# -------------------------------------
# We're creating multiple widget groups to simulate complex panel structures

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drill 9 - Deep Group Nesting")

        layout = QVBoxLayout()

        general_group = QGroupBox("General")
        general_layout = QVBoxLayout()
        general_layout.addWidget(QLineEdit("Username"))
        general_layout.addWidget(QLineEdit("Language"))
        general_group.setLayout(general_layout)

        advanced_group = QGroupBox("Advanced")
        advanced_layout = QVBoxLayout()
        advanced_layout.addWidget(QLineEdit("Token"))
        advanced_layout.addWidget(QLineEdit("Path"))
        advanced_group.setLayout(advanced_layout)

        layout.addWidget(general_group)
        layout.addWidget(advanced_group)
        layout.addWidget(QPushButton("Save"))

        self.setLayout(layout)

app = QApplication(sys.argv)
window = SettingsWindow()
window.show()
sys.exit(app.exec())

# SUMMARY:
# - Created a nested UI with multiple visual groups
# - Encodes real-world configuration panel structures
# - Promotes readability, testability, and maintainability