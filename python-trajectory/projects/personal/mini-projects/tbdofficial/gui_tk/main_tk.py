# Author:      Miguel Gonzalez Almonte  # Created:     2025-05-24  # File:        main_tk.py  # Description: Launches Tkinter showcase  
# main_tk.py
# Launches Tkinter demo showcase window

import tkinter as tk
from gui_tk.registry_tk import get_registered_demos

class MainTkApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter Demo Showcase")
        self.geometry("400x500")
        self.build_ui()

    def build_ui(self):
        for demo_class in get_registered_demos():
            btn = tk.Button(self, text=demo_class.__name__, command=lambda cls=demo_class: self.launch_demo(cls))
            btn.pack(pady=5, fill='x', padx=10)

    def launch_demo(self, demo_class):
        window = tk.Toplevel(self)
        demo_frame = demo_class(window)
        demo_frame.pack(fill='both', expand=True)

if __name__ == "__main__":
    app = MainTkApp()
    app.mainloop()
