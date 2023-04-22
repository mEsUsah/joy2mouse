import tkinter as tk
import tkinter.ttk as ttk
import gui

class Tab():
    def __init__(self, tab):
        '''This is the main tab for running the application'''
        self.armed = tk.BooleanVar(value=False)
        self.running = False
        
        self.tab = tab
        self.row_1 = ttk.Frame(self.tab)
        self.row_1.pack(side="top", expand=1, fill="both")

        self.row_1_label = ttk.Label(
            self.row_1, 
            text="Arm, then activate on joystick:",
            font="TkDefaultFont 10 bold"
        )
        self.row_1_label.pack(side="top", fill="x", padx=10, pady=6)

        self.arm_button = ttk.Checkbutton(
            self.row_1,
            text="Arm",
            variable=self.armed,
            command=self.update_status
        )
        self.arm_button.pack(side="top", fill="x", padx=10)

        self.status_label = ttk.Label(
            self.row_1,
            text="Disarmed",
            foreground="white",
            background="green",
            font=("Helvetica", 16),
            anchor="center",
            padding=20,
            border=2,
            borderwidth=2
        )
        self.status_label.pack(side="bottom", fill="x", padx=10, pady=6)

    def get_armed(self):
        return self.armed.get()


    def enable_arming(self):
        self.arm_button.config(state="normal")


    def disable_arming(self):
        self.arm_button.config(state="disabled")

    def set_run_status(self, status):
        self.running = status
        self.update_status()

    def update_status(self):
        if self.running:
            self.status_label.config(
                text="Running",
                foreground="white",
                background="red"
            )
        elif self.armed.get() and not self.running:
            self.status_label.config(
                text="Armed",
                foreground="white",
                background="orange"
            )
        else:
            self.status_label.config(
                text="Disarmed",
                foreground="white",
                background="green"
            )