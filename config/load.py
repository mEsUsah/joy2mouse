import config
import utils
import configparser
import os


def load_config_file():
    file_path = utils.files.gui_open_path()
    if not file_path:
        return  # User canceled the open dialog
    config.data.configModel['current_config_default'] = False
    config.data.configModel['current_config_file'] = file_path

    load_config()


def _get_int_or_none(cfg, section, option, fallback='None'):
    val = cfg.get(section, option, fallback=fallback)
    return None if val == 'None' else int(val)


def load_config():
    model = config.data.configModel

    if model['current_config_default']:
        model['current_config_file'] = os.path.join(os.getcwd(), 'default.ini')

    cfg = configparser.ConfigParser()
    cfg.read(model['current_config_file'])

    # Joystick
    model['translation_method'] = cfg.getint('JOYSTICK', 'translation_method', fallback=1)
    model['joystick_resolution'] = cfg.getint('JOYSTICK', 'joystick_resolution', fallback=500)
    model['joystick_selected'] = cfg.get('JOYSTICK', 'selected_joystick', fallback='None')

    model['joystick_x_axis'] = cfg.get('JOYSTICK', 'selected_x_axis', fallback='None')
    model['joystick_y_axis'] = cfg.get('JOYSTICK', 'selected_y_axis', fallback='None')
    model['joystick_x_inverted'] = cfg.getboolean('JOYSTICK', 'joystick_x_inverted', fallback=False)
    model['joystick_y_inverted'] = cfg.getboolean('JOYSTICK', 'joystick_y_inverted', fallback=False)

    model['mouse_left_button'] = _get_int_or_none(cfg, 'JOYSTICK', 'mouse_left_button')
    model['mouse_right_button'] = _get_int_or_none(cfg, 'JOYSTICK', 'mouse_right_button')
    model['mouse_middle_button'] = _get_int_or_none(cfg, 'JOYSTICK', 'mouse_middle_button')
    model['mouse_left_inverted'] = cfg.getboolean('JOYSTICK', 'mouse_left_inverted', fallback=False)
    model['mouse_right_inverted'] = cfg.getboolean('JOYSTICK', 'mouse_right_inverted', fallback=False)
    model['mouse_middle_inverted'] = cfg.getboolean('JOYSTICK', 'mouse_middle_inverted', fallback=False)

    model['autocenter'] = cfg.getboolean('JOYSTICK', 'autocenter', fallback=False)
    model['autocenter_key'] = cfg.get('JOYSTICK', 'autocenter_key', fallback='None')
    model['deadzone'] = cfg.getint('JOYSTICK', 'deadzone', fallback=10)

    # Buttonbox
    model['activation_method'] = cfg.getint('BUTTONBOX', 'selected_activation_method', fallback=1)
    model['buttonbox_selected'] = cfg.get('BUTTONBOX', 'selected_buttonbox', fallback='None')
    model['activation_button'] = _get_int_or_none(cfg, 'BUTTONBOX', 'activation_button')
    model['deactivation_button'] = _get_int_or_none(cfg, 'BUTTONBOX', 'deactivation_button')
    model['activation_button_inverted'] = cfg.getboolean('BUTTONBOX', 'activation_button_inverted', fallback=False)
    model['deactivation_button_inverted'] = cfg.getboolean('BUTTONBOX', 'deactivation_button_inverted', fallback=False)
