#StartHere - The application starts here with essential imports
import sys  # Import the system module to handle arguments and exit control
import json  # Import the JSON module to read and write configuration files
from PySide6.QtWidgets import QApplication  # Import the core Qt app framework
from system.login_dialog import LoginDialog  # Import the custom login dialog class
from gui_qt.main_qt import QtShowcaseWindow  # Import the main window for the app
from system import launcher  # Import the launcher module to get launch mode
from system.startup import launch_target  # Import the startup routine after login
from system.logger import Logger  # Import the Logger class for writing log entries

#SetupTheScene - Define the main logic flow for how the app boots
def main():
    app = QApplication(sys.argv)  # Create a new Qt application with system arguments

    #WhatThisDoes - Attempt to retrieve the launch mode (e.g., from CLI args or config)
    mode = launcher.get_launch_mode()  # Get the current mode from the launcher system

    #ThePlotTwist - If a valid mode was found, skip login and show main window directly
    if mode:
        Logger.write(f"[MODE] Launching in mode: {mode}")  # Log the chosen launch mode

        # Write the selected mode into the modes.json file for use by the app
        with open("system/modes.json", "w", encoding="utf-8") as f:
            json.dump({"launch_target": mode, "api_mode": "none"}, f, indent=2)  # Save mode config to JSON

        win = QtShowcaseWindow()  # Create the main GUI window
        win.show()  # Display the window to the user

        #TheExit - Begin the Qt event loop and exit cleanly when done
        sys.exit(app.exec())  # Start the main application loop

    #ActionTakesPlace - If no mode found, show the login dialog to the user
    dialog = LoginDialog()  # Create an instance of the login dialog
    if dialog.exec():  # Run the dialog and check if the user clicks "OK"
        Logger.write("[LOGIN] Login dialog accepted — launching target")  # Log successful login
        launch_target()  # Call the launch function to continue the app
    else:
        Logger.write("[LOGIN] Login cancelled by user")  # Log if the user cancels login

#BuildTheBoard - Ensure this script runs only when executed directly
if __name__ == "__main__":  # Check if this script is the main one being run
    main()  # Call the main function to begin app execution