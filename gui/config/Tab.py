import tkinter as tk
import tkinter.ttk as ttk
import gui

class Tab():
    def __init__(self, tab):
        '''This is the config tab for running the application'''
        self.tab = tab
        self.showing_center_option = False
        self.translation_method = tk.IntVar(value=1)
        self.autocenter = tk.BooleanVar(value=False)
        
        self.row_1 = ttk.Frame(self.tab)
        self.row_1.pack(side="top", expand=1, fill="both")

        # Translation method selection
        self.transation_label = ttk.Label(
            self.row_1,
            text="Translation method:",
            font="TkDefaultFont 10 bold"
        )
        self.transation_label.pack(side="top", fill="x", padx=10, pady=6)

        self.transation_methods = {
            1: "Absolute - From last mouse position before activation",
            2: "Absolute - From center of screen",
            3: "Relative - Based on absolute joystick position",
        }

        for key, value in self.transation_methods.items():
            ttk.Radiobutton(
                self.row_1,
                text=value,
                variable=self.translation_method,
                value=key,
                command=self.update_options
            ).pack(side="top", fill="x", padx=10)
        
        self.row_2 = ttk.Frame(self.tab)
        self.row_2.pack(side="top", expand=1, fill="both")


    def get_translation_method(self):
        return self.translation_method.get()
    
    def get_autocenter(self):
        return self.autocenter.get()
    
    def update_options(self):
        if self.translation_method.get() != 1:
            if not self.showing_center_option:
                self.showing_center_option = True
                self.center_option = ttk.Checkbutton(
                    self.row_2,
                    text="Autocenter mouse",
                    variable=self.autocenter
                )
                self.center_option.pack(side="top", fill="x", padx=10, pady=6)
        else:
            self.center_option.destroy()
            self.showing_center_option = False
            self.autocenter.set(False)