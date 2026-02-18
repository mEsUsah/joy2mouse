import tkinter.ttk as ttk


class StatusIndicator:
    def __init__(self, parent):
        self.label = ttk.Label(
            parent,
            text="Not configured",
            foreground="white",
            background="gray",
            font=("Helvetica", 16),
            anchor="center",
            padding=20,
            border=2,
            borderwidth=2
        )
        self.label.pack(side="bottom", fill="x", padx=10, pady=6)

    def set(self, running, armed, configured):
        if running:
            self.label.config(text="Running",      foreground="white", background="#ea5252")
        elif armed and configured:
            self.label.config(text="Armed",        foreground="white", background="orange")
        elif configured:
            self.label.config(text="Disarmed",     foreground="white", background="#4caf50")
        else:
            self.label.config(text="Not configured", foreground="white", background="gray")
