import config
import utils
import configparser
import os
import tkinter as tk


def load_config_file():
    config.data.current_config_default = False

    file_path = utils.files.gui_open_path()
    if not file_path:
        return # User canceled the open dialog
    config.data.current_config_file = file_path

    load_config()


def load_config():
    if config.data.current_config_default:
        config.data.current_config_file = os.path.join(os.getcwd(), 'default.ini')
    
    config.data.current_config = configparser.ConfigParser()
    config.data.current_config.read(config.data.current_config_file)

    # try:
    # Joystick
    config.data.translation_method = config.data.current_config.getint('JOYSTICK', 'translation_method')
    config.data.joystick_resolution = config.data.current_config.getint('JOYSTICK', 'joystick_resolution')
    config.data.joystick_selected = config.data.current_config.get('JOYSTICK', 'selected_joystick')

    config.data.joystick_x_axis = config.data.current_config.get('JOYSTICK', 'selected_x_axis')
    config.data.joystick_y_axis = config.data.current_config.get('JOYSTICK', 'selected_y_axis')
    config.data.joystick_x_inverted = config.data.current_config.getboolean('JOYSTICK', 'joystick_x_inverted')
    config.data.joystick_y_inverted = config.data.current_config.getboolean('JOYSTICK', 'joystick_y_inverted')

    config.data.mouse_left = config.data.current_config.get('JOYSTICK', 'mouse_left_button')
    config.data.mouse_right = config.data.current_config.get('JOYSTICK', 'mouse_right_button')
    config.data.mouse_left_inverted = config.data.current_config.getboolean('JOYSTICK', 'mouse_left_inverted')
    config.data.mouse_right_inverted = config.data.current_config.getboolean('JOYSTICK', 'mouse_right_inverted')
    
    config.data.autocenter = config.data.current_config.getboolean('JOYSTICK', 'autocenter')
    config.data.autocenter_key = config.data.current_config.get('JOYSTICK', 'autocenter_key')
    config.data.deadzone = config.data.current_config.getint('JOYSTICK', 'deadzone')


    # Buttonbox
    config.data.activation_method = config.data.current_config.getint('BUTTONBOX', 'selected_activation_method')
    config.data.buttonbox_selected = config.data.current_config.get('BUTTONBOX', 'selected_buttonbox')
    config.data.activation_button = config.data.current_config.get('BUTTONBOX', 'activation_button')
    config.data.deactivation_button = config.data.current_config.get('BUTTONBOX', 'deactivation_button')
    config.data.activation_button_inverted = config.data.current_config.getboolean('BUTTONBOX', 'activation_button_inverted')
    config.data.deactivation_button_inverted = config.data.current_config.getboolean('BUTTONBOX', 'deactivation_button_inverted')

    # Config filename
    # window.title(os.path.basename(config.data.current_config_file) + " - " + utils.releases.APP_NAME)
    # except:
    #     tk.messagebox.showerror("Open error", "Broken config file")


