import sys
import json
from PySide6.QtWidgets import QApplication
from system.login_dialog import LoginDialog
from gui_qt.main_qt import QtShowcaseWindow
from system import launcher
from system.startup import launch_target

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mode = launcher.get_launch_mode()

    if mode:
        with open("system/modes.json", "w", encoding="utf-8") as f:
            json.dump({"launch_target": mode, "api_mode": "none"}, f, indent=2)
        win = QtShowcaseWindow()
        win.show()
        sys.exit(app.exec())

    dialog = LoginDialog()
    if dialog.exec():
        launch_target()
