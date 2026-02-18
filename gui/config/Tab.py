import tkinter as tk
import tkinter.ttk as ttk
import config

class Tab():
    def __init__(self, tab):
        '''Config tab in app window'''
        self.tab = tab
        self.joysticks = {}
        self.configModel = {
            'translation_method': tk.IntVar(value=1),
            'joystick_resolution': tk.IntVar(value=500),
            'autocenter': tk.BooleanVar(value=False),
            'autocenter_key': tk.StringVar(value="c"),
            'selected_joystick': tk.StringVar(value="None"),
            'joystick_x_axis': tk.StringVar(value="None"),
            'joystick_x_inverted': tk.BooleanVar(value=False),
            'joystick_y_axis': tk.StringVar(value="None"),
            'joystick_y_inverted': tk.BooleanVar(value=False),
            'mouse_left': tk.StringVar(value="None"),
            'mouse_left_inverted': tk.BooleanVar(value=False),
            'mouse_right': tk.StringVar(value="None"),
            'mouse_right_inverted': tk.BooleanVar(value=False),
            'mouse_middle': tk.StringVar(value="None"),
            'mouse_middle_inverted': tk.BooleanVar(value=False),

            'activation_method': tk.IntVar(value=1),
            'selected_buttonbox': tk.StringVar(value="None"),
            'activation_button': tk.StringVar(value="None"),
            'activation_button_inverted': tk.BooleanVar(value=False),
            'deactivation_button': tk.StringVar(value="None"),
            'deactivation_button_inverted': tk.BooleanVar(value=False),
        }
        self.activation_button_display = tk.StringVar(value="None")
        self.deactivation_button_display = tk.StringVar(value="None")
        self.joystick_x_axis_display = tk.StringVar(value="None")
        self.joystick_y_axis_display = tk.StringVar(value="None")

        self.translation_frame = ttk.Frame(self.tab)
        self.translation_frame.pack(side="top", fill="x")

        # Translation method selection
        self.translation_label = ttk.Label(
            self.translation_frame,
            text="Translation method:",
            font="TkDefaultFont 10 bold"
        )
        self.translation_label.pack(side="top", fill="x", padx=10, pady=6)

        self.translation_methods = {
            1: "Absolute - From last mouse position before activation",
            2: "Absolute - From center of screen (Screen size limited)",
            3: "Emulate mouse movement based on joystick position",
        }

        for key, value in self.translation_methods.items():
            ttk.Radiobutton(
                self.translation_frame,
                text=value,
                variable=self.configModel['translation_method'],
                value=key,
            ).pack(side="top", fill="x", padx=10)

        # Sensitivity slider
        self.sensitivity_frame = ttk.Frame(self.tab)
        self.sensitivity_frame.pack(side="top", fill="x")

        self.sensitivity_label = ttk.Label(
            self.sensitivity_frame,
            text="Sensitivity:",
            font="TkDefaultFont 10 bold"
        )
        self.sensitivity_label.pack(side="top", fill="x", padx=10, pady=(6, 0))

        self.sensitivity_control_frame = ttk.Frame(self.sensitivity_frame)
        self.sensitivity_control_frame.pack(side="top", fill="x")

        self.sensitivity_slider = tk.Scale(
            self.sensitivity_control_frame,
            from_=1,
            to=4000,
            resolution=1,
            orient=tk.HORIZONTAL,
            variable=self.configModel['joystick_resolution'],
            showvalue=False,
        )
        self.sensitivity_slider.pack(side="left", fill="x", expand=True, padx=10, pady=0)

        self.sensitivity_spinbox = ttk.Spinbox(
            self.sensitivity_control_frame,
            from_=1,
            to=4000,
            textvariable=self.configModel['joystick_resolution'],
            width=6,
        )
        self.sensitivity_spinbox.pack(side="left", padx=(0, 10))

        self.autocenter_frame = ttk.Frame(self.tab)
        self.autocenter_frame.pack(side="top", fill="x")

        # Autocenter option
        self.center_option = ttk.Checkbutton(
            self.autocenter_frame,
            text="Autocenter:",
            variable=self.configModel['autocenter'],
            command=self.updater_autocenter,
            width=10
        )
        self.center_option.pack(side="left", padx=10, pady=6)

        self.joystick_gap_frame = ttk.Frame(self.tab)
        self.joystick_gap_frame.pack(side="top", fill="x")

        self.joystick_frame = ttk.Frame(self.tab)
        self.joystick_frame.pack(side="top", fill="x")

        self.joystick_select_label = ttk.Label(
            self.joystick_frame,
            text="Joystick for mouse control:",
            font="TkDefaultFont 10 bold"
        )
        self.joystick_select_label.pack(side="top", fill="x", padx=10, pady=6)

        # X axis selection
        self.x_axis_frame = ttk.Frame(self.tab)
        self.x_axis_frame.pack(side="top", fill="x", pady=6)

        # Y axis selection
        self.y_axis_frame = ttk.Frame(self.tab)
        self.y_axis_frame.pack(side="top", fill="x", pady=6)

        # Left mouse button selection
        self.mouse_left_frame = ttk.Frame(self.tab)
        self.mouse_left_frame.pack(side="top", fill="x", pady=6)

        # Middle mouse button selection
        self.mouse_middle_frame = ttk.Frame(self.tab)
        self.mouse_middle_frame.pack(side="top", fill="x", pady=6)

        # Right mouse button selection
        self.mouse_right_frame = ttk.Frame(self.tab)
        self.mouse_right_frame.pack(side="top", fill="x", pady=6)

        # Activation method selection
        self.activation_method_frame = ttk.Frame(self.tab)
        self.activation_method_frame.pack(side="top", fill="x", pady=6)

        self.activation_method_label = ttk.Label(
            self.activation_method_frame,
            text="Activation method:",
            font="TkDefaultFont 10 bold"
        )
        self.activation_method_label.pack(side="top", fill="x", padx=10, pady=6)

        self.activation_method_options = {
            1: "Hold button",
            2: "Toggle button",
            3: "On/Off button"
        }

        for key, value in self.activation_method_options.items():
            ttk.Radiobutton(
                self.activation_method_frame,
                text=value,
                variable=self.configModel['activation_method'],
                value=key,
                command=self.update_button_selection
            ).pack(side="top", fill="x", padx=10)

        # Buttonbox selection
        self.buttonbox_frame = ttk.Frame(self.tab)
        self.buttonbox_frame.pack(side="top", fill="x", pady=6)

        self.joystick_select_label = ttk.Label(
            self.buttonbox_frame,
            text="Button box for activation:",
            font="TkDefaultFont 10 bold"
        )
        self.joystick_select_label.pack(side="top", fill="x", padx=10, pady=6)

        # Activate button
        self.activate_btn_frame = ttk.Frame(self.tab)
        self.activate_btn_frame.pack(side="top", fill="x", pady=6)

        # Deactivate button
        self.deactivate_btn_frame = ttk.Frame(self.tab)
        self.deactivate_btn_frame.pack(side="top", fill="x", pady=6)


    def update_config(self):
        # Always store axis/button as int or None, not string 'None'
        axis_keys = ['joystick_x_axis', 'joystick_y_axis', 'activation_button', 'deactivation_button']
        # GUI uses 'mouse_left'/'mouse_right'/'mouse_middle' (1-indexed), data model uses '*_button' keys (0-indexed)
        button_keys = {'mouse_left': 'mouse_left_button', 'mouse_right': 'mouse_right_button', 'mouse_middle': 'mouse_middle_button'}
        for key, value in self.configModel.items():
            v = value.get()
            if key in axis_keys:
                if v == "None" or v == "" or v is None:
                    config.data.configModel[key] = None
                else:
                    try:
                        config.data.configModel[key] = int(v)
                    except Exception:
                        config.data.configModel[key] = None
            elif key in button_keys:
                if v == "None" or v == "" or v is None:
                    config.data.configModel[button_keys[key]] = None
                else:
                    try:
                        config.data.configModel[button_keys[key]] = int(v) - 1  # convert 1-indexed display to 0-indexed
                    except Exception:
                        config.data.configModel[button_keys[key]] = None
            else:
                config.data.configModel[key] = v

        config.data.configModel['selected_joystick_uuid'] = self.get_selected_joystick()
        config.data.configModel['selected_buttonbox_uuid'] = self.get_selected_buttonbox()


    def update_device_list(self, joysticks):
        self.joysticks = joysticks
        self.update_joystick_selection()
        self.update_axis_selection()
        self.update_buttonbox_selection()


    def updater_autocenter(self):
        try:
            self.autocenter_list_label.destroy()
            self.autocenter_list.destroy()
        except (AttributeError, tk.TclError):
            pass

        if self.configModel['autocenter'].get():
            self.autocenter_list_label = ttk.Label(
                self.autocenter_frame,
                text="Key*:",
                width=5
            )
            self.autocenter_list_label.pack(side="left", padx=10)

            self.autocenter_list = ttk.Entry(
                self.autocenter_frame,
                textvariable=self.configModel['autocenter_key'],
                width=10,
            )
            self.autocenter_list.pack(side="left", fill="x", padx=10)


    def update_joystick_selection(self):
        try:
            self.joystick_list.destroy()
        except (AttributeError, tk.TclError):
            pass

        joystick_list_values = ['None']
        for device in self.joysticks.values():
            joystick_list_values.append(device.get_name())

        self.joystick_list = ttk.Combobox(
            self.joystick_frame,
            values=joystick_list_values,
            textvariable=self.configModel['selected_joystick'],
            state="readonly",
        )
        self.joystick_list.bind('<<ComboboxSelected>>', self.update_axis_selection)
        self.joystick_list.pack(side="top", fill="x", padx=10)


    def update_buttonbox_selection(self):
        try:
            self.buttonbox_list.destroy()
        except (AttributeError, tk.TclError):
            pass

        buttonbox_list_values = ['None']
        for device in self.joysticks.values():
            buttonbox_list_values.append(device.get_name())

        self.buttonbox_list = ttk.Combobox(
            self.buttonbox_frame,
            values=buttonbox_list_values,
            textvariable=self.configModel['selected_buttonbox'],
            state="readonly",
        )
        self.buttonbox_list.bind('<<ComboboxSelected>>', self.update_button_selection)
        self.buttonbox_list.pack(side="top", fill="x", padx=10)


    def update_axis_selection(self, _event=None):
        try:
            self.x_axis_label.destroy()
            self.x_axis_list.destroy()
            self.x_axis_inverted.destroy()
            self.configModel['joystick_x_axis'].set("None")
            self.configModel['joystick_x_inverted'].set(False)

            self.y_axis_label.destroy()
            self.y_axis_list.destroy()
            self.y_axis_inverted.destroy()
            self.configModel['joystick_y_axis'].set("None")
            self.configModel['joystick_y_inverted'].set(False)

            self.left_mouse_button_label.destroy()
            self.left_mouse_button_list.destroy()
            self.left_mouse_inverted.destroy()
            self.configModel['mouse_left'].set("None")
            self.configModel['mouse_left_inverted'].set(False)

            self.right_mouse_button_label.destroy()
            self.right_mouse_button_list.destroy()
            self.right_mouse_inverted.destroy()
            self.configModel['mouse_right'].set("None")
            self.configModel['mouse_right_inverted'].set(False)

            self.middle_mouse_button_label.destroy()
            self.middle_mouse_button_list.destroy()
            self.middle_mouse_inverted.destroy()
            self.configModel['mouse_middle'].set("None")
            self.configModel['mouse_middle_inverted'].set(False)
        except (AttributeError, tk.TclError):
            pass

        for row in (self.x_axis_frame, self.y_axis_frame, self.mouse_left_frame, self.mouse_middle_frame, self.mouse_right_frame):
            row.pack_forget()

        if self.configModel['selected_joystick'].get() != "None":
            self.x_axis_frame.pack(side="top", fill="x", pady=6, after=self.joystick_frame)
            self.y_axis_frame.pack(side="top", fill="x", pady=6, after=self.x_axis_frame)
            self.mouse_left_frame.pack(side="top", fill="x", pady=6, after=self.y_axis_frame)
            self.mouse_middle_frame.pack(side="top", fill="x", pady=6, after=self.mouse_left_frame)
            self.mouse_right_frame.pack(side="top", fill="x", pady=6, after=self.mouse_middle_frame)

            for device in self.joysticks.values():
                if device.get_name() == self.configModel['selected_joystick'].get():
                    axis_list = ["None"]
                    axis_list.extend([x+1 for x in range(device.get_numaxes())])
                    button_list = ["None"]
                    button_list.extend([x+1 for x in range(device.get_numbuttons())])

                    # X axis selection
                    self.x_axis_label = ttk.Label(
                        self.x_axis_frame,
                        text="X axis*:",
                        width=10
                    )
                    self.x_axis_label.pack(side="left", padx=10)

                    self.x_axis_list = ttk.Combobox(
                        self.x_axis_frame,
                        values=axis_list,
                        state="readonly",
                        textvariable=self.joystick_x_axis_display,
                    )
                    current_x = self.configModel['joystick_x_axis'].get()
                    if current_x != "None":
                        try:
                            self.joystick_x_axis_display.set(str(int(current_x) + 1))
                        except Exception:
                            self.joystick_x_axis_display.set("None")
                    else:
                        self.joystick_x_axis_display.set("None")

                    def on_x_axis_selected(event=None):
                        val = self.joystick_x_axis_display.get()
                        if val == "None":
                            self.configModel['joystick_x_axis'].set("None")
                        else:
                            try:
                                self.configModel['joystick_x_axis'].set(str(int(val) - 1))
                            except Exception:
                                self.configModel['joystick_x_axis'].set("None")

                    self.x_axis_list.bind('<<ComboboxSelected>>', on_x_axis_selected)

                    self.x_axis_inverted = ttk.Checkbutton(
                        self.x_axis_frame,
                        text="Inverted",
                        variable=self.configModel['joystick_x_inverted'],
                    )
                    self.x_axis_inverted.pack(side="right", padx=(0, 10))
                    self.x_axis_list.pack(side="left", fill="x", expand=True, padx=10)

                    # Y axis selection
                    self.y_axis_label = ttk.Label(
                        self.y_axis_frame,
                        text="Y axis*:",
                        width=10
                    )
                    self.y_axis_label.pack(side="left", padx=10)

                    self.y_axis_list = ttk.Combobox(
                        self.y_axis_frame,
                        values=axis_list,
                        state="readonly",
                        textvariable=self.joystick_y_axis_display,
                    )
                    current_y = self.configModel['joystick_y_axis'].get()
                    if current_y != "None":
                        try:
                            self.joystick_y_axis_display.set(str(int(current_y) + 1))
                        except Exception:
                            self.joystick_y_axis_display.set("None")
                    else:
                        self.joystick_y_axis_display.set("None")

                    def on_y_axis_selected(event=None):
                        val = self.joystick_y_axis_display.get()
                        if val == "None":
                            self.configModel['joystick_y_axis'].set("None")
                        else:
                            try:
                                self.configModel['joystick_y_axis'].set(str(int(val) - 1))
                            except Exception:
                                self.configModel['joystick_y_axis'].set("None")

                    self.y_axis_list.bind('<<ComboboxSelected>>', on_y_axis_selected)

                    self.y_axis_inverted = ttk.Checkbutton(
                        self.y_axis_frame,
                        text="Inverted",
                        variable=self.configModel['joystick_y_inverted'],
                    )
                    self.y_axis_inverted.pack(side="right", padx=(0, 10))
                    self.y_axis_list.pack(side="left", fill="x", expand=True, padx=10)

                    # Left mouse button selection
                    self.left_mouse_button_label = ttk.Label(
                        self.mouse_left_frame,
                        text="Left:",
                        width=10
                    )
                    self.left_mouse_button_label.pack(side="left", padx=10)

                    self.left_mouse_button_list = ttk.Combobox(
                        self.mouse_left_frame,
                        values=button_list,
                        state="readonly",
                        textvariable=self.configModel['mouse_left'],
                    )
                    self.left_mouse_inverted = ttk.Checkbutton(
                        self.mouse_left_frame,
                        text="Inverted",
                        variable=self.configModel['mouse_left_inverted'],
                    )
                    self.left_mouse_inverted.pack(side="right", padx=(0, 10))
                    self.left_mouse_button_list.pack(side="left", fill="x", expand=True, padx=10)

                    # Right mouse button selection
                    self.right_mouse_button_label = ttk.Label(
                        self.mouse_right_frame,
                        text="Right:",
                        width=10
                    )
                    self.right_mouse_button_label.pack(side="left", padx=10)

                    self.right_mouse_button_list = ttk.Combobox(
                        self.mouse_right_frame,
                        values=button_list,
                        state="readonly",
                        textvariable=self.configModel['mouse_right'],
                    )
                    self.right_mouse_inverted = ttk.Checkbutton(
                        self.mouse_right_frame,
                        text="Inverted",
                        variable=self.configModel['mouse_right_inverted'],
                    )
                    self.right_mouse_inverted.pack(side="right", padx=(0, 10))
                    self.right_mouse_button_list.pack(side="left", fill="x", expand=True, padx=10)

                    # Middle mouse button selection
                    self.middle_mouse_button_label = ttk.Label(
                        self.mouse_middle_frame,
                        text="Middle:",
                        width=10
                    )
                    self.middle_mouse_button_label.pack(side="left", padx=10)

                    self.middle_mouse_button_list = ttk.Combobox(
                        self.mouse_middle_frame,
                        values=button_list,
                        state="readonly",
                        textvariable=self.configModel['mouse_middle'],
                    )
                    self.middle_mouse_inverted = ttk.Checkbutton(
                        self.mouse_middle_frame,
                        text="Inverted",
                        variable=self.configModel['mouse_middle_inverted'],
                    )
                    self.middle_mouse_inverted.pack(side="right", padx=(0, 10))
                    self.middle_mouse_button_list.pack(side="left", fill="x", expand=True, padx=10)


    def update_button_selection(self, _event=None):
        try:
            self.activate_button_label.destroy()
            self.activate_button_list.destroy()
            self.activate_button_inverted.destroy()
            self.configModel['activation_button'].set("None")
            self.configModel['activation_button_inverted'].set(False)

            self.deactivate_button_label.destroy()
            self.deactivation_button_list.destroy()
            self.deactivate_button_inverted.destroy()
            self.configModel['deactivation_button'].set("None")
            self.configModel['deactivation_button_inverted'].set(False)
        except (AttributeError, tk.TclError):
            pass

        if self.configModel['selected_buttonbox'].get() != "None":
            for device in self.joysticks.values():
                if device.get_name() == self.configModel['selected_buttonbox'].get():
                    button_list = ["None"]
                    button_list.extend([x+1 for x in range(device.get_numbuttons())])

                    # Activate button selection
                    self.activate_button_label = ttk.Label(
                        self.activate_btn_frame,
                        text="Activate*:",
                        width=10
                    )
                    self.activate_button_label.pack(side="left", padx=10)

                    self.activate_button_list = ttk.Combobox(
                        self.activate_btn_frame,
                        values=button_list,
                        state="readonly",
                        textvariable=self.activation_button_display,
                    )

                    def on_activation_button_selected(event=None):
                        val = self.activation_button_display.get()
                        if val != "None":
                            self.configModel['activation_button'].set(str(int(val) - 1))
                        else:
                            self.configModel['activation_button'].set("None")

                    self.activate_button_list.bind("<<ComboboxSelected>>", on_activation_button_selected)

                    # Sync display with model on load
                    val = self.configModel['activation_button'].get()
                    if val != "None":
                        self.activation_button_display.set(str(int(val) + 1))
                    else:
                        self.activation_button_display.set("None")

                    self.activate_button_inverted = ttk.Checkbutton(
                        self.activate_btn_frame,
                        text="Inverted",
                        variable=self.configModel['activation_button_inverted'],
                    )
                    self.activate_button_inverted.pack(side="right", padx=(0, 10))
                    self.activate_button_list.pack(side="left", fill="x", expand=True, padx=10)

                    # Deactivate button selection
                    if self.configModel['activation_method'].get() == 3:
                        self.deactivate_button_label = ttk.Label(
                            self.deactivate_btn_frame,
                            text="Deactivate*: ",
                            width=10
                        )
                        self.deactivate_button_label.pack(side="left", padx=10)

                        self.deactivation_button_list = ttk.Combobox(
                            self.deactivate_btn_frame,
                            values=button_list,
                            state="readonly",
                            textvariable=self.deactivation_button_display,
                        )

                        def on_deactivation_button_selected(event=None):
                            val = self.deactivation_button_display.get()
                            if val != "None":
                                self.configModel['deactivation_button'].set(str(int(val) - 1))
                            else:
                                self.configModel['deactivation_button'].set("None")

                        self.deactivation_button_list.bind("<<ComboboxSelected>>", on_deactivation_button_selected)

                        # Sync display with model on load
                        val = self.configModel['deactivation_button'].get()
                        if val != "None":
                            self.deactivation_button_display.set(str(int(val) + 1))
                        else:
                            self.deactivation_button_display.set("None")

                        self.deactivate_button_inverted = ttk.Checkbutton(
                            self.deactivate_btn_frame,
                            text="Inverted",
                            variable=self.configModel['deactivation_button_inverted'],
                        )
                        self.deactivate_button_inverted.pack(side="right", padx=(0, 10))
                        self.deactivation_button_list.pack(side="left", fill="x", expand=True, padx=10)


    ###########################################
    #
    #  GUI Setters and getters
    #
    ###########################################

    def get_translation_method(self):
        return self.configModel['translation_method'].get()


    def set_translation_method(self, value):
        self.configModel['translation_method'].set(value)


    def get_autocenter(self):
        return self.configModel['autocenter'].get()


    def set_autocenter(self, value):
        self.configModel['autocenter'].set(value)
        self.updater_autocenter()


    def get_autocenter_key(self):
        if self.configModel['autocenter_key'].get() == "":
            return None
        else:
            return self.configModel['autocenter_key'].get()


    def set_autocenter_key(self, value):
        if value == "None":
            self.configModel['autocenter_key'].set("")
        else:
            self.configModel['autocenter_key'].set(value)


    def get_joystick_resolution(self):
        return self.configModel['joystick_resolution'].get()


    def set_joystick_resolution(self, value):
        self.configModel['joystick_resolution'].set(value)


    def get_selected_joystick(self):
        selected_name = self.configModel['selected_joystick'].get()
        if selected_name != "None":
            for device in self.joysticks.values():
                if device.get_name() == selected_name:
                    return device.get_guid()
        else:
            return None


    def set_selected_joystick(self, guid):
        if guid != None:
            for device in self.joysticks.values():
                if device.get_guid() == guid:
                    value = device.get_name()
                    self.configModel['selected_joystick'].set(value)
                    self.update_axis_selection()
                    return True

            return False


    def get_joystick_x_axis(self):
        selected_x_axis = self.configModel['joystick_x_axis'].get()
        if selected_x_axis != "None":
            return int(selected_x_axis)
        else:
            return None


    def set_joystick_x_axis(self, value):
        if value != "None":
            self.configModel['joystick_x_axis'].set(int(value))
        else:
            self.configModel['joystick_x_axis'].set("None")


    def get_joystick_y_axis(self):
        selected_y_axis = self.configModel['joystick_y_axis'].get()
        if selected_y_axis != "None":
            return int(selected_y_axis)
        else:
            return None


    def set_joystick_y_axis(self, value):
        if value != "None":
            self.configModel['joystick_y_axis'].set(int(value))
        else:
            self.configModel['joystick_y_axis'].set("None")


    def get_joystick_x_inverted(self):
        return self.configModel['joystick_x_inverted'].get()


    def set_joystick_x_inverted(self, value):
        return self.configModel['joystick_x_inverted'].set(value)


    def get_joystick_y_inverted(self):
        return self.configModel['joystick_y_inverted'].get()


    def set_joystick_y_inverted(self, value):
        return self.configModel['joystick_y_inverted'].set(value)


    def get_activation_method(self):
        return self.configModel['activation_method'].get()


    def set_activation_method(self, value):
        self.configModel['activation_method'].set(value)
        self.update_button_selection()


    def get_selected_buttonbox(self):
        selected_name = self.configModel['selected_buttonbox'].get()
        if selected_name != "None":
            for device in self.joysticks.values():
                if device.get_name() == selected_name:
                    return device.get_guid()
        else:
            return None


    def set_selected_buttonbox(self, guid):
        if guid != None:
            for device in self.joysticks.values():
                if device.get_guid() == guid:
                    value = device.get_name()
                    self.configModel['selected_buttonbox'].set(value)
                    self.update_button_selection()
                    return True

            return False


    def get_activation_button(self):
        val = self.configModel['activation_button'].get()
        if val != "None":
            return str(int(val) + 1)
        else:
            return "None"


    def set_activation_button(self, value):
        if value != "None":
            self.configModel['activation_button'].set(str(int(value) - 1))
        else:
            self.configModel['activation_button'].set("None")


    def get_activation_button_inverted(self):
        return self.configModel['activation_button_inverted'].get()


    def set_activation_button_inverted(self, value):
        return self.configModel['activation_button_inverted'].set(value)


    def get_deactivation_button(self):
        selected_button = self.configModel['deactivation_button'].get()
        if selected_button != "None":
            return int(selected_button) - 1
        else:
            return None


    def set_deactivation_button(self, value):
        if value != "None":
            self.configModel['deactivation_button'].set(int(value)+1)
        else:
            self.configModel['deactivation_button'].set("None")


    def get_deactivation_button_inverted(self):
        return self.configModel['deactivation_button_inverted'].get()


    def set_deactivation_button_inverted(self, value):
        return self.configModel['deactivation_button_inverted'].set(value)


    def get_mouse_left(self):
        selected_button = self.configModel['mouse_left'].get()
        if selected_button != "None":
            return int(selected_button) - 1
        else:
            return None


    def set_mouse_left(self, value):
        if value != "None":
            self.configModel['mouse_left'].set(int(value)+1)
        else:
            self.configModel['mouse_left'].set("None")


    def get_mouse_left_inverted(self):
        return self.configModel['mouse_left_inverted'].get()


    def set_mouse_left_inverted(self, value):
        return self.configModel['mouse_left_inverted'].set(value)


    def get_mouse_right(self):
        selected_button = self.configModel['mouse_right'].get()
        if selected_button != "None":
            return int(selected_button) - 1
        else:
            return None


    def set_mouse_right(self, value):
        if value != "None":
            self.configModel['mouse_right'].set(int(value)+1)
        else:
            self.configModel['mouse_right'].set("None")


    def get_mouse_right_inverted(self):
        return self.configModel['mouse_right_inverted'].get()


    def set_mouse_right_inverted(self, value):
        return self.configModel['mouse_right_inverted'].set(value)


    def get_mouse_middle(self):
        selected_button = self.configModel['mouse_middle'].get()
        if selected_button != "None":
            return int(selected_button) - 1
        else:
            return None


    def set_mouse_middle(self, value):
        if value != "None":
            self.configModel['mouse_middle'].set(int(value)+1)
        else:
            self.configModel['mouse_middle'].set("None")


    def get_mouse_middle_inverted(self):
        return self.configModel['mouse_middle_inverted'].get()


    def set_mouse_middle_inverted(self, value):
        return self.configModel['mouse_middle_inverted'].set(value)


    def populate_from_config(self, model):
        '''Populate all GUI widgets from a loaded config data model.'''
        self.set_translation_method(model['translation_method'])
        self.set_joystick_resolution(model['joystick_resolution'])
        self.set_autocenter(model['autocenter'])
        self.set_autocenter_key(model['autocenter_key'] or "None")

        # Set joystick by name and rebuild axis UI
        joystick_name = model.get('joystick_selected') or 'None'
        self.configModel['selected_joystick'].set(joystick_name)
        self.update_axis_selection()

        # Restore axis/button values after update_axis_selection clears them
        x_axis = model['joystick_x_axis']
        if x_axis not in (None, 'None'):
            self.configModel['joystick_x_axis'].set(str(x_axis))
            self.joystick_x_axis_display.set(str(int(x_axis) + 1))
        self.configModel['joystick_x_inverted'].set(model['joystick_x_inverted'])

        y_axis = model['joystick_y_axis']
        if y_axis not in (None, 'None'):
            self.configModel['joystick_y_axis'].set(str(y_axis))
            self.joystick_y_axis_display.set(str(int(y_axis) + 1))
        self.configModel['joystick_y_inverted'].set(model['joystick_y_inverted'])

        mouse_left = model['mouse_left_button']
        self.set_mouse_left(mouse_left if mouse_left is not None else "None")
        self.configModel['mouse_left_inverted'].set(model['mouse_left_inverted'])

        mouse_right = model['mouse_right_button']
        self.set_mouse_right(mouse_right if mouse_right is not None else "None")
        self.configModel['mouse_right_inverted'].set(model['mouse_right_inverted'])

        mouse_middle = model['mouse_middle_button']
        self.set_mouse_middle(mouse_middle if mouse_middle is not None else "None")
        self.configModel['mouse_middle_inverted'].set(model['mouse_middle_inverted'])

        # Set activation method and rebuild button UI
        self.set_activation_method(model['activation_method'])
        buttonbox_name = model.get('buttonbox_selected') or 'None'
        self.configModel['selected_buttonbox'].set(buttonbox_name)
        self.update_button_selection()

        # Restore button values after update_button_selection clears them
        activation_btn = model['activation_button']
        if activation_btn is not None:
            self.configModel['activation_button'].set(str(activation_btn))
            self.activation_button_display.set(str(activation_btn + 1))
        self.configModel['activation_button_inverted'].set(model['activation_button_inverted'])

        deactivation_btn = model['deactivation_button']
        if deactivation_btn is not None:
            self.configModel['deactivation_button'].set(str(deactivation_btn))
            self.deactivation_button_display.set(str(deactivation_btn + 1))
        self.configModel['deactivation_button_inverted'].set(model['deactivation_button_inverted'])
