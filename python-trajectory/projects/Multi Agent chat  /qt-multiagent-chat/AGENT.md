# AGENT.md - Qt Multi-Agent Chat

## Commands
- **Run**: `python main.py` (starts PySide6/Qt GUI)
- **Test**: `pytest tests/` (unit tests with pytest-qt)
- **Install**: `pip install -r requirements.txt` or `pip install -e .[dev]`
- **Dependencies**: PySide6, requests, PyYAML (Ollama integration)

## Architecture
- **MVC Pattern**: UI (PySide6) → Controllers → Services → Domain
- **Key Components**:
  - `ui/chat_window.py` - Main Qt GUI with chat interface, role switcher, sidebar
  - `controllers/chat_controllers.py` - Async chat controller using QThread
  - `services/llm_qwen.py` - Ollama/Qwen LLM provider (localhost:11434)
  - `domain/store.py` - In-memory app state (messages, roles, settings)
  - `agents/` - Role-based agent system with registry
- **Data Flow**: User input → Controller → QThread Worker → Qwen API → UI update
- **Storage**: File-based history in `data/history/` directory

## Code Style
- **Imports**: Absolute imports from project root, PySide6 grouped first
- **Classes**: PascalCase, inherit from Qt classes appropriately
- **Methods**: snake_case, private methods prefixed with `_`
- **Signals**: Qt Signal/Slot pattern for async communication
- **Error Handling**: Try/catch with fallbacks, emit error signals to UI
- **Threading**: Use QThread for async operations, proper cleanup with deleteLater()
- **Layout**: Qt layouts (QVBoxLayout, QHBoxLayout), proper margins/spacing
