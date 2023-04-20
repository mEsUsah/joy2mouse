#! /bin/env python3

import keyboard
import pydirectinput
import mouse
import pygame
import time
import tkinter as tk
from tkinter import ttk
import gui

app_running = True
def stop_app():
    global app_running
    app_running = False

# Create the window
window = tk.Tk()
window.title("Joy 2 Mouse")
window.geometry("-100+100")
window.resizable(False, False)
window.protocol("WM_DELETE_WINDOW", stop_app)

main_control_tab = ttk.Notebook(window)
run_tab = ttk.Frame(main_control_tab)
test_tab = ttk.Frame(main_control_tab)
config_tab = ttk.Frame(main_control_tab)
main_control_tab.add(run_tab, text="Run")
main_control_tab.add(test_tab, text="Test")
main_control_tab.add(config_tab, text="Config")
main_control_tab.pack(expand=1, fill="both")

gui.run.Tab(run_tab)
gui.test.Tab(test_tab)
gui.config.Tab(config_tab)

# Credits
bottomFrame = ttk.Frame(window)
bottomFrame.pack(side="bottom", fill="x")
versionLabel = ttk.Label(bottomFrame, text="v0.0.1")
versionLabel.pack(side="right", fill="x", padx=10, pady=10)

creditsLabel = ttk.Label(bottomFrame, text="Created by Stanley Skarshaug - www.haxor.no")
creditsLabel.pack(side="left", fill="x", padx=10, pady=10)

pygame.init()
joysticks = {}
active = False
mouse_x = 0
mouse_y = 0

screen_x = 2560
screen_y = 1440

mechwarrior5 = True
debugging = False

pydirectinput.FAILSAFE = False

while app_running:
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
        if joy.get_guid() == "03000000443300005982000000000000": # VPC Panel 1
            ## check if activation button is pressed
            active = joy.get_button(19)
            if not active:
                mouse_x, mouse_y = mouse.get_position()

        if joy.get_guid() == "030000001d2300000002000000000000": # Gladiator NXT
            if active:
                # set mouse position
                if mechwarrior5:
                    x_axis_value = int(joy.get_axis(0) * (screen_x/2) )
                    y_axis_value = int(joy.get_axis(1) * screen_y/2 )
                    pydirectinput.moveTo(int(screen_x/2) + x_axis_value, int(screen_y/2) - y_axis_value, duration=0.1, _pause=False)

                    # center torso if joystick is in deadzone
                    deadzone = 10
                    within_deadzone_x = x_axis_value > -deadzone and x_axis_value < deadzone
                    within_deadzone_y = y_axis_value > -deadzone and y_axis_value < deadzone
                    if within_deadzone_x and within_deadzone_y:
                        keyboard.press_and_release("c")

                else:
                    x_axis_value = int(joy.get_axis(0) * 10000 / 2)
                    y_axis_value = int(joy.get_axis(1) * 10000 / 2)
                    pydirectinput.moveTo(mouse_x + x_axis_value, mouse_y - y_axis_value, duration=0.1, _pause=False)
                
                if debugging:
                    print(f"X: {x_axis_value} \tY: {y_axis_value}")
                

                # extra functionality for buttons
                if joy.get_button(0):
                    pydirectinput.click()
                if joy.get_button(2):
                    pydirectinput.click(button="right")
                    

    ## Update the display
    time.sleep(0.005)
    window.update()