from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
import sys




# -------------------------------------
# DRILL 5: Encapsulated Window Class
# -------------------------------------
# We're wrapping the logic into a reusable, testable QWidget subclass

class HelloWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drill 5 - Encapsulated Class")

        layout = QVBoxLayout()
        self.label = QLabel("Encapsulated Hello")
        self.button = QPushButton("Do Something")

        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

# App start
app = QApplication(sys.argv)
window = HelloWindow()
window.show()
sys.exit(app.exec())