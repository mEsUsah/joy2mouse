#! /bin/env python3

import keyboard
import pydirectinput
import mouse
import pygame
import time
import tkinter as tk
from tkinter import ttk
from screeninfo import get_monitors
import gui
import utils
import config
import webbrowser

def stop_app():
    global app_running
    app_running = False


def handle_inverted_axis(axis, inverted):
    for i in range(len(axis)):
        if inverted[i]:
            axis[i] *= -1
    return axis


def open_manual():
    webbrowser.open("https://haxor.no/en/article/joy2mouse")


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
window.title(utils.releases.APP_NAME)
window.geometry("-100+100")
window.resizable(False, False)
window.protocol("WM_DELETE_WINDOW", stop_app)
# window.iconbitmap(sys.executable)

main_control_tab = ttk.Notebook(window)
run_tab = ttk.Frame(main_control_tab)
test_tab = ttk.Frame(main_control_tab)


# Menu setup
menu = tk.Menu(window)
window.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open...", command=config.load.load_config_file)
file_menu.add_command(label="Save", command=config.save.save_config)
file_menu.add_command(label="Save As...", command=config.save.save_config_as)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=stop_app)

help_menu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="User manual", command=open_manual)


# Tab setup
config_tab = ttk.Frame(main_control_tab)
main_control_tab.add(run_tab, text="Run")
main_control_tab.add(test_tab, text="Test")
main_control_tab.add(config_tab, text="Config")
main_control_tab.pack(expand=1, fill="both")

runView = gui.run.Tab(run_tab)
testView = gui.test.Tab(test_tab)
configView = gui.config.Tab(config_tab)


# Credits
bottomFrame = ttk.Frame(window)
bottomFrame.pack(side="bottom", fill="x")
versionLabel = ttk.Label(bottomFrame, text=utils.APP_VERSION)
versionLabel.pack(side="right", fill="x", padx=10, pady=10)

creditsLabel = ttk.Label(bottomFrame, text="Created by Stanley Skarshaug - www.haxor.no")
creditsLabel.pack(side="left", fill="x", padx=10, pady=10)


#Check for updates
utils.releases.check_updates()


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
activate_button_released = True
deactivate_button_released = True
activated = False

# load_config()


# Main loop
while app_running:
    # Get configuation
    configModel = config.data.configModel

    armed = runView.get_armed()
    joystick_resolution = int((2**configModel['joystick_resolution']) / 16)

    if not config.data.joystick_config_ready():
        runView.disable_arming()


    runView.set_run_status(active, configured=config.data.joystick_config_ready())
    
    if main_control_tab.index("current") == 1: # Test tab
        testView.update_axis_view()


    # Handle PyGame events
    for event in pygame.event.get():
        # Handle hotplugging
        if event.type == pygame.JOYDEVICEADDED:
            # This event will be generated when the program starts for every
            # joystick, filling up the list without needing to create them manually.
            joy = pygame.joystick.Joystick(event.device_index)
            joysticks[joy.get_instance_id()] = joy
            testView.update_device_list(joysticks)
            configView.update_device_list(joysticks)

        if event.type == pygame.JOYDEVICEREMOVED:
            del joysticks[event.instance_id]
            print(f"Joystick {event.instance_id} disconnected")
            testView.update_device_list(joysticks)
            configView.update_device_list(joysticks)


    # Loop over all joysticks
    for joy in joysticks.values():
        
        # Handle activate button
        if configModel['selected_buttonbox'] != None and configModel['activation_button'] != None:
            if joy.get_guid() == configModel['selected_buttonbox_uuid']:
                ## check if activation button is pressed
                activate_button_pressed = joy.get_button(configModel['activation_button'])
                if configModel['activation_button_inverted']:
                    activate_button_pressed = not activate_button_pressed

                if configModel['selected_activation_method'] == 1: # hold
                    activated = activate_button_pressed

                elif configModel['selected_activation_method'] == 2: # toggle
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

                elif configModel['selected_activation_method'] == 3: # on/off
                    if configModel['deactivation_button'] != None:
                        deactivate_button_pressed = joy.get_button(deactivation_button)
                        if configModel['deactivation_button_inverted']:
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
                    runView.enable_arming()
                else:
                    runView.disable_arming()

                ## update center position of mouse
                if not active:
                    mouse_x, mouse_y = mouse.get_position()
                    last_mouse_x = joystick_resolution
                    last_mouse_y = joystick_resolution

        # Handle joystick input
        if configModel['selected_joystick'] and (configModel['joystick_x_axis'] != None or configModel['joystick_y_axis'] != None):
            if joy.get_guid() == configModel['selected_joystick_uuid']:
                if active:

                    # Handle one axis set to None
                    if configModel['selected_x_axis'] == None:
                        joystick_x_axis = 0
                    else:
                        joystick_x_axis = joy.get_axis(configModel['selected_x_axis'])
                    
                    if configModel['selected_y_axis'] == None:
                        joystick_y_axis = 0
                    else:
                        joystick_y_axis = joy.get_axis(configModel['selected_y_axis'])

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


                    # Mouse buttons
                    if configModel['mouse_left_button'] != None:
                        if joy.get_button(configModel['mouse_left_button']):
                            pydirectinput.click(button="left")
                    if configModel['mouse_right_button'] != None:
                        if joy.get_button(configModel['mouse_right_button']):
                            # Right mouse button
                            pydirectinput.click(button="right")


    ## Update the mouse position every frame
    time.sleep(1/max_refresh_rate)
    window.update()