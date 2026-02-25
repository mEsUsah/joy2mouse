# joy2mouse
Simple program to translate joystick axis to mouse movements and inputs for Windows hosts.


## 📦 Installation
1. Go to the [latest release page](https://github.com/mEsUsah/joy2mouse/releases/latest), and download the .exe file. 
2. Start the program. This program does not require any installation.
- Ignore the Windows Defender "unsigned software warning".
- The program will check for new releases on startup.

## 🕹️ GUI
1. Navigate to the config tab and set required inputs.
2. Navigate to the run tab, and turn on the arm switch.
3. Start game.
4. Activate/Deactivate with configured activation method to start translating joystick movement to mouse movement. 
- 📗A full user manual can be read at [www.haxor.no](https://haxor.no/en/article/joy2mouse).

## 🖥️ CLI
The program can be started from PowerShell and CMD, with support for startup automation. Run with -h or --help option to get a full set of options.
```cmd
joy2mouse_x.x.x.exe --help
```

## 💵 Support me!
- This is FOSS (Free and Open Source Software). I build this for fun, and mostly for my own needs. If you like it, find value in it, and would like to support me, please consider to ☕ [buy me a coffee](https://buymeacoffee.com/mesusah)! It would make my day! ❤️

## 🐛 Bugs / features found
- Please add a [issue](https://github.com/mEsUsah/joy2mouse/issues) with found bugs and feature suggestions.
- Look at the [todo](https://github.com/mEsUsah/joy2mouse/blob/master/TODO.md) for features and bugfixes that are in the pipeline. 

# 🚧For devs 🚧
The following section is inteded for developers who want to contribute to the project.

## Source code installation
For running from source and developing:  
⚠️NB! Use Python 3.12  
```cmd
# Activate virtual environment
py -m venv venv
venv\Scripts\actiavate.bat

# Install dependencies
py -m pip install -r .\requirements.txt

# When needed - deactivate virtual environment
deactivate
```

## Running from source
Once installed, the program can be launched from within the virtual environment.
```cmd
py app.py
```

## Build executable from source
Once installed, the program can be built into a single executable:
```cmd
build.bat
```

## Third-party documentation
- Mouse [Doc](https://github.com/boppreh/mouse)
- Keyboard [Doc](https://github.com/boppreh/keyboard)
- PyGame joystick [Doc](https://www.pygame.org/docs/ref/joystick.html)
- PyDirectInput [Doc](https://github.com/learncodebygaming/pydirectinput)
