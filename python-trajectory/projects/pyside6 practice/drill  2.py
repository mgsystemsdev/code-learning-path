from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
import sys

app = QApplication(sys.argv)
window = QWidget()
layout = QVBoxLayout()  # Layout manager

label = QLabel("Label Above")
button = QPushButton("Click Me")

layout.addWidget(label)   # Structure begins
layout.addWidget(button)  # Structure grows

window.setLayout(layout)  # Layout installed
window.setWindowTitle("Drill 2 - VBox Structure")
window.show()
sys.exit(app.exec())