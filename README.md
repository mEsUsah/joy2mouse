# joy2mouse
Simple app to translate joystick axis to mouse movement for Windows hosts.


## Installation
- Go to the [latest release page](https://github.com/mEsUsah/joy2mouse/releases/latest), and download the .exe file. 
- Execute the program. This program does not require any installation.
- Ignore the Windows Defender "unsigned software warning".

## Usage
- Configure joystick and activation method.
- Check the "Arm" checkmark
- Start game
- Activate/Deactivate with configured activation method to start translating joystick movement to mouse movement.


## Notes:
- This is a work in progress - look at the [TODO](https://github.com/mEsUsah/joy2mouse/blob/master/TODO.md) for features I want to implement.
- The program will talk to the github API to check for new releases on startup.


## Source code installation - for devs
For running and working on source code
```cmd
# Activate virtual environment
python3 -m venv venv
venv\Scripts\actiavate.bat

# Install dependencies
pip install -r requriements.txt

# When needed - deactivate virtual environment
deactivate
```

## Build executable from source
Once installed, the program can be built into a single executable:
```cmd
build.bat
```

## Running from source
Once installed, the program can be launched from within the virtual environment.
```cmd
python app.py
```

## Third-party documentation
- Mouse [Doc](https://github.com/boppreh/mouse)
- Keyboard [Doc](https://github.com/boppreh/keyboard)
- PyGame joystick [Doc](https://www.pygame.org/docs/ref/joystick.html)
- PyDirectInput [Doc](https://github.com/learncodebygaming/pydirectinput)
