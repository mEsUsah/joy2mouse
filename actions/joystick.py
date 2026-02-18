import keyboard
import pydirectinput
import config

pydirectinput.FAILSAFE = False # allow mouse to go outside of screen
configModel = config.data.configModel
mouse_x = configModel['mouse_x']
mouse_y = configModel['mouse_y']
screen_x_center = configModel['screen_x_center']
screen_y_center = configModel['screen_y_center']
joystick_resolution = configModel['joystick_resolution']
debugging = configModel['debugging']

_left_held = False
_right_held = False
_middle_held = False


def release_mouse_buttons():
    global _left_held, _right_held, _middle_held
    if _left_held:
        pydirectinput.mouseUp(button="left")
        _left_held = False
    if _right_held:
        pydirectinput.mouseUp(button="right")
        _right_held = False
    if _middle_held:
        pydirectinput.mouseUp(button="middle")
        _middle_held = False


def run():
    # Loop over all joysticks
    last_mouse_x = configModel.get('last_mouse_x', 0)
    last_mouse_y = configModel.get('last_mouse_y', 0)
    for joy in config.data.joysticks.values():
        # Handle joystick input
        if configModel['selected_joystick'] and (configModel['joystick_x_axis'] != None or configModel['joystick_y_axis'] != None):
            if joy.get_guid() == configModel['selected_joystick_uuid']:
                if configModel['active']:

                    # Handle one axis set to None
                    try:
                        x_axis_index = int(configModel['joystick_x_axis']) if configModel['joystick_x_axis'] is not None and configModel['joystick_x_axis'] != "None" else None
                    except ValueError:
                        x_axis_index = None
                    if x_axis_index is None:
                        joystick_x_axis = 0
                    else:
                        joystick_x_axis = joy.get_axis(x_axis_index)

                    try:
                        y_axis_index = int(configModel['joystick_y_axis']) if configModel['joystick_y_axis'] is not None and configModel['joystick_y_axis'] != "None" else None
                    except ValueError:
                        y_axis_index = None
                    if y_axis_index is None:
                        joystick_y_axis = 0
                    else:
                        joystick_y_axis = joy.get_axis(y_axis_index)

                    # set mouse position
                    if configModel['translation_method'] == 1: # default
                        x_axis_value = int(joystick_x_axis * 5000)
                        y_axis_value = int(joystick_y_axis * 5000)
                        
                        x_axis_value, y_axis_value = handle_inverted_axis(
                            [x_axis_value, y_axis_value], 
                            (configModel['joystick_x_inverted'], configModel['joystick_y_inverted'])
                        )

                        mouse_x_pos = mouse_x + x_axis_value
                        mouse_y_pos = mouse_y + y_axis_value
                        pydirectinput.moveTo(mouse_x_pos, mouse_y_pos, _pause=False)

                    elif configModel['translation_method'] == 2: # absolute mouse movement
                        x_axis_value = int(joystick_x_axis * screen_x_center)
                        y_axis_value = int(joystick_y_axis * screen_y_center)

                        x_axis_value, y_axis_value = handle_inverted_axis(
                            [x_axis_value, y_axis_value], 
                            (configModel['joystick_x_inverted'], configModel['joystick_y_inverted'])
                        )

                        mouse_x_pos = screen_x_center + x_axis_value
                        mouse_y_pos = screen_y_center + y_axis_value
                        pydirectinput.moveTo(mouse_x_pos, mouse_y_pos, _pause=False)

                    elif configModel['translation_method'] == 3: # relavitve mouse movement
                        x_axis_value = int(joystick_x_axis * joystick_resolution)
                        y_axis_value = int(joystick_y_axis * joystick_resolution)
                        mouse_Dx = x_axis_value - last_mouse_x
                        mouse_Dy = y_axis_value - last_mouse_y

                        mouse_Dx, mouse_Dy = handle_inverted_axis(
                            [mouse_Dx, mouse_Dy], 
                            (configModel['joystick_x_inverted'], configModel['joystick_y_inverted'])
                        )

                        last_mouse_x = x_axis_value
                        last_mouse_y = y_axis_value
                        pydirectinput.moveRel(mouse_Dx,mouse_Dy, _pause=False, relative=True)

                        # center torso if joystick is in deadzone
                        if configModel['autocenter'] and configModel['autocenter_key'] != None:
                            within_deadzone_x = x_axis_value > -configModel['deadzone'] and x_axis_value < configModel['deadzone']
                            within_deadzone_y = y_axis_value > -configModel['deadzone'] and y_axis_value < configModel['deadzone']

                            if within_deadzone_x and within_deadzone_y:
                                keyboard.press_and_release(configModel['autocenter_key'])

                        if debugging:
                            if configModel['translation_method'] == 3:
                                print(f"Mouse: \tdX: {mouse_Dx} \tdY: {mouse_Dy} \tres: {joystick_resolution}")
                            else:
                                print(f"Mouse: \tX: {x_axis_value} \tY: {y_axis_value}")

                    # Mouse buttons — hold while joystick button held, release on release
                    global _left_held, _right_held, _middle_held
                    if configModel['mouse_left_button'] != None:
                        pressed = joy.get_button(configModel['mouse_left_button'])
                        if pressed and not _left_held:
                            pydirectinput.mouseDown(button="left")
                            _left_held = True
                        elif not pressed and _left_held:
                            pydirectinput.mouseUp(button="left")
                            _left_held = False
                    if configModel['mouse_right_button'] != None:
                        pressed = joy.get_button(configModel['mouse_right_button'])
                        if pressed and not _right_held:
                            pydirectinput.mouseDown(button="right")
                            _right_held = True
                        elif not pressed and _right_held:
                            pydirectinput.mouseUp(button="right")
                            _right_held = False
                    if configModel['mouse_middle_button'] != None:
                        pressed = joy.get_button(configModel['mouse_middle_button'])
                        if pressed and not _middle_held:
                            pydirectinput.mouseDown(button="middle")
                            _middle_held = True
                        elif not pressed and _middle_held:
                            pydirectinput.mouseUp(button="middle")
                            _middle_held = False

    # Persist last_mouse_x and last_mouse_y
    configModel['last_mouse_x'] = last_mouse_x
    configModel['last_mouse_y'] = last_mouse_y


def handle_inverted_axis(axis, inverted):
    for i in range(len(axis)):
        if inverted[i]:
            axis[i] *= -1
    return axis