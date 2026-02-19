
import requests
import json
import tkinter as tk
import webbrowser

APP_VERSION = "v2.1.1"
APP_NAME = "Joy 2 Mouse"

def check_updates():
    url = "https://api.github.com/repos/mEsUsah/joy2mouse/releases/latest"
    headers = {
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    if data['name'] != APP_VERSION:
        message = f"""Joy2mouse {data['name']} is released!
            
Do you want to open the download page?"""

        update_box = tk.messagebox.askyesno(
            "New version", 
            message,
            icon="question",
            default="yes",
            )
        if update_box:
            webbrowser.open(data['html_url'])
