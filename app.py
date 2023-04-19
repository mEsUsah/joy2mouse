#! /bin/env python3

import keyboard  # using module keyboard
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
window.title("Joy 2 Game Mouse")
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

while app_running:
    for event in pygame.event.get():
        # Handle hotplugging
        if event.type == pygame.JOYDEVICEADDED:
            # This event will be generated when the program starts for every
            # joystick, filling up the list without needing to create them manually.
            joy = pygame.joystick.Joystick(event.device_index)
            joysticks[joy.get_instance_id()] = joy
            print(f"Joystick {joy.get_guid()} connencted")

        if event.type == pygame.JOYDEVICEREMOVED:
            del joysticks[event.instance_id]
            print(f"Joystick {event.instance_id} disconnected")


    for joy in joysticks.values():
        if joy.get_guid() == "03000000443300005982000000000000": # VPC Panel 1
            ## check if activatino button is pressed
            active = joy.get_button(19)

        if joy.get_guid() == "030000001d2300000002000000000000": # Gladiator NXT
            # set mouse position
            if active:
                x_axis_value = int(joy.get_axis(0) * 10000 / 2)
                y_axis_value = int(joy.get_axis(1) * 10000 / 2)

                mouse.move(x_axis_value, y_axis_value, absolute=True, duration=0)
    
    
    ## Update the display
    time.sleep(0.005)
    window.update()