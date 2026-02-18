import tkinter as tk
import tkinter.ttk as ttk
import utils
import os
import math

import config.data

_COLOR_PRESSED  = "red"
_COLOR_SELECTED = "#0099bb"   # teal — selected, not pressed
_COLOR_UNSEL    = "white"


class Tab():
    def __init__(self, tab):
        '''This is the test tab for running the application'''
        self.joysticks = {}
        self.device_data = {}
        self._frame_bg = ttk.Style().lookup("TFrame", "background") or "SystemButtonFace"

        self.button_height = 25
        self.button_margin = 2

        self.row_1 = utils.gui.VerticalScrolledFrame(
            tab,
            height=600,
            width=170,
        )
        self.row_1.pack(side="top", expand=1, fill="both")

        self.row_2 = ttk.Frame(tab)
        self.row_2.pack(side="top", expand=1, fill="both")

        self.open_win_joystick_button = ttk.Button(
            self.row_2,
            text="Open Window Joystick Properties",
            command=self.open_win_joystick,
        )
        self.open_win_joystick_button.pack(side="bottom", fill="x", padx=10, pady=10)

    def _roles_for_device(self, guid):
        """Return (axis_roles, btn_roles) dicts mapping index → role string for a device GUID."""
        m = config.data.configModel
        axis_roles = {}
        btn_roles  = {}

        if guid == m.get("selected_joystick_uuid"):
            xa = m.get("joystick_x_axis")
            ya = m.get("joystick_y_axis")
            if xa is not None: axis_roles[int(xa)] = "X"
            if ya is not None: axis_roles[int(ya)] = "Y"
            ml = m.get("mouse_left_button")
            mr = m.get("mouse_right_button")
            mm = m.get("mouse_middle_button")
            if ml is not None: btn_roles[int(ml)] = "L"
            if mr is not None: btn_roles[int(mr)] = "R"
            if mm is not None: btn_roles[int(mm)] = "M"

        if guid == m.get("selected_buttonbox_uuid"):
            ab = m.get("activation_button")
            db = m.get("deactivation_button")
            if ab is not None: btn_roles[int(ab)] = "A"
            if db is not None: btn_roles[int(db)] = "D"

        return axis_roles, btn_roles

    def update_device_list(self, joysticks):
        self.joysticks = joysticks
        for widget in self.row_1.interior.winfo_children():
            widget.destroy()

        self.device_list_label = ttk.Label(
            self.row_1.interior,
            text="Connected devices:",
            font="TkDefaultFont 10 bold"
        )
        self.device_list_label.pack(side="top", fill="x", padx=10, pady=(6, 6))

        self.device_data = {}
        for device_index, device in enumerate(self.joysticks.values()):
            self.device_data[device_index] = {"guid": device.get_guid()}

            ttk.Label(
                self.row_1.interior,
                text=device.get_name(),
            ).pack(side="top", fill="x", padx=10)
            ttk.Label(
                self.row_1.interior,
                text=f"GUID: {device.get_guid()}",
                font="TkDefaultFont 8",
            ).pack(side="top", fill="x", padx=10, pady=(0, 8))

            # Axes
            axis = device.get_numaxes()
            if axis:
                self.device_data[device_index]['axis']     = []
                self.device_data[device_index]['axis_ind'] = []
                for i in range(axis):
                    axis_row = ttk.Frame(self.row_1.interior)
                    axis_row.pack(side="top", fill="x", padx=10, pady=(0, 4))

                    ttk.Label(
                        axis_row,
                        text=f"Axis {i + 1}:",
                        font="TkDefaultFont 8",
                    ).pack(side="left", padx=(0, 10))

                    canvas = tk.Canvas(axis_row,
                        width=200, height=10,
                        highlightthickness=1, highlightbackground="black",
                        background="white",
                    )
                    canvas.pack(side="left", fill="x")
                    self.device_data[device_index]['axis'].append(canvas)

                    ind = tk.Label(axis_row, text="",
                                   width=2, anchor="center",
                                   fg="white", bg=self._frame_bg,
                                   padx=3, pady=1,
                                   highlightthickness=1,
                                   highlightbackground="black")
                    ind.pack(side="left", padx=(4, 0))
                    self.device_data[device_index]['axis_ind'].append(ind)

            # Buttons
            buttons = device.get_numbuttons()
            if buttons:
                button_row = ttk.Frame(self.row_1.interior, width=300)
                button_row.pack(side="top", fill="x", padx=10, pady=(0, 4))
                nCols = 10
                nRows = math.ceil(buttons / nCols)

                canvas = tk.Canvas(
                    button_row,
                    width=nCols * self.button_height + self.button_margin,
                    height=(self.button_height + self.button_margin) * nRows,
                )
                canvas.pack(side="top", anchor="center")
                self.device_data[device_index]['buttons'] = canvas

    def update_axis_view(self):
        for device_index, device in enumerate(self.joysticks.values()):
            guid = self.device_data[device_index].get("guid", "")
            axis_roles, btn_roles = self._roles_for_device(guid)

            # Axes
            axis = device.get_numaxes()
            if axis:
                axis_inds = self.device_data[device_index].get('axis_ind', [])
                for i in range(axis):
                    self.device_data[device_index]['axis'][i].delete("all")
                    self.device_data[device_index]['axis'][i].create_rectangle(
                        1, 1,
                        int(device.get_axis(i) * 100) + 100, 13,
                        fill="red", outline=""
                    )
                    role = axis_roles.get(i)
                    if i < len(axis_inds):
                        if role:
                            axis_inds[i].config(text=role, bg=_COLOR_SELECTED)
                        else:
                            axis_inds[i].config(text="", bg=self._frame_bg)

            # Buttons
            buttons = device.get_numbuttons()
            if buttons:
                canvas = self.device_data[device_index]['buttons']
                canvas.delete("all")
                nCols = 10
                for i in range(buttons):
                    pressed = device.get_button(i)
                    role    = btn_roles.get(i)

                    if pressed:
                        fill, text_fill, label = _COLOR_PRESSED,  "white", str(i + 1)
                    elif role:
                        fill, text_fill, label = _COLOR_SELECTED, "white", role
                    else:
                        fill, text_fill, label = _COLOR_UNSEL,    "black", str(i + 1)

                    x0 = self.button_margin + (i % nCols) * self.button_height
                    y0 = self.button_margin + math.floor(i / nCols) * self.button_height
                    x1 = self.button_height + (i % nCols) * self.button_height
                    y1 = self.button_height + math.floor(i / nCols) * self.button_height
                    cx = (self.button_height + self.button_margin) / 2 + (i % nCols) * self.button_height
                    cy = (self.button_height + self.button_margin) / 2 + math.floor(i / nCols) * self.button_height

                    canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline="black")
                    canvas.create_text(cx, cy, text=label, fill=text_fill)

    def open_win_joystick(self):
        os.system(r'%SystemRoot%\System32\joy.cpl')
