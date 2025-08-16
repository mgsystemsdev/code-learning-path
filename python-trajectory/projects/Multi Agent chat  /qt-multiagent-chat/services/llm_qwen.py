# services/llm_qwen.py
from __future__ import annotations

import requests
from typing import List, Dict, Any
from utils.logging import get_logger

logger = get_logger(__name__)


class QwenProvider:
    """
    Minimal local Qwen provider via Ollama.
    Requires Ollama running at http://localhost:11434 and a pulled model (default: qwen2.5:7b-instruct).
    """

    def __init__(
        self,
        model: str = "qwen2.5:7b-instruct",
        host: str = "http://localhost:11434",
        timeout: int = 120,
    ):
        self.model = model
        self.host = host.rstrip("/")
        self.timeout = timeout

    @property
    def name(self) -> str:
        return f"ollama:{self.model}"

    def health(self) -> bool:
        try:
            r = requests.get(f"{self.host}/api/tags", timeout=1.5)
            is_healthy = r.ok
            logger.debug(f"Health check: {is_healthy}")
            return is_healthy
        except Exception as e:
            logger.debug(f"Health check failed: {e}")
            return False

    def _chat(self, messages: List[Dict[str, str]], **opts) -> str:
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": float(opts.get("temperature", 0.2)),
                "top_p": float(opts.get("top_p", 0.9)),
                "num_ctx": int(opts.get("num_ctx", 4096)),
            },
        }
        logger.debug(f"Sending request to {self.host}/api/chat with model {self.model}")
        r = requests.post(f"{self.host}/api/chat", json=payload, timeout=self.timeout)
        r.raise_for_status()
        data = r.json()
        response = (data.get("message", {}) or {}).get("content", "").strip()
        logger.debug(f"Received response length: {len(response)}")
        return response

    def complete(self, system: str, user: str, **opts) -> str:
        """
        High-level call: pass a system prompt and a user message.
        Returns the model text.
        """
        if not self.health():
            raise RuntimeError("Ollama is not reachable at http://localhost:11434")
        messages = [
            {"role": "system", "content": system or "You are a concise, helpful assistant."},
            {"role": "user", "content": user},
        ]
        return self._chat(messages, **opts)
