import tkinter as tk
import tkinter.ttk as ttk
import gui

class Tab():
    def __init__(self, tab):
        '''Config tab in app window'''
        self.tab = tab
        self.showing_center_option = False
        self.translation_method = tk.IntVar(value=1)
        self.joystick_resolution = tk.IntVar(value=16)
        self.autocenter = tk.BooleanVar(value=False)
        self.autocenter_key = tk.StringVar(value="c")

        self.joysticks = {}
        self.joystick_selected = tk.StringVar(value="None")
        
        self.joystick_x_selected = tk.StringVar(value="None")
        self.joystick_x_inverted = tk.BooleanVar(value=False)
        
        self.joystick_y_selected = tk.StringVar(value="None")
        self.joystick_y_inverted = tk.BooleanVar(value=False)

        self.mouse_left_selected = tk.StringVar(value="None")
        self.mouse_left_inverted = tk.BooleanVar(value=False)
        
        self.mouse_right_selected = tk.StringVar(value="None")
        self.mouse_right_inverted = tk.BooleanVar(value=False)

        self.activation_method = tk.IntVar(value=1)

        self.buttonbox_selected = tk.StringVar(value="None")
        self.buttonbox_activate_selected = tk.StringVar(value="None")
        self.buttonbox_activate_inverted = tk.BooleanVar(value=False)

        self.buttonbox_deactivate_selected = tk.StringVar(value="None")
        self.buttonbox_deactivate_inverted = tk.BooleanVar(value=False)
        

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
            2: "Absolute - From center of screen (Screen size limited)",
            3: "Emulate mouse movement based on joystick position",
        }

        for key, value in self.transation_methods.items():
            ttk.Radiobutton(
                self.row_1,
                text=value,
                variable=self.translation_method,
                value=key,
            ).pack(side="top", fill="x", padx=10)
        
        self.row_2 = ttk.Frame(self.tab)
        self.row_2.pack(side="top", expand=1, fill="both")

        # Autocenter option
        self.center_option = ttk.Checkbutton(
            self.row_2,
            text="Autocenter:",
            variable=self.autocenter,
            command=self.updater_autocenter,
            width=10
        )
        self.center_option.pack(side="left", padx=10, pady=6)

        self.row_13 = ttk.Frame(self.tab)
        self.row_13.pack(side="top", expand=1, fill="both")

        # Joystick resolution options
        self.transation_label = ttk.Label(
            self.row_1,
            text="Joystick resolution:",
            font="TkDefaultFont 10 bold"
        )
        self.transation_label.pack(side="top", fill="x", padx=10, pady=6)

        self.row_3 = ttk.Frame(self.tab)
        self.row_3.pack(side="top", expand=1, fill="both")

        self.joystick_resolution_options = {
            8: "8-bit",
            12: "12-bit",
            16: "16-bit",
        }

        for key, value in self.joystick_resolution_options.items():
            ttk.Radiobutton(
                self.row_1,
                text=value,
                variable=self.joystick_resolution,
                value=key
            ).pack(side="top", fill="x", padx=10)

        self.row_4 = ttk.Frame(self.tab)
        self.row_4.pack(side="top", expand=1, fill="both")

        self.joystick_select_label = ttk.Label(
            self.row_4,
            text="Joystick for mouse control:",
            font="TkDefaultFont 10 bold"
        )
        self.joystick_select_label.pack(side="top", fill="x", padx=10, pady=6)
        
        # X axis selection
        self.row_5 = ttk.Frame(self.tab)
        self.row_5.pack(side="top", expand=1, fill="both", pady=6)
        
        # X axis selection
        self.row_6 = ttk.Frame(self.tab)
        self.row_6.pack(side="top", expand=1, fill="both", pady=6)

        # Left mouse button selection
        self.row_11 = ttk.Frame(self.tab)
        self.row_11.pack(side="top", expand=1, fill="both", pady=6)

        # Right mouse button selection
        self.row_12 = ttk.Frame(self.tab)
        self.row_12.pack(side="top", expand=1, fill="both", pady=6)

        # Activation method selection
        self.row_9 = ttk.Frame(self.tab)
        self.row_9.pack(side="top", expand=1, fill="both", pady=6)

        self.activation_method_label = ttk.Label(
            self.row_9,
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
                self.row_9,
                text=value,
                variable=self.activation_method,
                value=key,
                command=self.update_button_selection
            ).pack(side="top", fill="x", padx=10)

        # Buttonbox selection
        self.row_7 = ttk.Frame(self.tab)
        self.row_7.pack(side="top", expand=1, fill="both", pady=6)

        self.joystick_select_label = ttk.Label(
            self.row_7,
            text="Button box for activation:",
            font="TkDefaultFont 10 bold"
        )
        self.joystick_select_label.pack(side="top", fill="x", padx=10, pady=6)

        # Activate button
        self.row_8 = ttk.Frame(self.tab)
        self.row_8.pack(side="top", expand=1, fill="both", pady=6)
        
        # Deactiavte button
        self.row_10 = ttk.Frame(self.tab)
        self.row_10.pack(side="top", expand=1, fill="both", pady=6)


    def update_device_list(self, joysticks):
        self.joysticks = joysticks
        self.update_joystick_selection()
        self.update_axis_selection()
        self.update_buttonbox_selection()


    def updater_autocenter(self):
        try:
            self.autocenter_list_label.destroy()
            self.autocenter_list.destroy()
        except:
            pass

        if self.autocenter.get():
            self.autocenter_list_label = ttk.Label(
                self.row_2,
                text="Key*:",
                width=5
            )
            self.autocenter_list_label.pack(side="left", padx=10)
            
            self.autocenter_list = ttk.Entry(
                self.row_2,
                textvariable=self.autocenter_key,
                width=10,
            )
            self.autocenter_list.pack(side="left", fill="x", padx=10)
            

    def update_joystick_selection(self):
        # Destroy combobox if it exists
        try:
            self.joystick_list.destroy()
        except:
            pass

        # Create new selection combobox
        joystick_list_values = ['None']
        for device in self.joysticks.values():
            joystick_list_values.append(device.get_name())

        self.joystick_list = ttk.Combobox(
            self.row_4,
            values=joystick_list_values,
            textvariable=self.joystick_selected,
            state="readonly",
        )
        self.joystick_list.bind('<<ComboboxSelected>>', self.update_axis_selection)    
        self.joystick_list.pack(side="top", fill="x", padx=10)


    def update_buttonbox_selection(self):
        # Destroy combobox if it exists
        try:
            self.buttonbox_list.destroy()
        except:
            pass

        # Create new selection combobox
        buttonbox_list_values = ['None']
        for device in self.joysticks.values():
            buttonbox_list_values.append(device.get_name())

        self.buttonbox_list = ttk.Combobox(
            self.row_7,
            values=buttonbox_list_values,
            textvariable=self.buttonbox_selected,
            state="readonly",
        )
        self.buttonbox_list.bind('<<ComboboxSelected>>', self.update_button_selection)    
        self.buttonbox_list.pack(side="top", fill="x", padx=10)


    def update_axis_selection(self,event=None):
        # Destroy axis selection if it exists and deselect axis amd invertion
        try:
            self.x_axis_label.destroy()
            self.x_axis_list.destroy()
            self.x_axis_inverted.destroy()
            self.joystick_x_selected.set("None")
            self.joystick_x_inverted.set(False)

            self.y_axis_label.destroy()
            self.y_axis_list.destroy()
            self.y_axis_inverted.destroy()
            self.joystick_y_selected.set("None")
            self.joystick_y_inverted.set(False)

            self.left_mouse_button_label.destroy()
            self.left_mouse_button_list.destroy()
            self.left_mouse_inverted.destroy()
            self.mouse_left_selected.set("None")
            self.mouse_left_inverted.set(False)
            
            self.right_mouse_button_label.destroy()
            self.right_mouse_button_list.destroy()
            self.right_mouse_inverted.destroy()
            self.mouse_right_selected.set("None")
            self.mouse_right_inverted.set(False)
        except:
            pass

        if self.joystick_selected.get() != "None":
            for device in self.joysticks.values():
                if device.get_name() == self.joystick_selected.get():
                    axis_list = [x+1 for x in range(device.get_numaxes())]
                    button_list = [x+1 for x in range(device.get_numbuttons())]

                    # X axis selection
                    self.x_axis_label = ttk.Label(
                        self.row_5,
                        text="X axis*:",
                        width=10
                    )
                    self.x_axis_label.pack(side="left", padx=10)

                    self.x_axis_list = ttk.Combobox(
                        self.row_5,
                        values=axis_list,
                        state="readonly",
                        textvariable=self.joystick_x_selected,
                        width=6
                    )  
                    self.x_axis_list.pack(side="left", padx=10)

                    self.x_axis_inverted = ttk.Checkbutton(
                        self.row_5,
                        text="Inverted",
                        variable=self.joystick_x_inverted,
                    )
                    self.x_axis_inverted.pack(side="left", padx=10)

                    
                    # Y axis selection
                    self.y_axis_label = ttk.Label(
                        self.row_6,
                        text="Y axis*:",
                        width=10
                    )
                    self.y_axis_label.pack(side="left", padx=10)

                    self.y_axis_list = ttk.Combobox(
                        self.row_6,
                        values=axis_list,
                        state="readonly",
                        textvariable=self.joystick_y_selected,
                        width=6
                    )
                    self.y_axis_list.pack(side="left", padx=10
                                          )
                    self.y_axis_inverted = ttk.Checkbutton(
                        self.row_6,
                        text="Inverted",
                        variable=self.joystick_y_inverted,
                    )
                    self.y_axis_inverted.pack(side="left", padx=10)


                    # Left mouse button selection
                    self.left_mouse_button_label = ttk.Label(
                        self.row_11,
                        text="Left:",
                        width=10
                    )
                    self.left_mouse_button_label.pack(side="left", padx=10)

                    self.left_mouse_button_list = ttk.Combobox(
                        self.row_11,
                        values=button_list,
                        state="readonly",
                        textvariable=self.mouse_left_selected,
                        width=6
                    )
                    self.left_mouse_button_list.pack(side="left", padx=10)

                    self.left_mouse_inverted = ttk.Checkbutton(
                        self.row_11,
                        text="Inverted",
                        variable=self.mouse_left_inverted,
                    )
                    self.left_mouse_inverted.pack(side="left", padx=10)


                    # Right mouse button selection
                    self.right_mouse_button_label = ttk.Label(
                        self.row_12,
                        text="Right:",
                        width=10
                    )
                    self.right_mouse_button_label.pack(side="left", padx=10)

                    self.right_mouse_button_list = ttk.Combobox(
                        self.row_12,
                        values=button_list,
                        state="readonly",
                        textvariable=self.mouse_right_selected,
                        width=6
                    )
                    self.right_mouse_button_list.pack(side="left", padx=10)

                    self.right_mouse_inverted = ttk.Checkbutton(
                        self.row_12,
                        text="Inverted",
                        variable=self.mouse_right_inverted,
                    )
                    self.right_mouse_inverted.pack(side="left", padx=10)


    def update_button_selection(self,event=None):
        # Destroy axis selection if it exists and deselect axis amd invertion
        try:
            self.activate_button_label.destroy()
            self.activate_button_list.destroy()
            self.activate_button_inverted.destroy()
            self.buttonbox_activate_selected.set("None")
            self.buttonbox_activate_inverted.set(False)

            self.deactivate_button_label.destroy()
            self.deactivate_button_list.destroy()
            self.deactivate_button_inverted.destroy()
            self.buttonbox_deactivate_selected.set("None")
            self.buttonbox_deactivate_inverted.set(False)
        except:
            pass

        if self.buttonbox_selected.get() != "None":
            for device in self.joysticks.values():
                if device.get_name() == self.buttonbox_selected.get():
                    button_list = [x+1 for x in range(device.get_numbuttons())]

                    # Activate button selection
                    self.activate_button_label = ttk.Label(
                        self.row_8,
                        text="Activate*:",
                        width=10
                    )
                    self.activate_button_label.pack(side="left", padx=10)

                    self.activate_button_list = ttk.Combobox(
                        self.row_8,
                        values=button_list,
                        state="readonly",
                        textvariable=self.buttonbox_activate_selected,
                        width=6
                    )  
                    self.activate_button_list.pack(side="left", padx=10)

                    self.activate_button_inverted = ttk.Checkbutton(
                        self.row_8,
                        text="Inverted",
                        variable=self.buttonbox_activate_inverted,
                    )
                    self.activate_button_inverted.pack(side="left", padx=10)

                    # Deactivate button selection
                    if self.activation_method.get() == 3:
                        self.deactivate_button_label = ttk.Label(
                            self.row_10,
                            text="Deactivate*: ",
                            width=10
                        )
                        self.deactivate_button_label.pack(side="left", padx=10)

                        self.deactivate_button_list = ttk.Combobox(
                            self.row_10,
                            values=button_list,
                            state="readonly",
                            textvariable=self.buttonbox_deactivate_selected,
                            width=6
                        )
                        self.deactivate_button_list.pack(side="left", padx=10)

                        self.deactivate_button_inverted = ttk.Checkbutton(
                            self.row_10,
                            text="Inverted",
                            variable=self.buttonbox_deactivate_inverted,
                        )
                        self.deactivate_button_inverted.pack(side="left", padx=10)


    def get_translation_method(self):
        return self.translation_method.get()
    

    def set_translation_method(self, value):
        self.translation_method.set(value)


    def get_autocenter(self):
        return self.autocenter.get()
    

    def get_autocenter_key(self):
        if self.autocenter_key.get() == "":
            return None
        else:
            return self.autocenter_key.get()


    def get_joystick_resolution(self):
        return self.joystick_resolution.get()


    def set_joystick_resolution(self, value):
        self.joystick_resolution.set(value)


    def get_joystick_selected(self):
        selected_name = self.joystick_selected.get()
        if selected_name != "None":
            for device in self.joysticks.values():
                if device.get_name() == selected_name:
                    return device.get_guid()
        else:
            return None
        

    def set_joystick_selected(self, guid):
        if guid != None:
            for device in self.joysticks.values():
                if device.get_guid() == guid:
                    value = device.get_name()
                    self.joystick_selected.set(value)
                    self.update_axis_selection()
                    return True
        
            return False
        

    def get_joystick_x_axis(self):
        selected_x_axise = self.joystick_x_selected.get()
        if selected_x_axise != "None":
            return int(selected_x_axise) - 1
        else:
            return None
    

    def set_joystick_x_axis(self, value):
        if value != "None":
            self.joystick_x_selected.set(int(value)+1)
        else:
            self.joystick_x_selected.set("None")

    
    def get_joystick_y_axis(self):
        selected_y_axise = self.joystick_y_selected.get()
        if selected_y_axise != "None":
            return int(selected_y_axise) - 1
        else:
            return None


    def set_joystick_y_axis(self, value):
        if value != "None":
            self.joystick_y_selected.set(int(value)+1)
        else:
            self.joystick_y_selected.set("None")


    def get_joystick_x_inverted(self):
        return self.joystick_x_inverted.get()


    def set_joystick_x_inverted(self,value):
        return self.joystick_x_inverted.set(value)
    

    def get_joystick_y_inverted(self):
        return self.joystick_y_inverted.get()


    def set_joystick_y_inverted(self,value):
        return self.joystick_y_inverted.set(value)


    def get_activation_method(self):
        return self.activation_method.get()


    def get_buttonbox_selected(self):
        selected_name = self.buttonbox_selected.get()
        if selected_name != "None":
            for device in self.joysticks.values():
                if device.get_name() == selected_name:
                    return device.get_guid()
        else:
            return None


    def get_activation_button(self):
        selected_button = self.buttonbox_activate_selected.get()
        if selected_button != "None":
            return int(selected_button) - 1
        else:
            return None
        
        
    def get_activation_button_inverted(self):
        return self.buttonbox_activate_inverted.get()
    

    def get_deactivation_button(self):
        selected_button = self.buttonbox_deactivate_selected.get()
        if selected_button != "None":
            return int(selected_button) - 1
        else:
            return None
    

    def get_deactivation_button_inverted(self):
        return self.buttonbox_deactivate_inverted.get()


    def get_mouse_left(self):
        selected_button = self.mouse_left_selected.get()
        if selected_button != "None":
            return int(selected_button) - 1
        else:
            return None
        
        
    def set_mouse_left(self, value):
        if value != "None":
            self.mouse_left_selected.set(int(value)+1)
        else:
            self.mouse_left_selected.set("None")
    

    def get_mouse_left_inverted(self):
        return self.mouse_left_inverted.get()
    

    def get_mouse_right(self):
        selected_button = self.mouse_right_selected.get()
        if selected_button != "None":
            return int(selected_button) - 1
        else:
            return None
    

    def get_mouse_right_inverted(self):
        return self.mouse_right_inverted.get()