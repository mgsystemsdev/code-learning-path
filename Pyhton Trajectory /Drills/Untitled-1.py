#!/usr/bin/env python3
"""
Create a blank 'miguel_toolbox' project tree.

Usage
-----
python bootstrap_miguel_toolbox.py  [target_dir]

• If *target_dir* is omitted, the folder is created in the current directory.
• All modules are empty stubs (only 'pass'), ready for your code.
"""

from pathlib import Path
import sys
import textwrap

# ------------------------------------------------------------------#
# 1. Where to create the project
# ------------------------------------------------------------------#
root = Path(sys.argv[1] if len(sys.argv) > 1 else "miguel_toolbox").resolve()
pkg  = "miguel_logic"                      # importable package name

# ------------------------------------------------------------------#
# 2. File map: relative path → file content (None = empty file)
# ------------------------------------------------------------------#
FILES: dict[str, str | None] = {
    # --- top level -------------------------------------------------
    ".gitignore": textwrap.dedent("""\
        __pycache__/
        *.pyc
        .venv/
        build/
        dist/
        .pytest_cache/
    """),
    "README.md": "# miguel_toolbox\n\nReusable logic toolbox.\n",
    "pyproject.toml": textwrap.dedent(f"""\
        [build-system]
        requires = ["setuptools"]
        build-backend = "setuptools.build_meta"

        [project]
        name = "miguel_toolbox"
        version = "0.0.1"
        description = "Reusable logic library"
        authors = [{{ name="Miguel Gonzalez" }}]
        requires-python = ">=3.10"
    """),
    # --- package skeleton ------------------------------------------
    f"src/{pkg}/__init__.py": textwrap.dedent(f'''\
        """
        {pkg}

        Public API re-exports will live here.
        """
        __all__: list[str] = []
    '''),
    f"src/{pkg}/core_functions.py":      "pass\n",
    f"src/{pkg}/core_classes.py":        "pass\n",
    f"src/{pkg}/tasks.py":               "pass\n",
    f"src/{pkg}/formatters.py":          "pass\n",
    f"src/{pkg}/validators.py":          "pass\n",
    f"src/{pkg}/config.py":              "pass\n",
    f"src/{pkg}/logger.py":              "pass\n",
    f"src/{pkg}/errors.py":              "pass\n",
    f"src/{pkg}/data_manager.py":        "pass\n",
    f"src/{pkg}/utils/__init__.py":      "pass\n",
    f"src/{pkg}/utils/string_utils.py":  "pass\n",
    f"src/{pkg}/services/__init__.py":   "pass\n",
    f"src/{pkg}/services/task_service.py": "pass\n",
    # --- tests ------------------------------------------------------
    "tests/test_core_functions.py": textwrap.dedent("""\
        def test_placeholder() -> None:
            assert True
    """),
    "tests/test_core_classes.py":        textwrap.dedent("""\
        def test_placeholder() -> None:
            assert True
    """),
    "tests/fixtures/.keep":              None,  # keeps folder in git
    # --- examples --------------------------------------------------
    "examples/try_core_features.py": textwrap.dedent(f"""\
        # Example file – start experimenting here.
        # from {pkg}.core_functions import ...
        pass
    """),
}

# ------------------------------------------------------------------#
# 3. Create everything
# ------------------------------------------------------------------#
print(f"📦 Creating project at: {root}")
for rel_path, content in FILES.items():
    file_path = root / rel_path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    if file_path.exists():
        print(f"  ⚠️  Skipped existing {rel_path}")
        continue
    file_path.write_text("" if content is None else content)
    print(f"  ✅ Wrote {rel_path}")

# ------------------------------------------------------------------#
# 4. Final instructions
# ------------------------------------------------------------------#
print(
    "\n🎉 Blank scaffold complete!\n"
    "Next steps:\n"
    f"1. cd {root}\n"
    "2. python -m venv .venv && source .venv/bin/activate  # Windows: .venv\\Scripts\\activate\n"
    "3. pip install -e .\n"
    "4. pytest  # placeholder tests should pass\n"
    "5. Start adding code inside src/miguel_logic/ 🚀"
)
