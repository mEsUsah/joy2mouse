import tkinter as tk
import tkinter.ttk as ttk
import gui

class Tab():
    def __init__(self, tab):
        '''This is the main tab for running the application'''
        elementaryTabContent = ttk.Frame(tab)
        elementaryTabContent.pack(side="top", expand=1, fill="both")

        tab1_label = ttk.Label(
            elementaryTabContent, 
            text="This is the main tab"
        )
        tab1_label.pack(side="top", fill="x", padx=10, pady=10)