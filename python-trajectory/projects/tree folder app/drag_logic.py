from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QPoint, Qt

class DraggableBlock(QWidget):
    def __init__(self, inner_widget, width=220, height=30):
        super().__init__()
        self.setFixedSize(width, height)
        self.inner_widget = inner_widget
        self.inner_widget.setParent(self)
        self.inner_widget.move(0, 0)
        self.inner_widget.resize(width, height)
        self.start_pos = None
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_pos = event.globalPosition().toPoint() - self.pos()
            self.raise_()

    def mouseMoveEvent(self, event):
        if self.start_pos and event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.start_pos)

    def mouseReleaseEvent(self, event):
        self.start_pos = None

    def eventFilter(self, obj, event):
        # Forward all mouse events from child widgets to this block
        if event.type() in (event.MouseButtonPress, event.MouseMove, event.MouseButtonRelease):
            self.mousePressEvent(event)
            return True
        return super().eventFilter(obj, event)
