#! /bin/env python3

# stdlib
import argparse
import ctypes
import io
import os
import sys
import time
import webbrowser
import tkinter as tk
from tkinter import ttk

# PyInstaller console builds can set sys.stdout/stderr to None.
if sys.stdout is None:
    sys.stdout = io.StringIO()
if sys.stderr is None:
    sys.stderr = io.StringIO()

# third-party
import mouse
import pygame
from screeninfo import get_monitors

# local
import actions
import config
import gui
import utils


def _resource(rel):
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel)


def _set_icon(window, ico_path):
    """Set window + taskbar icon using PIL iconphoto + ctypes class override."""
    from PIL import Image, ImageTk
    from ctypes import wintypes

    window.update_idletasks()

    # PIL iconphoto — sets title bar and informs tkinter's icon system
    img   = Image.open(ico_path).convert("RGBA")
    photo = ImageTk.PhotoImage(img)
    window.iconphoto(True, photo)
    window._icon_photo = photo  # prevent GC

    # ctypes — overwrite the Tk window class icon so taskbar picks it up
    hwnd   = window.winfo_id()
    user32 = ctypes.windll.user32
    buf_l  = (wintypes.HICON * 1)()
    buf_s  = (wintypes.HICON * 1)()
    if ctypes.windll.shell32.ExtractIconExW(sys.executable, 0, buf_l, buf_s, 1) > 0:
        if buf_l[0]:
            user32.SetClassLongPtrW(hwnd, -14, buf_l[0])   # GCL_HICON
            user32.SendMessageW(hwnd, 0x80, 1, buf_l[0])   # WM_SETICON ICON_BIG
        if buf_s[0]:
            user32.SetClassLongPtrW(hwnd, -34, buf_s[0])   # GCL_HICONSM
            user32.SendMessageW(hwnd, 0x80, 0, buf_s[0])   # WM_SETICON ICON_SMALL

_parser = argparse.ArgumentParser(
    prog="joy2mouse",
    description="Joy 2 Mouse — use your joystick as a mouse",
    epilog="User manual: https://haxor.no/en/article/joy2mouse",
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
_parser.add_argument(
    "-c", "--config",
    metavar="FILE",
    help="path to a .ini profile to load on startup",
)
_parser.add_argument(
    "-a", "--arm",
    action="store_true",
    help="arm automatically on startup (requires --config)",
)
_args = _parser.parse_args()

# Hide the console window — built with console=True for CLI flag support,
# but the console itself should never be visible to the user.
try:
    _hwnd_console = ctypes.windll.kernel32.GetConsoleWindow()
    if _hwnd_console:
        ctypes.windll.user32.ShowWindow(_hwnd_console, 0)  # SW_HIDE
except Exception:
    pass

def stop_app():
    global app_running
    app_running = False


def update_title():
    cfg_file = config.data.configModel['current_config_file']
    filename = os.path.basename(cfg_file)
    window.title(f"{utils.releases.APP_NAME} - {filename}")


def open_manual():
    webbrowser.open("https://haxor.no/en/article/joy2mouse")


def open_config_file():
    pygame.event.pump()  # Flush pygame state before blocking tkinter dialog
    config.load.load_config_file()
    pygame.event.pump()  # Drain events that queued during dialog
    configView.populate_from_config(config.data.configModel)
    configView.update_config()
    update_title()


def save_config():
    pygame.event.pump()
    config.save.save_config()
    pygame.event.pump()
    update_title()


def save_config_as():
    pygame.event.pump()
    config.save.save_config_as()
    pygame.event.pump()
    update_title()


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

screen_x_center = int(screen_x/2)
screen_y_center = int(screen_y/2)
configModel['screen_x_center'] = screen_x_center
configModel['screen_y_center'] = screen_y_center


# Create the window
window = tk.Tk()
window.withdraw()  # hide before taskbar captures the feather icon
_set_icon(window, _resource("logo.ico"))
window.title(utils.releases.APP_NAME)
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

window.deiconify()  # show now that the icon is set

# Start the app
pygame.init()
_autoload_pending = bool(_args.config)
_autoarm_pending  = False


# Main loop
while app_running:
    # Get configuation
    config.data.configModel['armed'] = runView.get_armed()
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

    if _autoarm_pending and config.data.joystick_config_ready():
        _autoarm_pending = False
        runView.arm()

    if _autoload_pending:
        _autoload_pending = False
        config.data.configModel['current_config_file'] = _args.config
        config.data.configModel['current_config_default'] = False
        config.load.load_config()
        configView.populate_from_config(config.data.configModel)
        configView.update_config()
        update_title()
        _autoarm_pending = bool(_args.arm)

    ## update center position of mouse
    if not active:
        actions.joystick.release_mouse_buttons()
        mouse_x, mouse_y = mouse.get_position()
        configModel['mouse_x'] = mouse_x
        configModel['mouse_y'] = mouse_y
        configModel['last_mouse_x'] = 0
        configModel['last_mouse_y'] = 0

    if config.data.joystick_config_ready():
        actions.buttonbox.run()
    
    if active:
        actions.joystick.run()

    ## Update the mouse position every frame
    time.sleep(1/max_refresh_rate)
    window.update()