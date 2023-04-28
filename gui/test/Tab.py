import tkinter as tk
import tkinter.ttk as ttk
import gui
import os
import math

class Tab():
    def __init__(self, tab):
        '''This is the test tab for running the application'''
        self.joysticks = {}
        self.device_data= {}
        
        self.row_1 = ttk.Frame(tab)
        self.row_1.pack(side="top", expand=1, fill="both")

        self.row_2 = ttk.Frame(tab)
        self.row_2.pack(side="top", expand=1, fill="both")

        self.open_win_joystick = ttk.Button(
            self.row_2,
            text="Open Window Joystick Properties",
            command=self.open_win_joystick,
        )
        self.open_win_joystick.pack(side="bottom", fill="x", padx=10, pady=10)


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
        self.device_data = {}
        for device_index, device in enumerate(self.joysticks.values()):
            self.device_data[device_index] = {}
            ttk.Label(
                self.row_1,
                text=device.get_name(),
            ).pack(side="top", fill="x", padx=10)
            ttk.Label(
                self.row_1,
                text=f"GUID: {device.get_guid()}",
                font="TkDefaultFont 8",
            ).pack(side="top", fill="x", padx=10, pady=(0,8))
            
            # Add Axis
            axis = device.get_numaxes()
            if axis:
                self.device_data[device_index]['axis'] = []
                for i in range(axis):
                    axis_row = ttk.Frame(self.row_1)
                    axis_row.pack(side="top", fill="x", padx=10, pady=(0,4))

                    axis_label = ttk.Label(
                        axis_row,
                        text=f"Axis {i+1}:",
                        font="TkDefaultFont 8",
                    )
                    axis_label.pack(side="left", padx=(0,10))

                    
                    canvas = tk.Canvas(axis_row,
                        width=200,
                        height=10,
                        highlightthickness=1,
                        highlightbackground="black",
                        background="white",
                    )
                    canvas.pack(side="left", fill="x")
                    self.device_data[device_index]['axis'].append(canvas)

            # Add Buttons
            buttons = device.get_numbuttons()
            if buttons:
                button_row = ttk.Frame(self.row_1, width=300)
                button_row.pack(side="top", fill="x", padx=10, pady=(0,4))
                nCols = 10
                cRows = math.ceil(buttons/nCols)

                canvas = tk.Canvas(
                    button_row,
                    width=240,
                    height=22*cRows,
                )
                canvas.pack(side="top", fill="x")

                for i in range(buttons):
                    canvas.create_rectangle(
                        2+(i%nCols)*24,
                        2+math.floor(i/nCols)*22,
                        10+(i%nCols)*24,
                        10+math.floor(i/nCols)*22,
                        fill="white",
                        outline="black",
                    )
                self.device_data[device_index]['buttons'] = canvas


    def update_axis_view(self):
        for device_index, device in enumerate(self.joysticks.values()):   
            for i in range(device.get_numaxes()):
                self.device_data[device_index]['axis'][i].delete("all")
                self.device_data[device_index]['axis'][i].create_rectangle(
                    1, 
                    1, 
                    int(device.get_axis(i)*100)+100, 
                    13, 
                    fill="red", 
                    outline=""
                )
            
            canvas = self.device_data[device_index]['buttons']
            canvas.delete("all")
            buttons = device.get_numbuttons()
            nCols = 10
            for i in range(buttons):
                if device.get_button(i):
                    canvas.create_rectangle(
                        2+(i%nCols)*24,
                        2+math.floor(i/nCols)*24,
                        22+(i%nCols)*24,
                        22+math.floor(i/nCols)*24,
                        fill="red",
                        outline="black",
                    )
                else:
                    canvas.create_rectangle(
                        2+(i%nCols)*24,
                        2+math.floor(i/nCols)*24,
                        22+(i%nCols)*24,
                        22+math.floor(i/nCols)*24,
                        fill="white",
                        outline="black",
                    )
                
        
    def open_win_joystick(self):
        os.system('%SystemRoot%\System32\joy.cpl')
