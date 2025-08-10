
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QGroupBox, QLineEdit
)
import sys


# -------------------------------------
# DRILL 7: GroupBox for Visual and Logical Grouping
# -------------------------------------
# We're grouping related widgets inside a labeled container

app = QApplication(sys.argv)
window = QWidget()
main_layout = QVBoxLayout()

form_group = QGroupBox("User Info")
form_layout = QVBoxLayout()
form_layout.addWidget(QLineEdit("Name"))
form_layout.addWidget(QLineEdit("Email"))
form_group.setLayout(form_layout)

main_layout.addWidget(form_group)
main_layout.addWidget(QPushButton("Submit"))

window.setLayout(main_layout)
window.setWindowTitle("Drill 7 - GroupBox Pattern")
window.show()
sys.exit(app.exec())

# SUMMARY:
# - Introduced QGroupBox to visually group related widgets
# - Encourages logic modularity and visual clarity
# - Ideal for forms, settings panels, and multi-step inputs