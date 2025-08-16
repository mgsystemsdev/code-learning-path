# --- path safety net ---
import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
# ------------------------

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListView, QLineEdit, QPushButton,
    QLabel, QTreeWidget, QTreeWidgetItem, QSplitter, QTabWidget, QTextEdit, QMenu, QSizePolicy
)
from PySide6.QtCore import Qt, QEvent, Signal, QTimer, QTime
from PySide6.QtGui import QAction

from .message_model import MsgModel, ROLE_USER, ROLE_AGENT
from .message_delegate import MsgDelegate
from domain.store import store
from config import config
from utils.logging import get_logger

# NEW: use the async Qwen-backed controller
from controllers.chat_controllers import ChatController

logger = get_logger(__name__)


class Header(QWidget):
    roleChanged = Signal(str)
    def __init__(self, roles, initial="Engineer"):
        super().__init__()
        row = QHBoxLayout(self); row.setContentsMargins(12,10,12,10); row.setSpacing(8)
        self.btnSidebar = QPushButton("☰"); self.btnSidebar.setObjectName("iconbtn")
        self.btnPreview = QPushButton("◧"); self.btnPreview.setObjectName("iconbtn")
        title = QLabel("Super Agent"); title.setObjectName("title")
        
        # Health status indicator
        self.health_status = QLabel("● Offline"); self.health_status.setObjectName("health-status")
        self.health_status.setStyleSheet("QLabel { color: red; }")
        
        spacer = QWidget(); spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.roleBtn = QPushButton(f"{initial} ▼"); self.roleBtn.setObjectName("rolebtn")
        menu = QMenu(self)
        for r in roles:
            act = QAction(r, self); act.triggered.connect(lambda _, rr=r: self._set_role(rr))
            menu.addAction(act)
        self.roleBtn.setMenu(menu)

        self.btnSettings = QPushButton("⚙"); self.btnSettings.setObjectName("iconbtn")
        row.addWidget(self.btnSidebar); row.addWidget(self.btnPreview)
        row.addWidget(title); row.addWidget(self.health_status); row.addWidget(spacer)
        row.addWidget(self.roleBtn); row.addWidget(self.btnSettings)

    def _set_role(self, role): 
        self.roleBtn.setText(f"{role} ▼"); 
        self.roleChanged.emit(role)


class ChatWindow(QMainWindow):
    def __init__(self, conv_id="default"):
        super().__init__()
        self.setWindowTitle("Super Agent – Chat")
        self.resize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        self.conv_id = conv_id
        logger.info(f"Starting chat window for conversation: {conv_id}")

        # Controller (Qwen-only path); emits reply/error
        self.controller = ChatController()
        self.controller.reply.connect(self._on_reply)
        self.controller.error.connect(self._on_error)
        self.controller.health_changed.connect(self._on_health_changed)

        roles = ["General", "Architect", "Engineer", "Tester", "Doc Writer", "Data Analyst"]
        self.header = Header(roles, "Engineer")
        self.header.roleChanged.connect(self.on_role_change)

        # Sidebar → Tree with sections
        self.sidebar = QTreeWidget(); self.sidebar.setHeaderHidden(True)
        dev = QTreeWidgetItem(["Developers"]); [QTreeWidgetItem(dev, [r]) for r in ("Architect","Engineer","Tester")]
        docs = QTreeWidgetItem(["Writers"]); [QTreeWidgetItem(docs, [r]) for r in ("Doc Writer",)]
        ops = QTreeWidgetItem(["Analysts"]); [QTreeWidgetItem(ops, [r]) for r in ("Data Analyst","General")]
        self.sidebar.addTopLevelItems([dev, docs, ops]); self.sidebar.expandAll()
        self.sidebar.itemClicked.connect(lambda it,_: self.on_role_change(it.text(0)) if it.childCount()==0 else None)
        self.sidebar.setMaximumWidth(260)

        # Center chat (ListView + delegate)
        self.model = MsgModel([])
        # Load history; be tolerant to key name ("text" vs "message")
        for m in store.load_latest(self.conv_id):
            msg_text = m.get("text") or m.get("message") or ""
            self.model.add_message(m.get("role","agent"), msg_text)

        self.list = QListView(); self.list.setModel(self.model); self.list.setItemDelegate(MsgDelegate())
        self.list.setVerticalScrollMode(QListView.ScrollPerPixel); self.list.setSelectionMode(QListView.NoSelection)

        self.input = QLineEdit(); self.input.setPlaceholderText("Type a message…")
        self.send = QPushButton("Send"); self.send.setObjectName("sendbtn"); self.send.clicked.connect(self.on_send)
        # ENTER sends the message
        self.input.returnPressed.connect(self.on_send)

        inprow = QHBoxLayout(); inprow.addWidget(self.input,1); inprow.addWidget(self.send)
        center = QWidget(); col = QVBoxLayout(center); col.setContentsMargins(0,0,0,0); col.setSpacing(8)
        col.addWidget(self.list); col.addLayout(inprow)

        # Preview tabs
        self.preview = QTabWidget()
        for name, txt in [("Diff","Diff preview…"),("Tests/Lint","Unit test output…"),("Docs","Markdown…"),("HTML","HTML/Charts…"),("JSON","JSON payloads…")]:
            w = QTextEdit(txt); w.setReadOnly(True); self.preview.addTab(w, name)
        self.preview.setMinimumWidth(420)

        splitter = QSplitter(Qt.Horizontal); splitter.addWidget(self.sidebar); splitter.addWidget(center); splitter.addWidget(self.preview)
        splitter.setSizes([260, 780, 420])

        root = QWidget(); rootv = QVBoxLayout(root); rootv.setContentsMargins(10,10,10,10); rootv.setSpacing(10)
        rootv.addWidget(self.header); rootv.addWidget(splitter)
        self.setCentralWidget(root)

        self.header.btnSidebar.clicked.connect(lambda: self.sidebar.setVisible(not self.sidebar.isVisible()))
        self.header.btnPreview.clicked.connect(lambda: self.preview.setVisible(not self.preview.isVisible()))
        self._load_styles()

        # Initial health check
        self.controller.check_health()

        if not getattr(store, "chat_history", []):
            self._add_agent("UI upgraded: dark theme, card messages, role tree, preview polish.")

    # Styles
    def _load_styles(self):
        # Try common paths (project differs across setups)
        for candidate in ("ui/styles.qss", "styles/styles.qss"):
            try:
                with open(candidate, "r", encoding="utf-8") as f:
                    self.setStyleSheet(f.read()); 
                    return
            except Exception:
                continue

    # Model/store helpers
    def _add_user(self, text):
        self.model.add_message(ROLE_USER, text); store.append(self.conv_id, ROLE_USER, text)
        QTimer.singleShot(0, lambda: self.list.scrollToBottom())
    def _add_agent(self, text):
        self.model.add_message(ROLE_AGENT, text); store.append(self.conv_id, ROLE_AGENT, text)
        QTimer.singleShot(0, lambda: self.list.scrollToBottom())

    # Events
    def on_send(self):
        t = self.input.text().strip()
        if not t: 
            return
        self.input.clear()
        self._add_user(t)

        # Lock UI while thinking (optional, simple)
        self.send.setEnabled(False)

        # Ensure controller has the latest role
        try:
            current_role = getattr(store, "current_role", "Engineer")
        except Exception:
            current_role = "Engineer"
        self.controller.set_role(current_role)

        # Ask Qwen asynchronously (reply/error signals will re-enable button)
        self.controller.ask(t)

    def on_role_change(self, role):
        if role in ("Developers","Writers","Analysts"):
            return
        store.set_role(role)
        self.controller.set_role(role)
        self._add_agent(f"Switched role → {role}.")

    # Signal handlers from ChatController
    def _on_reply(self, text: str):
        self._add_agent(text)
        self.send.setEnabled(True)

    def _on_error(self, msg: str):
        self._add_agent(f"[Qwen error] {msg}")
        self.send.setEnabled(True)
        
    def _on_health_changed(self, is_healthy: bool):
        """Update health status indicator."""
        if is_healthy:
            self.header.health_status.setText("● Online")
            self.header.health_status.setStyleSheet("QLabel { color: green; }")
            logger.info("Ollama connection healthy")
        else:
            self.header.health_status.setText("● Offline")  
            self.header.health_status.setStyleSheet("QLabel { color: red; }")
            logger.warning("Ollama connection unhealthy")
