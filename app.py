#! /bin/env python3

import keyboard  # using module keyboard
import mouse
while True:  # making a loop
    if keyboard.is_pressed('q'):  # if key 'q' is pressed 
        print('You Pressed A Key!')
        break  # finishing the loop
    # elif keyboard.is_pressed('w'):
    #     mouse.move(200, 0, absolute=True, duration=0)