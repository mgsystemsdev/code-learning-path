import sys
from PySide6.QtWidgets import QApplication
from system.launcher import get_launch_mode
from gui.login_dialog import LoginDialog
from windows.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    mode = get_launch_mode()

    if mode:
        window = MainWindow(mode)
        window.show()
    else:
        dialog = LoginDialog()
        if dialog.exec():
            window = MainWindow("from_login")
            window.show()
        else:
            sys.exit()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
