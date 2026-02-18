#! /bin/env python3



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
import actions

def stop_app():
    global app_running
    app_running = False


def open_manual():
    webbrowser.open("https://haxor.no/en/article/joy2mouse")


def open_config_file():
    config.load.load_config_file()
    pygame.event.pump()  # Prevent GIL crash after blocking tkinter dialog
    configView.populate_from_config(config.data.configModel)


def save_config():
    config.save.save_config()
    pygame.event.pump()  # Prevent GIL crash after blocking tkinter dialog


def save_config_as():
    config.save.save_config_as()
    pygame.event.pump()  # Prevent GIL crash after blocking tkinter dialog


configModel = config.data.configModel
app_running = True
active = configModel['active']
mouse_x = configModel['mouse_x']
mouse_y = configModel['mouse_y']
last_mouse_x = configModel['last_mouse_x']
last_mouse_y = configModel['last_mouse_y']
debugging = configModel['debugging']
max_refresh_rate = configModel['max_refresh_rate']
activate_button_pressed = configModel['activate_button_pressed']
deactivate_button_pressed = configModel['deactivate_button_pressed']
joystick_resolution = configModel['joystick_resolution']
joysticks = config.data.joysticks
activated = False

# Get game screen size
screen_x = None
screen_y = None
for m in get_monitors():
    if m.is_primary:
        screen_x = m.width
        screen_y = m.height

screen_x_center = configModel['screen_x_center']
screen_y_center = configModel['screen_y_center']
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
file_menu.add_command(label="Open...", command=open_config_file)
file_menu.add_command(label="Save", command=save_config)
file_menu.add_command(label="Save As...", command=save_config_as)
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


# Main loop
while app_running:
    # Get configuation
    config.data.configModel['armed'] = runView.get_armed()
    joystick_resolution = int((2**configModel['joystick_resolution']) / 16)

    # Always update 'active' from configModel
    active = configModel['active']


    config_ready = config.data.joystick_config_ready()
    if not config_ready:
        runView.disable_arming()
    else:
        if not activate_button_pressed:
            runView.enable_arming()
        else:
            runView.disable_arming()

    runView.set_run_status(active, configured=config_ready)

    if main_control_tab.index("current") == 1: # Test tab
        testView.update_axis_view()
    if main_control_tab.index("current") == 2: # Config tab
        configView.update_config()

    # Handle PyGame events
    for event in pygame.event.get():
        # Handle hotplugging
        if event.type == pygame.JOYDEVICEADDED:
            # This event will be generated when the program starts for every
            # joystick, filling up the list without needing to create them manually.
            joy = pygame.joystick.Joystick(event.device_index)
            config.data.joysticks[joy.get_instance_id()] = joy
            testView.update_device_list(joysticks)
            configView.update_device_list(joysticks)

        if event.type == pygame.JOYDEVICEREMOVED:
            del config.data.joysticks[event.instance_id]
            print(f"Joystick {event.instance_id} disconnected")
            testView.update_device_list(config.data.joysticks)
            configView.update_device_list(config.data.joysticks)

    ## update center position of mouse
    if not active:
        actions.joystick.release_mouse_buttons()
        mouse_x, mouse_y = mouse.get_position()
        last_mouse_x = joystick_resolution
        last_mouse_y = joystick_resolution

    if config.data.joystick_config_ready():
        actions.buttonbox.run()
    
    if active:
        actions.joystick.run()

    ## Update the mouse position every frame
    time.sleep(1/max_refresh_rate)
    window.update()