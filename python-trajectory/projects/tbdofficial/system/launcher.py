# Author:      Miguel Gonzalez Almonte  # Created:     2025-05-24  # File:        launcher.py  # Description: Handles CLI or prelaunch flags  
# launcher.py
# Handles CLI arguments to skip login and set launch mode

import argparse

def get_launch_mode():
    parser = argparse.ArgumentParser(description="Training Python Board Launcher")
    parser.add_argument("--qt", action="store_true", help="Launch PySide6 GUI")
    parser.add_argument("--tk", action="store_true", help="Launch Tkinter GUI")
    args = parser.parse_args()

    if args.qt:
        return "qt"
    elif args.tk:
        return "tk"
    else:
        return None  # fall back to login
