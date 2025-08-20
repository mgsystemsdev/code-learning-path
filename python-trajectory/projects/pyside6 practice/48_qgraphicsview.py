# NOTE:
# This demo uses PySide6 (Qt for Python).
# If you prefer PyQt5/PyQt6, you can switch imports accordingly.
# Each script is standalone: run with `python this_file.py`.

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class Demo(QGraphicsView):
    def __init__(self):
        scene = QGraphicsScene()
        super().__init__(scene)
        self.setWindowTitle("QGraphicsView demo")
        scene.addText("Hello Graphics").setPos(20, 20)
        ellipse = scene.addEllipse(0, 0, 120, 80)
        ellipse.setBrush(QBrush(Qt.Dense4Pattern))

if __name__ == "__main__":
    app = QApplication([])
    w = Demo()
    w.resize(480, 320)
    w.show()
    sys.exit(app.exec())
