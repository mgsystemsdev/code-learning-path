
# ===============================
# DRILL BLOCK: SK31-B04
# Styling and Themes via CSS and Object Names
# ===============================

from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit
)
import sys


# -------------------------------------
# DRILL 20: Runtime Theming Swap
# -------------------------------------
# We're switching styles on button click

class ThemeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drill 20 - Theme Swap")
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout()
        self.label = QLabel("Themed UI")
        self.button = QPushButton("Toggle Theme")
        self.button.clicked.connect(self.toggle_theme)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.dark_mode = False
        self.apply_theme()

    def apply_theme(self):
        if self.dark_mode:
            self.setStyleSheet("""
                QWidget { background-color: #222; color: #eee; }
                QPushButton { background-color: #444; color: white; }
            """)
        else:
            self.setStyleSheet("""
                QWidget { background-color: white; color: black; }
                QPushButton { background-color: lightgray; color: black; }
            """)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

app = QApplication(sys.argv)
window = ThemeWindow()
window.show()
sys.exit(app.exec())

# SUMMARY:
# - Toggled styles at runtime
# - Enabled user-facing theming (light/dark)
# - Demonstrates declarative visual control via logic layer