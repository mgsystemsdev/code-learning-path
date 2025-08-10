# code-learning-path

**Purpose:** A multi-trajectory learning repository tracking courses, projects, and templates across Python, Web, and DevOps.

## Overview
- A **trajectory** is a focused learning lane (e.g., *python-trajectory*, *react-trajectory*). Each trajectory keeps its own courses, personal projects, and templates.
- This repo standardizes metadata, progress tracking, and CI checks so everything stays consistent and testable.

## Structure
```text
code-learning-path/
├─ python-trajectory/
├─ html-css-trajectory/
├─ javascript-trajectory/
├─ react-trajectory/
├─ django-trajectory/
├─ database-trajectory/
└─ devops-trajectory/
```
- Each trajectory contains:
  - `COURSES.md` / `PROJECTS.md` indices.
  - `courses/` with course folders that include `meta.yaml`, `progress.md`, `notes.md`, and (optionally) `syllabus.md`, `resources.md`, and a `certificate.pdf` placeholder.
  - `projects/` for personal work with a repeatable Python template where relevant.
  - `templates/` with ready-to-copy blueprints.

## How to Use
1. **Clone** the repo:
   ```bash
   git clone https://github.com/mgsystemsdev/code-learning-path.git
   cd code-learning-path
   ```
2. **Add a new course**: copy the folder under `python-trajectory/templates/course/` into `python-trajectory/courses/`, rename, then edit `meta.yaml` and `progress.md`.
3. **Add a new project**: use `python-trajectory/projects/templates/python_project_slim/` as a base. Copy it into `python-trajectory/projects/personal/mini-projects/` or `.../capstones/`, rename, and update `pyproject.toml` `[project].name`.
4. **Keep progress up to date**: append rows to `progress.md` tables and store notes in `notes.md`.
5. **Certificates**: keep a valid 1-page `certificate.pdf` placeholder until you have the real certificate.

## Quickstart (Python templates)
- **Package manager:** `uv` (fallback: `pip`)
- **Code style:** Black + Ruff (line length 100)
- **Tests:** pytest
- **Primary language:** Python 3.11

### CI Explanation
- GitHub Actions workflow at `.github/workflows/ci.yml`:
  - Discovers all `pyproject.toml` files.
  - Installs dev dependencies using `uv` if available (otherwise `pip`).
  - Runs Ruff, Black (check), and pytest for each detected project.

## Contributing
- Keep YAML/TOML syntactically valid.
- Follow the templates when adding new content.
- Use meaningful commit messages.

## Licensing
MIT License © 2025 Miguel A. Gonzalez. See [LICENSE](LICENSE).
# code-learning-path
