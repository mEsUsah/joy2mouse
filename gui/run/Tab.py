import tkinter.ttk as ttk

from gui.run.ArmSwitch import ArmSwitch


class Tab():
    def __init__(self, tab):
        '''This is the main tab for running the application'''
        self.running = False
        self._configured = False

        self.tab = tab
        self.row_1 = ttk.Frame(self.tab)
        self.row_1.pack(side="top", expand=1, fill="both")

        self.arm_switch = ArmSwitch(self.row_1, on_toggle=self._on_arm_toggled)

        self.status_label = ttk.Label(
            self.row_1,
            text="Not configured",
            foreground="white",
            background="gray",
            font=("Helvetica", 16),
            anchor="center",
            padding=20,
            border=2,
            borderwidth=2
        )
        self.status_label.pack(side="bottom", fill="x", padx=10, pady=6)

    def _on_arm_toggled(self):
        self.update_status()

    def get_armed(self):
        return self.arm_switch.get_armed()

    def enable_arming(self):
        self._configured = True
        self.arm_switch.enable_arming()
        self.update_status()

    def disable_arming(self):
        self._configured = False
        self.arm_switch.disable_arming()
        self.update_status()

    def set_run_status(self, status, configured=True):
        self._configured = configured
        self.running = status
        self.arm_switch.set_run_status(running=status, configured=configured)
        self.update_status()

    def update_status(self):
        if self.running:
            self.status_label.config(
                text="Running",
                foreground="white",
                background="red"
            )
        elif self.arm_switch.get_armed() and self._configured:
            self.status_label.config(
                text="Armed",
                foreground="white",
                background="orange"
            )
        elif self._configured:
            self.status_label.config(
                text="Disarmed",
                foreground="white",
                background="green"
            )
        else:
            self.arm_switch.reset_armed()
            self.status_label.config(
                text="Not configured",
                foreground="white",
                background="gray"
            )
