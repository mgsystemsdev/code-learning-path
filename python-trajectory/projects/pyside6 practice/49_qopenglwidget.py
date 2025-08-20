# NOTE:
# This demo uses PySide6 (Qt for Python).
# If you prefer PyQt5/PyQt6, you can switch imports accordingly.
# Each script is standalone: run with `python this_file.py`.

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

try:
    from PySide6.QtOpenGLWidgets import QOpenGLWidget
except Exception as e:
    QOpenGLWidget = None

class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QOpenGLWidget demo")
        lay = QVBoxLayout(self)
        if QOpenGLWidget is None:
            lay.addWidget(QLabel("QtOpenGLWidgets not available in this environment."))
        else:
            lay.addWidget(QOpenGLWidget())

if __name__ == "__main__":
    app = QApplication([])
    w = Demo()
    w.resize(480, 320)
    w.show()
    sys.exit(app.exec())
