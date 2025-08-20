# NOTE:
# This demo uses PySide6 (Qt for Python).
# If you prefer PyQt5/PyQt6, you can switch imports accordingly.
# Each script is standalone: run with `python this_file.py`.

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class Page1(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Welcome")
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel("This is a QWizardPage."))

class DemoWizard(QWizard):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QWizard / QWizardPage demo")
        self.addPage(Page1())

if __name__ == "__main__":
    app = QApplication([])
    wiz = DemoWizard()
    wiz.show()
    sys.exit(app.exec())
