from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
import sys

# -------------------------------------
# DRILL 1: Single Widget, Manual Show
# -------------------------------------
# We're creating a base-level widget that renders a single button manually

app = QApplication(sys.argv)
window = QWidget()  # Primary container
button = QPushButton("Click Me")  # Child widget manually constructed

window.setWindowTitle("Drill 1 - Manual Button")  # Declare window identity
button.setParent(window)  # Manual parenting

window.show()  # Render to screen
sys.exit(app.exec())
