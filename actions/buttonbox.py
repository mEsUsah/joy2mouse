import config
import gui
import utils

configModel = config.data.configModel

# Persistent state for toggle logic
activated = False
activate_button_released = True
deactivate_button_released = True


# Handle activate button
# Loop over all joysticks
def run():
    global activated, activate_button_released, deactivate_button_released
    for joy in config.data.joysticks.values():
        deactivate_button_pressed = False  # Ensure always defined
        if configModel['selected_buttonbox'] != None and configModel['activation_button'] != None:
            if joy.get_guid() == configModel['selected_buttonbox_uuid']:
                ## check if activation button is pressed
                try:
                    activation_button_index = int(configModel['activation_button']) if configModel['activation_button'] is not None and configModel['activation_button'] != "None" else None
                except ValueError:
                    activation_button_index = None
                activate_button_pressed = joy.get_button(activation_button_index) if activation_button_index is not None else False
                if configModel['activation_button_inverted']:
                    activate_button_pressed = not activate_button_pressed

                if configModel['activation_method'] == 1: # hold
                    activated = activate_button_pressed

                elif configModel['activation_method'] == 2: # toggle
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

                elif configModel['activation_method'] == 3: # on/off
                    if configModel['deactivation_button'] != None and configModel['deactivation_button'] != "None":
                        try:
                            deactivation_button_index = int(configModel['deactivation_button'])
                        except ValueError:
                            deactivation_button_index = None
                        deactivate_button_pressed = joy.get_button(deactivation_button_index) if deactivation_button_index is not None else False
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


                
                if configModel['armed']:
                    configModel['active'] = activated
                else:
                    configModel['active'] = False

                    

           