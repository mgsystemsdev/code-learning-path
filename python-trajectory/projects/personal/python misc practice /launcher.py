import sys
import json
import os

CONFIG_PATH = "system/config.json"

def get_launch_mode():
    for arg in sys.argv:
        if arg.startswith("--mode="):
            return arg.split("=")[-1].strip()

    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                config = json.load(f)
                return config.get("mode")
        except json.JSONDecodeError:
            print("⚠️ Error in config.json")

    return None
