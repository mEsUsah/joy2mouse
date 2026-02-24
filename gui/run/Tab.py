import tkinter.ttk as ttk

from gui.run.ArmSwitch import ArmSwitch
from gui.run.InputChecklist import InputChecklist
from gui.run.StatusIndicator import StatusIndicator


class Tab():
    def __init__(self, tab):
        '''This is the main tab for running the application'''
        self.running = False
        self._configured = False

        self.tab = tab
        self.row_1 = ttk.Frame(self.tab)
        self.row_1.pack(side="top", expand=1, fill="both")

        self.arm_switch = ArmSwitch(self.row_1, on_toggle=self._on_arm_toggled)
        self.checklist  = InputChecklist(self.row_1)
        self.status     = StatusIndicator(self.row_1)

    def _on_arm_toggled(self):
        self._update_status()

    def get_armed(self):
        return self.arm_switch.get_armed()

    def arm(self):
        self.arm_switch.arm()

    def enable_arming(self):
        self._configured = True
        self.arm_switch.enable_arming()
        self._update_status()

    def disable_arming(self):
        self._configured = False
        self.arm_switch.disable_arming()
        self._update_status()

    def set_run_status(self, status, configured=True):
        self._configured = configured
        self.running = status
        self.arm_switch.set_run_status(running=status, configured=configured)
        self._update_status()

    def _update_status(self):
        armed = self.arm_switch.get_armed()
        if not self._configured:
            self.arm_switch.reset_armed()
        self.checklist.update()
        self.status.set(self.running, armed, self._configured)
