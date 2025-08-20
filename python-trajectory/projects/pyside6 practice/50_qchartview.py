# NOTE:
# This demo uses PySide6 (Qt for Python).
# If you prefer PyQt5/PyQt6, you can switch imports accordingly.
# Each script is standalone: run with `python this_file.py`.

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

# QChartView requires the Qt Charts module. If missing, we fall back to a label.
try:
    from PySide6.QtCharts import QChartView, QChart, QLineSeries
except Exception:
    QChartView = QChart = QLineSeries = None

class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QChartView demo (Qt Charts)")
        lay = QVBoxLayout(self)
        if QChartView is None:
            lay.addWidget(QLabel("Qt Charts module not available."))
        else:
            series = QLineSeries()
            for x in range(10):
                series.append(x, x*x)
            chart = QChart()
            chart.addSeries(series)
            chart.createDefaultAxes()
            lay.addWidget(QChartView(chart))

if __name__ == "__main__":
    app = QApplication([])
    w = Demo()
    w.resize(520, 360)
    w.show()
    sys.exit(app.exec())
