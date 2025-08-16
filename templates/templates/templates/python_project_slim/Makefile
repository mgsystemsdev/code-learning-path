.PHONY: init lint fmt test clean

    init:
	@if command -v uv >/dev/null; then \
		uv pip install -e ".[dev]"; \
	else \
		pip install -e ".[dev]"; \
	fi

    lint:
	python -m ruff check .

    fmt:
	python -m black .

    test:
	pytest

    clean:
	rm -rf .pytest_cache .ruff_cache **/__pycache__
