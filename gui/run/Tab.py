import tkinter as tk
import tkinter.ttk as ttk
import gui

class Tab():
    def __init__(self, tab):
        '''This is the main tab for running the application'''
        self.armed = tk.BooleanVar(value=False)
        
        self.tab = tab
        self.row_1 = ttk.Frame(self.tab)
        self.row_1.pack(side="top", expand=1, fill="both")

        self.row_1_label = ttk.Label(
            self.row_1, 
            text="Arm to run, then activate to run"
        )
        self.row_1_label.pack(side="top", fill="x", padx=10, pady=6)

        self.arm_button = ttk.Checkbutton(
            self.row_1,
            text="Arm",
            variable=self.armed
        )
        self.arm_button.pack(side="top", fill="x", padx=10)

    def get_armed(self):
        return self.armed.get()