from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt

class ResizablePipe(QWidget):
    def __init__(self, width=20, height=24):
        super().__init__()
        self.setMinimumSize(width, height)
        self.setStyleSheet("background-color: transparent;")

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

        self._pipe_lines = []
        self._update_pipe_lines()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_pipe_lines()

    def _update_pipe_lines(self):
        for pipe in self._pipe_lines:
            self.layout.removeWidget(pipe)
            pipe.deleteLater()
        self._pipe_lines.clear()

        # Estimate how many pipes fit vertically based on height
        line_count = max(1, self.height() // 16)

        for _ in range(line_count):
            lbl = QLabel("│")
            lbl.setAlignment(Qt.AlignHCenter)
            lbl.setStyleSheet("""
                QLabel {
                    color: #aaa;
                    font-family: Consolas, monospace;
                    font-size: 16px;
                    background-color: transparent;
                }
            """)
            self.layout.addWidget(lbl)
            self._pipe_lines.append(lbl)
