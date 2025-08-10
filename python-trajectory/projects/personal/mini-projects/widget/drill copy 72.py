from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
import sys


app = QApplication(sys.argv)
window = QWidget()

window.setLayout(
    QVBoxLayout()  # Layout created inline
)
window.layout().addWidget(QLabel("Hello"))
window.layout().addWidget(QPushButton("Go"))

window.setWindowTitle("Drill 4 - Inline Layout")
window.show()
sys.exit(app.exec())