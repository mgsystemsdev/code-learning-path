# Author:      Miguel Gonzalez Almonte  # Created:     2025-05-24  # File:        constants.py  # Description: Shared enums and UI strings  
# constants.py
# Shared enums and UI strings

from enum import Enum

class LaunchMode(str, Enum):
    QT = "qt"
    TK = "tk"

# UI strings
APP_TITLE = "Training Python Board"
WELCOME_TEXT = "Welcome to Training Python Board"
LOGIN_LABEL = "Login:"
USERNAME_PLACEHOLDER = "Username"
PASSWORD_PLACEHOLDER = "Password"
MODE_SELECT_TEXT = "Choose GUI Mode"
ADVANCED_LABEL = "🔧 Advanced GUI Projects"
COMING_SOON_TEXT = " is coming soon!"
