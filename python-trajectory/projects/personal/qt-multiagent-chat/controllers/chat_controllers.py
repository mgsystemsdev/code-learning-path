# controllers/chat_controllers.py
from __future__ import annotations

from PySide6.QtCore import QObject, Signal, QThread, QTimer
from agents.role_manager import REGISTRY
from services.llm_qwen import QwenProvider
from config import config
from utils.logging import get_logger

logger = get_logger(__name__)


class _Worker(QObject):
    finished = Signal(str)
    failed = Signal(str)

    def __init__(self, role: str, user_text: str, parent: QObject | None = None):
        super().__init__(parent)
        self.role = role
        self.user_text = user_text

    def run(self):
        try:
            # Resolve role instructions safely with fallbacks
            role_cfg = REGISTRY.get(self.role) or REGISTRY.get("General") or None
            system = getattr(role_cfg, "instructions", "") if role_cfg else ""

            provider = QwenProvider()  # Local Ollama-backed Qwen
            out = provider.complete(system=system, user=self.user_text)
            self.finished.emit(out or "")
        except Exception as e:
            self.failed.emit(f"{type(e).__name__}: {e}")


class ChatController(QObject):
    """
    Async controller for UI:
    - call ask(text) to start a background request
    - listen to reply(str) and error(str) signals
    """
    reply = Signal(str)
    error = Signal(str)
    health_changed = Signal(bool)

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self.role = config.DEFAULT_ROLE
        self._thread: QThread | None = None
        self._worker: _Worker | None = None
        self._provider = QwenProvider(
            host=config.OLLAMA_HOST,
            model=config.OLLAMA_MODEL,
            timeout=config.OLLAMA_TIMEOUT
        )
        
        # Health check timer
        self._health_timer = QTimer()
        self._health_timer.timeout.connect(self.check_health)
        self._health_timer.start(30000)  # Check every 30 seconds
        self._last_health_status = False

    def set_role(self, role: str):
        self.role = role

    def ask(self, user_text: str):
        # Prevent overlapping jobs
        if self._thread is not None and self._thread.isRunning():
            self.error.emit("Busy: previous request still running.")
            return

        self._thread = QThread(self)
        self._worker = _Worker(self.role, user_text)
        self._worker.moveToThread(self._thread)

        # Start → run
        self._thread.started.connect(self._worker.run)

        # Results → UI
        self._worker.finished.connect(self._on_finished)
        self._worker.failed.connect(self._on_failed)

        # Cleanup
        self._worker.finished.connect(self._thread.quit)
        self._worker.failed.connect(self._thread.quit)
        self._thread.finished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._clear_refs)
        self._thread.finished.connect(self._thread.deleteLater)

        self._thread.start()

    # Signal handlers
    def _on_finished(self, text: str):
        self.reply.emit(text)

    def _on_failed(self, msg: str):
        self.error.emit(f"Qwen error: {msg}")

    def _clear_refs(self):
        self._worker = None
        self._thread = None
        
    def check_health(self):
        """Check Ollama health and emit signal if status changed."""
        try:
            is_healthy = self._provider.health()
            if is_healthy != self._last_health_status:
                self._last_health_status = is_healthy
                self.health_changed.emit(is_healthy)
                logger.info(f"Health check: {'healthy' if is_healthy else 'unhealthy'}")
        except Exception as e:
            if self._last_health_status != False:
                self._last_health_status = False
                self.health_changed.emit(False)
                logger.error(f"Health check failed: {e}")

    def set_provider_config(self, host: str = None, model: str = None, timeout: int = None):
        """Update provider configuration."""
        if host or model or timeout:
            self._provider = QwenProvider(
                host=host or config.OLLAMA_HOST,
                model=model or config.OLLAMA_MODEL,
                timeout=timeout or config.OLLAMA_TIMEOUT
            )
            logger.info(f"Updated provider config: {host}, {model}, {timeout}")
