from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton,
    QVBoxLayout, QHBoxLayout, QScrollArea
)
from PySide6.QtCore import Qt, QPoint
from block_factory import (
    create_symbol_block,
    create_label_block,
    create_blank_line
)
from drag_logic import DraggableBlock


class FolderTreeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Folder Tree Builder")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # === Left Panel: Buttons ===
        button_panel = QVBoxLayout()
        main_layout.addLayout(button_panel, 1)

        # === Right Panel: Scrollable Canvas ===
        self.canvas = QWidget()
        self.canvas.setMinimumSize(1200, 1000)
        self.canvas.setStyleSheet("background-color: #252526;")
        self.canvas.setAttribute(Qt.WA_StaticContents)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.canvas)
        main_layout.addWidget(scroll, 4)

        self.last_label_block = None
        self.next_y = 10

        def make_btn(text, func):
            btn = QPushButton(text)
            btn.clicked.connect(func)
            button_panel.addWidget(btn)

        make_btn("├── Mid Branch", self.add_mid_branch)
        make_btn("└── End Branch", self.add_end_branch)
        make_btn("│ Pipe", self.add_pipe)
        make_btn("␣␣␣␣ Blank Line", self.add_blank_line)
        make_btn("Add Label", self.add_label)
        make_btn("/ Mark as Folder", self.mark_as_folder)

        # === StyleSheet (Dark Mode) ===
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #dcdcdc;
            }
            QPushButton {
                background-color: #2d2d30;
                color: #ffffff;
                border: 1px solid #444;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #3e3e42;
            }
            QLabel {
                background-color: #2a2a2a;
                color: #e0e0e0;
                border: 1px solid #555;
                padding: 3px;
            }
        """)

    def add_block_to_canvas(self, block, width=220, height=30):
        draggable = DraggableBlock(block, width=width, height=height)
        draggable.setParent(self.canvas)
        draggable.move(20, self.next_y)
        draggable.show()
        self.next_y += height + 8

    def add_mid_branch(self):
        symbol = create_symbol_block("├──")
        self.add_block_to_canvas(symbol, width=100, height=26)

    def add_end_branch(self):
        symbol = create_symbol_block("└──")
        self.add_block_to_canvas(symbol, width=100, height=26)

    def add_pipe(self):
        symbol = create_symbol_block("│")
        self.add_block_to_canvas(symbol, width=20, height=24)

    def add_blank_line(self):
        blank = create_blank_line(height=10)
        self.add_block_to_canvas(blank, width=100, height=10)

    def add_label(self):
        label_block = create_label_block("New Folder")
        self.add_block_to_canvas(label_block, width=220, height=26)
        self.last_label_block = label_block

    def mark_as_folder(self):
        if self.last_label_block:
            label = self.last_label_block.findChild(QWidget).findChild(QWidget)
            if label and hasattr(label, "text"):
                if not label.text().endswith("/"):
                    label.setText(label.text() + "/")


if __name__ == "__main__":
    app = QApplication([])
    window = FolderTreeWindow()
    window.show()
    app.exec()
