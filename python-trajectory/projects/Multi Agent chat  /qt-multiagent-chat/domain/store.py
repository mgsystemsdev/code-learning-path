import os
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from utils.logging import get_logger

logger = get_logger(__name__)


class AppStore:
    def __init__(self):
        self.current_role = "Engineer"
        self.chat_history = []
        self.settings = {}
        self.history_dir = Path("data/history")
        self.history_dir.mkdir(parents=True, exist_ok=True)
    
    def set_role(self, role: str):
        self.current_role = role
        logger.info(f"Role changed to: {role}")
    
    def add_message(self, message: str, role: str):
        entry = {
            "message": message,
            "role": role,
            "timestamp": datetime.now().isoformat()
        }
        self.chat_history.append(entry)
        logger.debug(f"Added message: {role} - {message[:50]}...")

    def load_latest(self, conv: str, limit: int = 200) -> List[Dict[str, Any]]:
        # Try to load from file first
        history = self._load_conversation_from_file(conv)
        if history:
            return history[-limit:]
        return self.chat_history[-limit:]

    def append(self, conv: str, role: str, text: str):
        self.add_message(text, role)
        # Save to file after each message
        self._save_conversation_to_file(conv)

    def _get_conversation_file(self, conv: str) -> Path:
        """Get the file path for a conversation."""
        safe_name = "".join(c for c in conv if c.isalnum() or c in ('-', '_'))
        return self.history_dir / f"{safe_name}.json"

    def _load_conversation_from_file(self, conv: str) -> Optional[List[Dict[str, Any]]]:
        """Load conversation history from file."""
        file_path = self._get_conversation_file(conv)
        if not file_path.exists():
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('messages', [])
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Failed to load conversation {conv}: {e}")
            return None

    def _save_conversation_to_file(self, conv: str):
        """Save conversation history to file."""
        file_path = self._get_conversation_file(conv)
        
        try:
            data = {
                'conversation_id': conv,
                'created_at': datetime.now().isoformat(),
                'current_role': self.current_role,
                'messages': self.chat_history
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except IOError as e:
            logger.error(f"Failed to save conversation {conv}: {e}")

    def get_conversation_list(self) -> List[str]:
        """Get list of available conversations."""
        conversations = []
        for file_path in self.history_dir.glob("*.json"):
            conversations.append(file_path.stem)
        return sorted(conversations)

    def clear_conversation(self, conv: str):
        """Clear a specific conversation."""
        self.chat_history.clear()
        file_path = self._get_conversation_file(conv)
        if file_path.exists():
            try:
                file_path.unlink()
                logger.info(f"Cleared conversation: {conv}")
            except OSError as e:
                logger.error(f"Failed to clear conversation {conv}: {e}")

store = AppStore()
