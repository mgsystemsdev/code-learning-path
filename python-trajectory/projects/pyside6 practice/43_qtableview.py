# NOTE:
# This demo uses PySide6 (Qt for Python).
# If you prefer PyQt5/PyQt6, you can switch imports accordingly.
# Each script is standalone: run with `python this_file.py`.

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class SimpleTableModel(QAbstractTableModel):
    def rowCount(self, parent=QModelIndex()): return 3
    def columnCount(self, parent=QModelIndex()): return 3
    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole: return f"R{index.row()}C{index.column()}"
        return None

class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTableView demo (with model)")
        lay = QVBoxLayout(self)
        view = QTableView()
        view.setModel(SimpleTableModel())
        lay.addWidget(view)

if __name__ == "__main__":
    app = QApplication([])
    w = Demo()
    w.resize(360, 220)
    w.show()
    sys.exit(app.exec())
