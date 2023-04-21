import tkinter as tk
import tkinter.ttk as ttk
import gui

class Tab():
    def __init__(self, tab):
        '''This is the config tab for running the application'''
        self.tab = tab
        self.translation_method = tk.IntVar(value=1)
        
        row_1 = ttk.Frame(self.tab)
        row_1.pack(side="top", expand=1, fill="both")

        # Translation method selection
        elmAddLabel1 = ttk.Label(row_1,text="Translation method")
        elmAddLabel1.pack(side="top", fill="x", padx=10, pady=6)

        transation_methods = {
            1: "Absolute - From last mouse position before activation",
            2: "Absolute - From center of screen",
            3: "Relative - Based on absolute joystick position",
        }

        for key, value in transation_methods.items():
            ttk.Radiobutton(
                row_1,
                text=value,
                variable=self.translation_method,
                value=key
            ).pack(side="top", fill="x", padx=10)

    def get_translation_method(self):
        return self.translation_method.get()



