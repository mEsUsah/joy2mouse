import configparser


def get_current_config():
    current_config = configparser.ConfigParser()
    current_config['JOYSTICK'] = {
        'translation_method': str(translation_method),
        'joystick_resolution': str(joystick_resolution),
        'selected_joystick': str(joystick_selected),
        'selected_x_axis': str(joystick_x_axis),
        'selected_y_axis': str(joystick_y_axis),
        'joystick_x_inverted': str(joystick_x_inverted),
        'joystick_y_inverted': str(joystick_y_inverted),
        'mouse_left_button': str(mouse_left),
        'mouse_right_button': str(mouse_right),
        'mouse_left_inverted': str(mouse_left_inverted),
        'mouse_right_inverted': str(mouse_right_inverted),
        'autocenter': str(autocenter),
        'autocenter_key': str(autocenter_key),
        'deadzone': str(deadzone),
    }
    current_config['BUTTONBOX'] = {
        'selected_activation_method': str(activation_method),
        'selected_buttonbox': str(buttonbox_selected),
        'activation_button': str(activation_button),
        'activation_button_inverted': str(activation_button_inverted),
        'deactivation_button': str(deactivation_button),
        'deactivation_button_inverted': str(deactivation_button_inverted),
    }
    return current_config


def joystick_config_ready():
    if (not joystick_selected == None or \
        not buttonbox_selected == None and \
        not activation_button == None) and \
        (not joystick_x_axis == None or not joystick_y_axis == None):
            return True
    else:
        return False


current_config_file = 'default.ini'
current_config_default = True
deadzone = 10

# Joystick
translation_method = 1
joystick_resolution = 16
joystick_selected = None

joystick_x_axis = None
joystick_y_axis = None
joystick_x_inverted = False
joystick_y_inverted = False

mouse_left = None
mouse_right = None
mouse_left_inverted = False
mouse_right_inverted = False
        
autocenter = False
autocenter_key = None

# Buttonbox
activation_method = 1
buttonbox_selected = None
activation_button = None
deactivation_button = None
activation_button_inverted = False
deactivation_button_inverted = False
