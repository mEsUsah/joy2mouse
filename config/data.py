import configparser


def get_current_config():
    current_config = configparser.ConfigParser()
    current_config['JOYSTICK'] = {
        'translation_method': str(configModel['translation_method']),
        'joystick_resolution': str(configModel['joystick_resolution']),
        'selected_joystick': str(configModel['selected_joystick']),
        'selected_x_axis': str(configModel['joystick_x_axis']),
        'selected_y_axis': str(configModel['joystick_y_axis']),
        'joystick_x_inverted': str(configModel['joystick_x_inverted']),
        'joystick_y_inverted': str(configModel['joystick_y_inverted']),
        'mouse_left_button': str(configModel['mouse_left']),
        'mouse_right_button': str(configModel['mouse_right']),
        'mouse_left_inverted': str(configModel['mouse_left_inverted']),
        'mouse_right_inverted': str(configModel['mouse_right_inverted']),
        'autocenter': str(configModel['autocenter']),
        'autocenter_key': str(configModel['autocenter_key']),
        'deadzone': str(configModel['deadzone']),
    }
    current_config['BUTTONBOX'] = {
        'selected_activation_method': str(configModel['activation_method']),
        'selected_buttonbox': str(configModel['selected_buttonbox']),
        'activation_button': str(configModel['activation_button']),
        'activation_button_inverted': str(configModel['activation_button_inverted']),
        'deactivation_button': str(configModel['deactivation_button']),
        'deactivation_button_inverted': str(configModel['deactivation_button_inverted']),
    }
    return current_config


def joystick_config_ready():
    if (not configModel['selected_joystick'] == None or \
        not configModel['selected_buttonbox'] == None and \
        not configModel['activation_button'] == None) and \
        (not configModel['joystick_x_axis'] == None or not configModel['joystick_y_axis'] == None):
            return True
    else:
        return False

configModel = {
    'screen_x_center': 0,
    'screen_y_center': 0,
    'current_config_file': 'default.ini',
    'current_config_default': True,
    'armed': False,
    'active': False,
    'activated': False,
    'debugging': False,
    'activate_button_pressed': False,
    'deactivate_button_pressed': False,
    'mouse_x': 0,
    'mouse_y': 0,
    'last_mouse_x': 0,
    'last_mouse_y': 0,
    'max_refresh_rate': 165,
    'joystick_resolution': 0,

    # Joystick
    'translation_method': 1,
    'joystick_resolution': 16,
    'selected_joystick': None,
    'selected_joystick_uuid': None,

    'joystick_x_axis': None,
    'joystick_y_axis': None,
    'joystick_x_inverted': False,
    'joystick_y_inverted': False,

    'mouse_left': None,
    'mouse_right': None,
    'mouse_left_inverted': False,
    'mouse_right_inverted': False,
            
    'deadzone': 10,
    'autocenter': False,
    'autocenter_key': None,

    # Buttonbox
    'activation_method': 1,
    'selected_buttonbox': None,
    'selected_buttonbox_uuid': None,
    'activation_button': None,
    'deactivation_button': None,
    'activation_button_inverted': False,
    'deactivation_button_inverted': False,
}

joysticks = {}