# demo_qdockwidget.py
# Demo: QDockWidget with dockable label

from PySide6.QtWidgets import QMainWindow, QLabel, QDockWidget

def launch_demo():
    window = QMainWindow()
    window.setWindowTitle("QDockWidget Demo")
    window.resize(500, 300)

    # Central widget
    label = QLabel("Main Window Area")
    label.setStyleSheet("padding: 20px;")
    window.setCentralWidget(label)

    # Dock widget
    dock = QDockWidget("Dockable Panel", window)
    dock.setWidget(QLabel("This is a dockable widget"))
    window.addDockWidget(Qt.LeftDockWidgetArea, dock)

    window.show()
    return window
