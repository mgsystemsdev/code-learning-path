# app/main.py
"""
Application entry point for Smart Learning Tracker.

- Sets HiDPI environment variables BEFORE creating QApplication
- Applies HighDPI rounding policy
- Bootstraps and runs the MainWindow
"""

from __future__ import annotations

import os
import sys

# --- HiDPI fixes must be set BEFORE creating QApplication ---
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt

# Remove deprecated HiDPI attribute: set rounding policy globally
QGuiApplication.setHighDpiScaleFactorRoundingPolicy(
    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
)

# Import after Qt pieces are configured
from app.main_window import MainWindow  # noqa: E402


def main() -> int:
    """Create the Qt application, show MainWindow, and start the event loop."""
    app = QApplication(sys.argv)
    app.setApplicationName("Smart Learning Tracker")
    app.setApplicationVersion("2.0")

    try:
        window = MainWindow()
        window.show()
        return app.exec()
    except Exception as e:
        # Last-chance error surface so startup failures aren’t silent
        QMessageBox.critical(None, "Startup Error", f"Failed to start application:\n{e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
