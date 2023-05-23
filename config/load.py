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
    if config.data.configModel['current_config_default']:
        config.data.configModel['current_config_file'] = os.path.join(os.getcwd(), 'default.ini')
    
    config.data.configModel['current_config'] = configparser.ConfigParser()
    config.data.configModel['current_config'].read(config.data.configModel['current_config_file'])

    # try:
    # Joystick
    config.data.configModel['translation_method'] = config.data.configModel['current_config'].getint('JOYSTICK', 'translation_method')
    config.data.configModel['joystick_resolution'] = config.data.configModel['current_config'].getint('JOYSTICK', 'joystick_resolution')
    config.data.configModel['joystick_selected'] = config.data.configModel['current_config'].get('JOYSTICK', 'selected_joystick')

    config.data.configModel['joystick_x_axis'] = config.data.configModel['current_config'].get('JOYSTICK', 'selected_x_axis')
    config.data.configModel['joystick_y_axis'] = config.data.configModel['current_config'].get('JOYSTICK', 'selected_y_axis')
    config.data.configModel['joystick_x_inverted'] = config.data.configModel['current_config'].getboolean('JOYSTICK', 'joystick_x_inverted')
    config.data.configModel['joystick_y_inverted'] = config.data.configModel['current_config'].getboolean('JOYSTICK', 'joystick_y_inverted')

    config.data.configModel['mouse_left'] = config.data.configModel['current_config'].get('JOYSTICK', 'mouse_left_button')
    config.data.configModel['mouse_right'] = config.data.configModel['current_config'].get('JOYSTICK', 'mouse_right_button')
    config.data.configModel['mouse_left_inverted'] = config.data.configModel['current_config'].getboolean('JOYSTICK', 'mouse_left_inverted')
    config.data.configModel['mouse_right_inverted'] = config.data.configModel['current_config'].getboolean('JOYSTICK', 'mouse_right_inverted')
    
    config.data.configModel['autocenter'] = config.data.configModel['current_config'].getboolean('JOYSTICK', 'autocenter')
    config.data.configModel['autocenter_key'] = config.data.configModel['current_config'].get('JOYSTICK', 'autocenter_key')
    config.data.configModel['deadzone'] = config.data.configModel['current_config'].getint('JOYSTICK', 'deadzone')


    # Buttonbox
    config.data.configModel['activation_method'] = config.data.configModel['current_config'].getint('BUTTONBOX', 'selected_activation_method')
    config.data.configModel['buttonbox_selected'] = config.data.configModel['current_config'].get('BUTTONBOX', 'selected_buttonbox')
    config.data.configModel['activation_button'] = config.data.configModel['current_config'].get('BUTTONBOX', 'activation_button')
    config.data.configModel['deactivation_button'] = config.data.configModel['current_config'].get('BUTTONBOX', 'deactivation_button')
    config.data.configModel['activation_button_inverted'] = config.data.configModel['current_config'].getboolean('BUTTONBOX', 'activation_button_inverted')
    config.data.configModel['deactivation_button_inverted'] = config.data.configModel['current_config'].getboolean('BUTTONBOX', 'deactivation_button_inverted')

    # Config filename
    # window.title(os.path.basename(config.data.current_config_file) + " - " + utils.releases.APP_NAME)
    # except:
    #     tk.messagebox.showerror("Open error", "Broken config file")


