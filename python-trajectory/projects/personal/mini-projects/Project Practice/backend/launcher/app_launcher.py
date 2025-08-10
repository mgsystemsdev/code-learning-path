

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

from login import LoginScreen

def launch_app():
    app = QApplication(sys.argv)               
    window = LoginScreen()               
    window.show()                               

    sys.exit(app.exec())                        
