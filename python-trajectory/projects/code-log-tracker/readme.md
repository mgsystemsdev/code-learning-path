# Learning Tracker (Desktop + Web Demo)

https://code-learning-path-he6mnt3usprtot3tltlab4.streamlit.app/

**What this is:** A production-style learning log with computed **Points** and **Project Progress %**.  
**Desktop app:** PySide6 (offline, fast data entry).  
**Web demo:** Streamlit viewer so recruiters can browse your progress **without installing the desktop UI**.

## Highlights
- **Type rules:** Exercise vs Project enforced with validation and disabled fields.
- **Auto metadata:** Difficulty / Topic inferred with override, **Points** computed, **Progress %** for Projects.
- **Data export:** One-click CSV → published as a web demo.

## Screenshots
<p align="center">
  <img src="docs/screenshots/dashboard.png" width="49%">
  <img src="docs/screenshots/entry_form.png" width="49%">
</p>

## Quick Start (Desktop)
```bash
python -m venv .venv && source .venv/bin/activate  # (or .venv\Scripts\activate on Windows)
pip install -r requirements.txt
python app/main.py
