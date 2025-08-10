# helpers.py
# 🧠 Utility helpers for folder naming

def ensure_folder_format(text: str) -> str:
    """
    Appends '/' if the label appears to be a folder.
    Folder = any name with no file extension (no dot).
    """
    if "." not in text and not text.endswith("/"):
        return text + "/"
    return text
