# Author:      Miguel Gonzalez Almonte
# Created:     2025-05-20
# File:        start.py
# Description: Launch script — initializes environment and starts the login screen
# start.py
# --------
# Application bootstrap — sets up the environment and launches the initial login screen
# This is the one and only entry point for the system
# TODO: Extend with config loader, logging, and CLI options
# ----------------------------------

# The import system for internal modules
import sys
import os

# Ensure the project root is in Python's module search path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

#  Importing the delegated Qt launch logic
from backend.launcher.app_launcher import launch_app


# Excepcution Flow
def main():
    launch_app()


# Entrypoint 
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[Fatal] Startup error: {e}")
        sys.exit(1)


