from PySide6.QtWidgets import QLabel, QLineEdit, QFrame, QVBoxLayout, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt

def create_symbol_block(text):
    label = QLabel(text)
    label.setMinimumSize(30, 26)        # 🔧 Tunable block size
    label.setStyleSheet("""
        QLabel {
            background-color: #2a2a2a;
            color: #ffffff;
            font-size: 16px;
            padding: 0px;
            margin: 0px;
            font-family: Menlo, Consolas, Courier, monospace;
        }
    """)
    return label

def create_label_block(default_text="New Folder"):
    frame = QFrame()
    frame.setStyleSheet("""
        QFrame {
            background-color: #1f1f1f;
            border: 1px solid #666;
            border-radius: 5px;
        }
    """)

    input_field = QLineEdit()
    input_field.setText(default_text)
    input_field.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    input_field.setStyleSheet("""
        QLineEdit {
            background-color: transparent;
            color: #f0f0f0;
            border: none;
            font-family: Menlo, Consolas, Courier, monospace;
        }
    """)

    layout = QVBoxLayout(frame)
    layout.setContentsMargins(6, 4, 6, 4)  # 🔧 Adjust frame padding
    layout.setSpacing(0)
    layout.addSpacerItem(QSpacerItem(0, 2, QSizePolicy.Minimum, QSizePolicy.Expanding))
    layout.addWidget(input_field)
    layout.addSpacerItem(QSpacerItem(0, 2, QSizePolicy.Minimum, QSizePolicy.Expanding))

    return frame

def create_blank_line(height=10):
    line = QLabel("")
    line.setFixedHeight(height)
    line.setStyleSheet("background-color: transparent;")
    return line
