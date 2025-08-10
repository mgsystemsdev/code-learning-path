

# Author:      Miguel Gonzalez Almonte
# Created:     2025-05-22
# File:        app_launcher.py
# Description: Boot manager — creates the QApplication and launches the login screen

# app_launcher.py
# ----------------
# This file owns the system startup logic for all UI flows
# It allows for future switching between login, dashboard, etc.
# TODO: Add config check, auth route, and headless bypass
# ----------------------------------

import sys
from PySide6.QtWidgets import QApplication

from ui.dialogs.login_dialog import LoginScreen# ✅ spelling fix

def launch_app():
    app = QApplication(sys.argv)                # 🔁 Create the Qt app context

    window = LoginScreen()               # 🔁 Launch the viewer
    window.show()                               # 🔁 Show window on screen

    sys.exit(app.exec())                        # 🔁 Start Qt event loop
