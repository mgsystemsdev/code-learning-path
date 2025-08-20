# startup.py
import json
import subprocess
import sys
from PySide6.QtWidgets import QApplication
from gui_qt.main_qt import QtShowcaseWindow

qt_window = None

def launch_target(mode=None):
    global qt_window

    if not mode:
        try:
            with open("system/modes.json", "r", encoding="utf-8") as f:
                config = json.load(f)
                mode = config.get("launch_target")
        except Exception:
            mode = None

    if mode == "qt":
        qt_window = QtShowcaseWindow()
        qt_window.show()
        QApplication.instance().exec()

    elif mode == "tk":
        subprocess.Popen([sys.executable, "gui_tk/main_tk.py"])
    else:
        print("⚠️ Unknown or missing launch mode.")
