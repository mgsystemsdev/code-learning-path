from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
import sys



app = QApplication(sys.argv)
window = QWidget()
layout = QVBoxLayout()

label = QLabel("Welcome")
label.setObjectName("main_label")  # Declarative ID
button = QPushButton("OK")
button.setObjectName("submit_button")

layout.addWidget(label)
layout.addWidget(button)

window.setLayout(layout)
window.setWindowTitle("Drill 3 - Named Widgets")
window.show()
sys.exit(app.exec())