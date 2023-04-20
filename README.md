# joy2mouse
Simple app to translate joystick axis to mouse movement.

## Installation windows
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
## Linux (Debian) Installation
```bash
# Activate virtual environment
python3 -m venv venv
chmod +x venv/bin/activate
source venv/bin/activate

# Install dependencies
sudo apt install python3-tk
pip install -r requirements.txt 
```

## Third-party documentation
- Mouse [Doc](https://github.com/boppreh/mouse)
- Keyboard [Doc](https://github.com/boppreh/keyboard)
- PyGame joystick [Doc](https://www.pygame.org/docs/ref/joystick.html)
- PyDirectInput [Doc](https://github.com/learncodebygaming/pydirectinput)