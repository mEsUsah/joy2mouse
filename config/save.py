import config
import utils


def save_config():
    if config.data.current_config_file == 'default.ini':
        file_path = utils.files.gui_save_as_path()
        if not file_path:
            return # User canceled the save dialog
        config.data.current_config_file = file_path

    current_config = config.data.get_current_config()
    with open(config.data.current_config_file, 'w') as configfile:
        current_config.write(configfile)


def save_config_as():
    file_path = utils.files.gui_save_as_path()
    if not file_path:
        return # User canceled the save dialog
    config.data.current_config_file = file_path

    current_config = config.data.get_current_config()
    with open(config.data.current_config_file, 'w') as configfile:
        current_config.write(configfile)