# joy2mouse
Simple app to translate joystick axis to mouse movement for Windows hosts.

## Installation
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