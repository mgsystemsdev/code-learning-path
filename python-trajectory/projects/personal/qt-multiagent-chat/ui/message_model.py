from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex
ROLE_USER = "user"
ROLE_AGENT = "agent"

class MsgModel(QAbstractListModel):
    def __init__(self, messages=None):
        super().__init__()
        self.messages = messages or []

    def rowCount(self, parent=QModelIndex()):
        return len(self.messages)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.messages[index.row()]
        return None

    def add_message(self, role, text):
        self.beginInsertRows(QModelIndex(), len(self.messages), len(self.messages))
        self.messages.append({"role": role, "text": text})
        self.endInsertRows()
