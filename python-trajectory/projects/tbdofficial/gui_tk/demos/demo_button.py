# Author:      Miguel Gonzalez Almonte  # Created:     2025-05-24  # File:        demo_button.py  # Description: Button demo for Tkinter  
# registry_tk.py
# Dynamically loads demo_* modules from gui_tk/demos/

import importlib.util
import os
import sys
from pathlib import Path

def get_registered_demos():
    demo_classes = []
    demos_path = Path(__file__).parent / "demos"

    for file in os.listdir(demos_path):
        if file.startswith("demo_") and file.endswith(".py"):
            module_name = file[:-3]
            full_path = demos_path / file

            spec = importlib.util.spec_from_file_location(module_name, full_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)

                for name in dir(module):
                    obj = getattr(module, name)
                    if isinstance(obj, type):
                        demo_classes.append(obj)

    return demo_classes
