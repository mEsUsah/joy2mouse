#! /bin/env python3

import keyboard
import pydirectinput
import configparser
import mouse
import pygame
import time
import tkinter as tk
from tkinter import ttk
from screeninfo import get_monitors
import gui
import utils
import os

def stop_app():
    global app_running
    app_running = False

def joystick_config_ready():
    global selected_joystick
    global selected_x_axis
    global selected_y_axis
    global selected_buttonbox
    global activation_button
    global autocenter
    global autocenter_key
    
    if selected_joystick == None or \
        selected_x_axis == None or \
        selected_y_axis == None or \
        selected_buttonbox == None or \
        activation_button == None:
            return False
    else:
        return True
    

def handle_inverted_axis(axis, inverted):
    for i in range(len(axis)):
        if inverted[i]:
            axis[i] *= -1
    return axis


def save_config():
    global current_config_file

    if current_config_file == 'default.ini':
        file_path = utils.files.gui_save_as_path()
        if not file_path:
            return # User canceled the save dialog
        current_config_file = file_path

    current_config = get_current_config()
    with open(current_config_file, 'w') as configfile:
        current_config.write(configfile)


def save_config_as():
    global current_config_file

    file_path = utils.files.gui_save_as_path()
    if not file_path:
        return # User canceled the save dialog
    current_config_file = file_path

    current_config = get_current_config()
    with open(current_config_file, 'w') as configfile:
        current_config.write(configfile)


def get_current_config():
    current_config = configparser.ConfigParser()
    current_config['JOYSTICK'] = {
        'translation_method': str(config.get_translation_method()),
        'selected_joystick': str(config.get_joystick_selected()),
        'joystick_resolution': str(config.get_joystick_resolution()),
        'selected_x_axis': str(config.get_joystick_x_axis()),
        'joystick_x_inverted': str(config.get_joystick_x_inverted()),
        'selected_y_axis': str(config.get_joystick_y_axis()),
        'joystick_y_inverted': str(config.get_joystick_y_inverted()),
        'mouse_left_button': str(config.get_mouse_left()),
        'mouse_left_inverted': str(config.get_mouse_left_inverted()),
        'mouse_right_button': str(config.get_mouse_right()),
        'mouse_right_inverted': str(config.get_mouse_right_inverted()),
        'autocenter': str(config.get_autocenter()),
        'autocenter_key': str(config.get_autocenter_key()),
        'deadzone': str(deadzone),
    }
    current_config['BUTTONBOX'] = {
        'selected_activation_method': str(config.get_activation_method()),
        'selected_buttonbox': str(config.get_buttonbox_selected()),
        'activation_button': str(config.get_activation_button()),
        'activation_button_inverted': str(config.get_activation_button_inverted()),
        'deactivation_button': str(config.get_deactivation_button()),
        'deactivation_button_inverted': str(config.get_deactivation_button_inverted()),
    }
    return current_config


def load_config():
    global current_config_file
    global current_config_default
    if current_config_default:
        current_config_file = os.path.join(os.getcwd(), 'default.ini')
    
    current_config = configparser.ConfigParser()
    current_config.read(current_config_file)

    try:
        config.set_translation_method(current_config.getint('JOYSTICK', 'translation_method'))
        config.set_joystick_resolution(current_config.getint('JOYSTICK', 'joystick_resolution'))
        config.set_joystick_selected(current_config.get('JOYSTICK', 'selected_joystick'))
        config.set_joystick_x_axis(current_config.get('JOYSTICK', 'selected_x_axis'))
        config.set_joystick_x_inverted(current_config.getboolean('JOYSTICK', 'joystick_x_inverted'))
        config.set_joystick_y_axis(current_config.get('JOYSTICK', 'selected_y_axis'))
        config.set_joystick_y_inverted(current_config.getboolean('JOYSTICK', 'joystick_y_inverted'))
        config.set_mouse_left(current_config.get('JOYSTICK', 'mouse_left_button'))
        config.set_mouse_right(current_config.get('JOYSTICK', 'mouse_right_button'))
    except:
        tk.messagebox.showerror("Open error", "Broken config file")

# Get game screen size
screen_x = None
screen_y = None
for m in get_monitors():
    if m.is_primary:
        screen_x = m.width
        screen_y = m.height

screen_x_center = int(screen_x/2)
screen_y_center = int(screen_y/2)


# Create the window
window = tk.Tk()
window.title("Joy 2 Mouse")
window.geometry("-100+100")
window.resizable(False, False)
window.protocol("WM_DELETE_WINDOW", stop_app)

main_control_tab = ttk.Notebook(window)
run_tab = ttk.Frame(main_control_tab)
test_tab = ttk.Frame(main_control_tab)


# Menu setup
menu = tk.Menu(window)
window.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open...", command=load_config)
file_menu.add_command(label="Save", command=save_config)
file_menu.add_command(label="Save As...", command=save_config_as)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=stop_app)


# Tab setup
config_tab = ttk.Frame(main_control_tab)
main_control_tab.add(run_tab, text="Run")
main_control_tab.add(test_tab, text="Test")
main_control_tab.add(config_tab, text="Config")
main_control_tab.pack(expand=1, fill="both")

run = gui.run.Tab(run_tab)
test = gui.test.Tab(test_tab)
config = gui.config.Tab(config_tab)


# Credits
bottomFrame = ttk.Frame(window)
bottomFrame.pack(side="bottom", fill="x")
versionLabel = ttk.Label(bottomFrame, text="v0.0.1")
versionLabel.pack(side="right", fill="x", padx=10, pady=10)

creditsLabel = ttk.Label(bottomFrame, text="Created by Stanley Skarshaug - www.haxor.no")
creditsLabel.pack(side="left", fill="x", padx=10, pady=10)


# Start the app
pygame.init()
pydirectinput.FAILSAFE = False # allow mouse to go outside of screen
joysticks = {}
app_running = True
active = False
mouse_x = 0
mouse_y = 0
debugging = False
max_refresh_rate = 165
last_mouse_x = 0
last_mouse_y = 0
deadzone = 10
activate_button_released = True
deactivate_button_released = True
activated = False
current_config_file = 'default.ini'
current_config_default = True


# Main loop
while app_running:
    # Get configuation
    translation_method = config.get_translation_method()

    autocenter = config.get_autocenter()
    autocenter_key = config.get_autocenter_key()

    armed = run.get_armed()
    joystick_resolution = int((2**config.get_joystick_resolution()) / 16)
    selected_joystick = config.get_joystick_selected()
    selected_x_axis = config.get_joystick_x_axis()
    selected_y_axis = config.get_joystick_y_axis()
    joystick_x_inverted = config.get_joystick_x_inverted()
    joystick_y_inverted = config.get_joystick_y_inverted()

    mouse_left_button = config.get_mouse_left()
    mouse_left_inverted = config.get_mouse_left_inverted()
    mouse_right_button = config.get_mouse_right()
    mouse_right_inverted = config.get_mouse_right_inverted()

    selected_activation_method = config.get_activation_method()
    selected_buttonbox = config.get_buttonbox_selected()
    activation_button = config.get_activation_button()
    activation_button_inverted = config.get_activation_button_inverted()

    deactivation_button = config.get_deactivation_button()
    deactivation_button_inverted = config.get_deactivation_button_inverted()

    if not joystick_config_ready():
        run.disable_arming()


    run.set_run_status(active, configured=joystick_config_ready())


    # Handle PyGame events
    for event in pygame.event.get():
        # Handle hotplugging
        if event.type == pygame.JOYDEVICEADDED:
            # This event will be generated when the program starts for every
            # joystick, filling up the list without needing to create them manually.
            joy = pygame.joystick.Joystick(event.device_index)
            joysticks[joy.get_instance_id()] = joy
            test.update_device_list(joysticks)
            config.update_device_list(joysticks)

        if event.type == pygame.JOYDEVICEREMOVED:
            del joysticks[event.instance_id]
            print(f"Joystick {event.instance_id} disconnected")
            test.update_device_list(joysticks)
            config.update_device_list(joysticks)


    # Loop over all joysticks
    for joy in joysticks.values():
        
        # Handle activate button
        if selected_buttonbox and activation_button != None:
            if joy.get_guid() == selected_buttonbox:
                ## check if activation button is pressed
                activate_button_pressed = joy.get_button(activation_button)
                if activation_button_inverted:
                    activate_button_pressed = not activate_button_pressed

                if selected_activation_method == 1: # hold
                    activated = activate_button_pressed

                elif selected_activation_method == 2: # toggle
                    if not activated and activate_button_pressed and activate_button_released:
                        activated = True
                        activate_button_released = False
                    elif activated and not activate_button_pressed:
                        activate_button_released = True
                    elif activated and activate_button_pressed and activate_button_released:
                        activated = False
                        activate_button_released = False
                    elif not activated and not activate_button_pressed and not activate_button_released:
                        activate_button_released = True

                elif selected_activation_method == 3: # on/off
                    if deactivation_button != None:
                        deactivate_button_pressed = joy.get_button(deactivation_button)
                        if deactivation_button_inverted:
                            deactivate_button_pressed = not deactivate_button_pressed

                        if not activated and activate_button_released and activate_button_pressed and\
                            not deactivate_button_pressed:
                                activated = True
                                activate_button_released = False

                        elif activated and not activate_button_pressed and not activate_button_released and \
                            not deactivate_button_pressed:
                                activate_button_released = True
                        
                        elif activated and deactivate_button_released and deactivate_button_pressed and\
                            not activate_button_pressed:
                                activated = False
                                deactivate_button_released = False
                        
                        elif activated and not deactivate_button_released and not deactivate_button_pressed:
                                deactivate_button_released = True
                        

                if armed:
                    active = activated
                else:
                    active = False

                if not activate_button_pressed:
                    run.enable_arming()
                else:
                    run.disable_arming()

                ## update center position of mouse
                if not active:
                    mouse_x, mouse_y = mouse.get_position()
                    last_mouse_x = joystick_resolution
                    last_mouse_y = joystick_resolution

        # Handle joystick input
        if selected_joystick and selected_x_axis != None and selected_y_axis != None:
            if joy.get_guid() == selected_joystick:
                if active:
                    # set mouse position
                    if translation_method == 1: # default
                        x_axis_value = int(joy.get_axis(selected_x_axis) * 5000)
                        y_axis_value = int(joy.get_axis(selected_y_axis) * 5000)
                        
                        x_axis_value, y_axis_value = handle_inverted_axis(
                            [x_axis_value, y_axis_value], 
                            (joystick_x_inverted, joystick_y_inverted)
                        )

                        mouse_x_pos = mouse_x + x_axis_value
                        mouse_y_pos = mouse_y + y_axis_value
                        pydirectinput.moveTo(mouse_x_pos, mouse_y_pos, _pause=False)

                    elif translation_method == 2: # absolute mouse movement
                        x_axis_value = int(joy.get_axis(selected_x_axis) * screen_x_center)
                        y_axis_value = int(joy.get_axis(selected_y_axis) * screen_y_center)

                        x_axis_value, y_axis_value = handle_inverted_axis(
                            [x_axis_value, y_axis_value], 
                            (joystick_x_inverted, joystick_y_inverted)
                        )

                        mouse_x_pos = screen_x_center + x_axis_value
                        mouse_y_pos = screen_y_center - y_axis_value
                        pydirectinput.moveTo(mouse_x_pos, mouse_y_pos, _pause=False)

                    elif translation_method == 3: # relavitve mouse movement
                        x_axis_value = int(joy.get_axis(selected_x_axis) * joystick_resolution)
                        y_axis_value = int(joy.get_axis(selected_y_axis) * joystick_resolution)
                        mouse_Dx = x_axis_value - last_mouse_x
                        mouse_Dy = y_axis_value - last_mouse_y

                        mouse_Dx, mouse_Dy = handle_inverted_axis(
                            [mouse_Dx, mouse_Dy], 
                            (joystick_x_inverted, joystick_y_inverted)
                        )

                        last_mouse_x = x_axis_value
                        last_mouse_y = y_axis_value
                        pydirectinput.moveRel(mouse_Dx,mouse_Dy, _pause=False, relative=True)


                    # center torso if joystick is in deadzone
                    if autocenter and autocenter_key != None:
                        within_deadzone_x = x_axis_value > -deadzone and x_axis_value < deadzone
                        within_deadzone_y = y_axis_value > -deadzone and y_axis_value < deadzone

                        if within_deadzone_x and within_deadzone_y:
                            keyboard.press_and_release(autocenter_key)


                    if debugging:
                        if translation_method == 3:
                            print(f"Mouse: \tdX: {mouse_Dx} \tdY: {mouse_Dy} \tres: {joystick_resolution}")
                        else:
                            print(f"Mouse: \tX: {x_axis_value} \tY: {y_axis_value}")


                    # Mouse buttons
                    if mouse_left_button != None:
                        if joy.get_button(mouse_left_button):
                            pydirectinput.click(button="left")
                    if mouse_right_button != None:
                        if joy.get_button(mouse_right_button):
                            # Right mouse button
                            pydirectinput.click(button="right")


    ## Update the mouse position every frame
    time.sleep(1/max_refresh_rate)
    window.update()