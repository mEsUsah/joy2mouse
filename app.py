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

def stop_app():
    global app_running
    app_running = False


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
joystick_resolution = int(32767/8)
last_mouse_x = joystick_resolution
last_mouse_y = joystick_resolution
deadzone = 10


# Main loop
while app_running:
    # Get configuation
    translation_method = config.get_translation_method()
    autocenter = config.get_autocenter()
    armed = run.get_armed()


    # Handle PyGame events
    for event in pygame.event.get():
        # Handle hotplugging
        if event.type == pygame.JOYDEVICEADDED:
            # This event will be generated when the program starts for every
            # joystick, filling up the list without needing to create them manually.
            joy = pygame.joystick.Joystick(event.device_index)
            joysticks[joy.get_instance_id()] = joy
            print(f'Connencted Joystick "{joy.get_name()}" \t{joy.get_guid()}')

        if event.type == pygame.JOYDEVICEREMOVED:
            del joysticks[event.instance_id]
            print(f"Joystick {event.instance_id} disconnected")


    # Loop over all joysticks
    for joy in joysticks.values():
        
        # Handle start button
        if joy.get_guid() == "03000000443300005982000000000000": # VPC Panel 1
            ## check if activation button is pressed
            if armed:
                active = joy.get_button(19)
            else:
                active = False

            ## update center position of mouse
            if not active:
                mouse_x, mouse_y = mouse.get_position()
                last_mouse_x = joystick_resolution
                last_mouse_y = joystick_resolution

        # Handle joystick input
        if joy.get_guid() == "030000001d2300000002000000000000": # Gladiator NXT
            if active:
                # set mouse position
                if translation_method == 1: # default
                    x_axis_value = int(joy.get_axis(0) * 5000)
                    y_axis_value = int(joy.get_axis(1) * 5000)
                    mouse_x_pos = mouse_x + x_axis_value
                    mouse_y_pos = mouse_y - y_axis_value
                    pydirectinput.moveTo(mouse_x_pos, mouse_y_pos, _pause=False)
                
                elif translation_method == 2: # absolute mouse movement
                    x_axis_value = int(joy.get_axis(0) * screen_x_center)
                    y_axis_value = int(joy.get_axis(1) * screen_y_center)
                    mouse_x_pos = screen_x_center + x_axis_value
                    mouse_y_pos = screen_y_center - y_axis_value
                    pydirectinput.moveTo(mouse_x_pos, mouse_y_pos, _pause=False)

                elif translation_method == 3: # relavitve mouse movement
                    x_axis_value = int(joy.get_axis(0) * joystick_resolution)
                    y_axis_value = int(joy.get_axis(1) * joystick_resolution)
                    mouse_Dx = x_axis_value - last_mouse_x
                    mouse_Dy = y_axis_value - last_mouse_y
                    last_mouse_x = x_axis_value
                    last_mouse_y = y_axis_value
                    pydirectinput.moveRel(mouse_Dx,mouse_Dy, _pause=False, relative=True)


                # center torso if joystick is in deadzone
                if autocenter:
                    within_deadzone_x = x_axis_value > -deadzone and x_axis_value < deadzone
                    within_deadzone_y = y_axis_value > -deadzone and y_axis_value < deadzone

                    if within_deadzone_x and within_deadzone_y:
                        keyboard.press_and_release("c")


                if debugging:
                    if translation_method == 3:
                        print(f"Mouse: \tdX: {mouse_Dx} \tdY: {mouse_Dy}")
                    else:
                        print(f"Mouse: \tX: {x_axis_value} \tY: {y_axis_value}")
                

                # extra functionality for buttons
                if joy.get_button(0):
                    # Left mouse button
                    pydirectinput.click(button="left")
                if joy.get_button(2):
                    # Right mouse button
                    pydirectinput.click(button="right")
                    

    ## Update the mouse position every frame
    time.sleep(1/max_refresh_rate)
    window.update()