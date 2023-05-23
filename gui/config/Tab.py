import tkinter as tk
import tkinter.ttk as ttk
import gui
import config

class Tab():
    def __init__(self, tab):
        '''Config tab in app window'''
        self.tab = tab
        self.showing_center_option = False
        self.joysticks = {}
        self.configModel = {
            'translation_method': tk.IntVar(value=1),
            'joystick_resolution': tk.IntVar(value=16),
            'autocenter': tk.BooleanVar(value=False),
            'autocenter_key': tk.StringVar(value="c"),
            'joystick_selected': tk.StringVar(value="None"),
            'joystick_x_axis': tk.StringVar(value="None"),
            'joystick_x_inverted': tk.BooleanVar(value=False),
            'joystick_y_axis': tk.StringVar(value="None"),
            'joystick_y_inverted': tk.BooleanVar(value=False),
            'mouse_left': tk.StringVar(value="None"),
            'mouse_left_inverted': tk.BooleanVar(value=False),
            'mouse_right': tk.StringVar(value="None"),
            'mouse_right_inverted': tk.BooleanVar(value=False),

            'activation_method': tk.IntVar(value=1),
            'buttonbox_selected': tk.StringVar(value="None"),
            'activation_button': tk.StringVar(value="None"),
            'activation_button_inverted': tk.BooleanVar(value=False),
            'deactivation_button': tk.StringVar(value="None"),
            'deactivation_button_inverted': tk.BooleanVar(value=False),
        }
        

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
                variable=self.configModel['translation_method'],
                value=key,
                command=self.update_config
            ).pack(side="top", fill="x", padx=10)
        
        self.row_2 = ttk.Frame(self.tab)
        self.row_2.pack(side="top", expand=1, fill="both")

        # Autocenter option
        self.center_option = ttk.Checkbutton(
            self.row_2,
            text="Autocenter:",
            variable=self.configModel['autocenter'],
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
                variable=self.configModel['joystick_resolution'],
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
                variable=self.configModel['activation_method'],
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

    def update_config(self):   
        for key, value in self.configModel.items():
            config.data.configModel[key] = value.get()

        config.data.configModel['selected_joystick_uuid'] = self.get_joystick_selected()
        config.data.configModel['selected_buttonbox_uuid'] = self.get_buttonbox_selected()


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

        if self.configModel['autocenter'].get():
            self.autocenter_list_label = ttk.Label(
                self.row_2,
                text="Key*:",
                width=5
            )
            self.autocenter_list_label.pack(side="left", padx=10)
            
            self.autocenter_list = ttk.Entry(
                self.row_2,
                textvariable=self.configModel['autocenter_key'],
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
            textvariable=self.configModel['joystick_selected'],
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
            textvariable=self.configModel['buttonbox_selected'],
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
        except:
            pass

        if self.configModel['joystick_selected'].get() != "None":
            for device in self.joysticks.values():
                if device.get_name() == self.configModel['joystick_selected'].get():
                    axis_list = ["None"]
                    axis_list.extend([x+1 for x in range(device.get_numaxes())])
                    button_list = ["None"]
                    button_list.extend([x+1 for x in range(device.get_numbuttons())])

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
                        textvariable=self.configModel['joystick_x_axis'],
                        width=6
                    )  
                    self.x_axis_list.pack(side="left", padx=10)

                    self.x_axis_inverted = ttk.Checkbutton(
                        self.row_5,
                        text="Inverted",
                        variable=self.configModel['joystick_x_inverted'],
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
                        textvariable=self.configModel['joystick_y_axis'],
                        width=6
                    )
                    self.y_axis_list.pack(side="left", padx=10
                                          )
                    self.y_axis_inverted = ttk.Checkbutton(
                        self.row_6,
                        text="Inverted",
                        variable=self.configModel['joystick_y_inverted'],
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
                        textvariable=self.configModel['mouse_left'],
                        width=6
                    )
                    self.left_mouse_button_list.pack(side="left", padx=10)

                    self.left_mouse_inverted = ttk.Checkbutton(
                        self.row_11,
                        text="Inverted",
                        variable=self.configModel['mouse_left_inverted'],
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
                        textvariable=self.configModel['mouse_right'],
                        width=6
                    )
                    self.right_mouse_button_list.pack(side="left", padx=10)

                    self.right_mouse_inverted = ttk.Checkbutton(
                        self.row_12,
                        text="Inverted",
                        variable=self.configModel['mouse_right_inverted'],
                    )
                    self.right_mouse_inverted.pack(side="left", padx=10)


    def update_button_selection(self,event=None):
        # Destroy axis selection if it exists and deselect axis amd invertion
        try:
            self.activate_button_label.destroy()
            self.activate_button_list.destroy()
            self.activate_button_inverted.destroy()
            self.configModel['activation_button'].set("None")
            self.configModel['activation_button_inverted'].set(False)

            self.deactivate_button_label.destroy()
            self.deactivate_button_list.destroy()
            self.deactivate_button_inverted.destroy()
            self.configModel['deactivation_button'].set("None")
            self.configModel['deactivation_button_inverted'].set(False)
        except:
            pass

        if self.configModel['buttonbox_selected'].get() != "None":
            for device in self.joysticks.values():
                if device.get_name() == self.configModel['buttonbox_selected'].get():
                    button_list = ["None"]
                    button_list.extend([x+1 for x in range(device.get_numbuttons())])

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
                        textvariable=self.configModel['activation_button'],
                        width=6
                    )  
                    self.activate_button_list.pack(side="left", padx=10)

                    self.activate_button_inverted = ttk.Checkbutton(
                        self.row_8,
                        text="Inverted",
                        variable=self.configModel['activation_button_inverted'],
                    )
                    self.activate_button_inverted.pack(side="left", padx=10)

                    # Deactivate button selection
                    if self.configModel['activation_method'].get() == 3:
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
                            textvariable=self.configModel['deactivation_button'],
                            width=6
                        )
                        self.deactivate_button_list.pack(side="left", padx=10)

                        self.deactivate_button_inverted = ttk.Checkbutton(
                            self.row_10,
                            text="Inverted",
                            variable=self.configModel['deactivation_button_inverted'],
                        )
                        self.deactivate_button_inverted.pack(side="left", padx=10)


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


    def get_joystick_selected(self):
        selected_name = self.configModel['joystick_selected'].get()
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
                    self.configModel['joystick_selected'].set(value)
                    self.update_axis_selection()
                    return True
        
            return False
        

    def get_joystick_x_axis(self):
        selected_x_axise = self.configModel['joystick_x_axis'].get()
        if selected_x_axise != "None":
            return int(selected_x_axise) - 1
        else:
            return None
    

    def set_joystick_x_axis(self, value):
        if value != "None":
            self.configModel['joystick_x_axis'].set(int(value)+1)
        else:
            self.configModel['joystick_x_axis'].set("None")

    
    def get_joystick_y_axis(self):
        selected_y_axise = self.configModel['joystick_y_axis'].get()
        if selected_y_axise != "None":
            return int(selected_y_axise) - 1
        else:
            return None


    def set_joystick_y_axis(self, value):
        if value != "None":
            self.configModel['joystick_y_axis'].set(int(value)+1)
        else:
            self.configModel['joystick_y_axis'].set("None")


    def get_joystick_x_inverted(self):
        return self.configModel['joystick_x_inverted'].get()


    def set_joystick_x_inverted(self,value):
        return self.configModel['joystick_x_inverted'].set(value)
    

    def get_joystick_y_inverted(self):
        return self.configModel['joystick_y_inverted'].get()


    def set_joystick_y_inverted(self,value):
        return self.configModel['joystick_y_inverted'].set(value)


    def get_activation_method(self):
        return self.configModel['activation_method'].get()


    def set_activation_method(self, value):
        self.configModel['activation_method'].set(value)
        self.update_button_selection()


    def get_buttonbox_selected(self):
        selected_name = self.configModel['buttonbox_selected'].get()
        if selected_name != "None":
            for device in self.joysticks.values():
                if device.get_name() == selected_name:
                    return device.get_guid()
        else:
            return None

        
    def set_buttonbox_selected(self, guid):
        if guid != None:
            for device in self.joysticks.values():
                if device.get_guid() == guid:
                    value = device.get_name()
                    self.configModel['buttonbox_selected'].set(value)
                    self.update_button_selection()
                    return True
        
            return False


    def get_activation_button(self):
        selected_button = self.configModel['activation_button'].get()
        if selected_button != "None":
            return int(selected_button) - 1
        else:
            return None
        

    def set_activation_button(self, value):
        if value != "None":
            self.configModel['activation_button'].set(int(value)+1)
        else:
            self.configModel['activation_button'].set("None")

        
    def get_activation_button_inverted(self):
        return self.configModel['activation_button_inverted'].get()


    def set_activation_button_inverted(self,value):
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


    def set_deactivation_button_inverted(self,value):
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