# Agent Configuration for Code Learning Path

## Commands
- **Test**: `python3 -m pytest tests/` (from project root), `pytest -q` (standard options)
- **Lint**: `ruff check .` then `black --check .` (line length: 100)
- **Format**: `black .` and `ruff --fix .`
- **Run main app**: `cd code-log-tracker && python3 main.py`
- **Install deps**: `uv pip install -e ".[dev]"` (fallback: `pip install -r requirements.txt`)

## Architecture
- **Multi-trajectory learning repository**: Python (active), HTML/CSS, JS, React, Django, Database, DevOps (planned)
- **Main application**: `code-log-tracker/` - PySide6 desktop learning tracker with SQLite backend
- **Project templates**: Python projects use `pyproject.toml` with Black/Ruff/pytest
- **Database**: SQLite at `code-log-tracker/learning_tracker.db`
- **Entry points**: `main.py` files, tests in `tests/` dirs

## Code Style
- **Python 3.11+** with comprehensive type hints (`from __future__ import annotations`)
- **Imports**: stdlib first, third-party, then local with `# noqa: E402` for late imports
- **Names**: snake_case functions/vars, PascalCase classes, UPPER_CASE constants, _private methods
- **Docstrings**: Module-level with bullet points, concise function docs
- **Error handling**: Specific exceptions, graceful degradation, context logging
- **Line length**: 100 chars (Black + Ruff configured)
- **No comments** in code unless complex logic requires explanation
