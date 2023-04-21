import tkinter as tk
import tkinter.ttk as ttk
import gui

class Tab():
    def __init__(self, tab):
        '''This is the test tab for running the application'''
        self.joysticks = {}
        
        self.row_1 = ttk.Frame(tab)
        self.row_1.pack(side="top", expand=1, fill="both")


    def update_device_list(self, joysticks):
        self.joysticks = joysticks
        # destroy all widgets in frame
        for widget in self.row_1.winfo_children():
            widget.destroy()

        # add label
        self.device_list_label = ttk.Label(
            self.row_1, 
            text="Connected devices:",
            font="TkDefaultFont 10 bold"
        )
        self.device_list_label.pack(side="top", fill="x", padx=10, pady=(6,6))

        # add new widgets for each device
        for device in self.joysticks.values():
            ttk.Label(
                self.row_1,
                text=device.get_name(),
            ).pack(side="top", fill="x", padx=10)
            ttk.Label(
                self.row_1,
                text="GUID: " + device.get_guid(),
                font="TkDefaultFont 8",
            ).pack(side="top", fill="x", padx=10, pady=(0,8))
