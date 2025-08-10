# ============================================================
#  File:        start.py
#  Author:      Miguel Gonzalez Almonte
#  Created:     2025-05-20
#  Description: Launch script — initializes environment and starts the UI stack
# ------------------------------------------------------------
#  Project:     Unit Turn
#  Module:      System Bootstrap
#  Purpose:     Single entry point for app launch; configures path and delegates to launcher
# ============================================================

import sys
from pathlib import Path

# === Path Setup ===
ROOT_DIR = Path(__file__).resolve().parent
sys.path.append(str(ROOT_DIR))  # Ensures local module resolution

# === Launch Logic ===
try:
    from launcher import launch_app
except ImportError as e:
    print(f"[Startup Error] Failed to import launcher: {e}")
    sys.exit(1)

def main():
    try:
        launch_app()
    except Exception as e:
        print(f"[Fatal] Uncaught exception during app launch:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
