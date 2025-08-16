import sys, pathlib, os
from PySide6.QtWidgets import QApplication
sys.path.append(str(pathlib.Path(__file__).parent.resolve()))

from config import config
from utils.logging import setup_logging
from ui.chat_window import ChatWindow

def main():
    # Setup logging
    setup_logging(config.LOG_LEVEL, config.LOG_FILE)
    
    # Ensure directories exist
    config.ensure_directories()
    
    app = QApplication(sys.argv)
    w = ChatWindow(conv_id="default")
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
