# main.py
# 🚀 Entry point

import sys
from PySide6.QtWidgets import QApplication
from ui_main import FolderTreeWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FolderTreeWindow()
    window.show()
    sys.exit(app.exec())
