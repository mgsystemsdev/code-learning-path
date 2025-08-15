import pytest
from domain.store import AppStore


class TestAppStore:
    def test_initial_state(self):
        store = AppStore()
        assert store.current_role == "Engineer"
        assert store.chat_history == []
        assert store.settings == {}

    def test_set_role(self):
        store = AppStore()
        store.set_role("Architect")
        assert store.current_role == "Architect"

    def test_add_message(self):
        store = AppStore()
        store.add_message("Hello", "user")
        
        assert len(store.chat_history) == 1
        assert store.chat_history[0]["message"] == "Hello"
        assert store.chat_history[0]["role"] == "user"

    def test_load_latest_with_limit(self):
        store = AppStore()
        # Add multiple messages
        for i in range(10):
            store.add_message(f"Message {i}", "user")
        
        latest = store.load_latest("test", limit=5)
        assert len(latest) == 5
        assert latest[-1]["message"] == "Message 9"

    def test_append(self):
        store = AppStore()
        store.append("conv1", "user", "Test message")
        
        assert len(store.chat_history) == 1
        assert store.chat_history[0]["message"] == "Test message"
        assert store.chat_history[0]["role"] == "user"
