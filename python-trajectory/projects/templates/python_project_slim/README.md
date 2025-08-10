# python_project_slim

A slim Python project template.

## How to copy and initialize
- Copy this folder and rename it to your project name.
- Update `pyproject.toml` `[project].name` to match the new folder name.
- Create a virtual environment (recommended via `uv`), install dev tools, and run tests.

### Quickstart
```bash
# using uv (preferred)
uv venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
uv pip install -e ".[dev]"

# fallback: pip
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Run tests
```bash
pytest
```

### Project layout
```text
.
├─ pyproject.toml
├─ src/
│  ├─ __init__.py
│  └─ <package_name>/__init__.py
└─ tests/
   ├─ __init__.py
   └─ test_basic.py
```
