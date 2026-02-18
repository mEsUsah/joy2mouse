import tkinter as tk

import config.data

_BG        = "#0b0b1f"
_BORDER    = "#1a3a6a"
_FG_HEAD   = "#3366aa"
_FG_LABEL  = "#44aacc"
_FG_OK     = "#00ff88"
_FG_FAIL   = "#ff3355"
_FG_NA     = "#2a3a4a"
_FONT_HEAD = ("Courier New", 8, "bold")
_FONT_ROW  = ("Courier New", 10, "bold")

_ROWS = [
    ("JOYSTICK",  "device"),
    ("BUTTONBOX", "buttonbox"),
    ("X-AXIS",    "x_axis"),
    ("Y-AXIS",    "y_axis"),
    ("ACTV BTN",  "actv_btn"),
    ("DACT BTN",  "dact_btn"),
]


class InputChecklist:
    def __init__(self, parent):
        outer = tk.Frame(parent, bg=_BG,
                         highlightthickness=1, highlightbackground=_BORDER)
        outer.pack(side="top", fill="x", padx=10, pady=(0, 8))

        tk.Label(outer, text="// INPUT CONFIG STATUS", bg=_BG, fg=_FG_HEAD,
                 font=_FONT_HEAD, anchor="w", padx=6, pady=4
                 ).pack(side="top", fill="x")

        tk.Frame(outer, bg=_BORDER, height=1).pack(side="top", fill="x")

        inner = tk.Frame(outer, bg=_BG, padx=8, pady=6)
        inner.pack(side="top", fill="x")

        self._labels = {}
        for display, key in _ROWS:
            row = tk.Frame(inner, bg=_BG)
            row.pack(side="top", fill="x", pady=2)

            tk.Label(row, text=display, bg=_BG, fg=_FG_LABEL,
                     font=_FONT_ROW, anchor="w", width=10
                     ).pack(side="left")

            lbl = tk.Label(row, text="[ ? ]", bg=_BG, fg=_FG_NA,
                           font=_FONT_ROW, anchor="e")
            lbl.pack(side="right")
            self._labels[key] = lbl

    def update(self):
        m = config.data.configModel
        method = int(m.get("activation_method", 1))

        self._set("device",    m.get("selected_joystick_uuid") is not None)
        self._set("buttonbox", m.get("selected_buttonbox_uuid") is not None)
        self._set("x_axis",   m.get("joystick_x_axis") is not None)
        self._set("y_axis",   m.get("joystick_y_axis") is not None)
        self._set("actv_btn", m.get("activation_button") is not None)
        self._set("dact_btn", m.get("deactivation_button") is not None,
                  na=(method != 3))

    def _set(self, key, ok, na=False):
        lbl = self._labels[key]
        if na:
            lbl.config(text="[ - ]", fg=_FG_NA)
        elif ok:
            lbl.config(text="[ Y ]", fg=_FG_OK)
        else:
            lbl.config(text="[ N ]", fg=_FG_FAIL)
