#! /bin/env python3

import keyboard  # using module keyboard
import mouse
import pygame
import time


pygame.init()
joysticks = {}
active = False

while True:
    time.sleep(0.005)
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