


from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit 



class UsernameField(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)


        layout = QVBoxLayout()

        self.input = QLineEdit()
        self.input.setPlaceholderText("          Username")

        
        layout.addWidget(self.input)



        self.setLayout(layout)
