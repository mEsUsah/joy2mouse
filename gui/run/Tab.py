import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageDraw, ImageTk


class Tab():
    def __init__(self, tab):
        '''This is the main tab for running the application'''
        self.armed = tk.BooleanVar(value=False)
        self.running = False
        self._configured = False
        self._hazard_img = None  # prevent GC
        self._last_drawn = None  # skip redraw if state unchanged

        self.tab = tab
        self.row_1 = ttk.Frame(self.tab)
        self.row_1.pack(side="top", expand=1, fill="both")

        self._tw   = 50   # track width
        self._th   = 24   # track height
        self._pad  = 10   # canvas padding around track
        self._scale = 4   # supersampling factor
        self._hpad = 12   # padding inside hazard zone

        cw = self._tw + self._pad * 2
        ch = self._th + self._pad * 2
        self._cw = cw
        self._ch = ch

        self.hazard_canvas = tk.Canvas(
            self.row_1,
            height=ch + self._hpad * 2,
            highlightthickness=3,
            highlightbackground="#222222",
        )
        self.hazard_canvas.pack(side="top", fill="x", padx=10, pady=20)

        _bg_tk = ttk.Style().lookup("TFrame", "background")
        try:
            rgb = self.hazard_canvas.winfo_rgb(_bg_tk)
            self._win_bg = "#{:02x}{:02x}{:02x}".format(rgb[0]>>8, rgb[1]>>8, rgb[2]>>8)
        except Exception:
            self._win_bg = "#f0f0f0"
        self.hazard_canvas.bind("<Configure>", lambda _e: self._draw_hazard())
        self.hazard_canvas.bind("<Button-1>", self._on_click)
        self.hazard_canvas.bind("<Motion>",   self._on_motion)
        self.hazard_canvas.bind("<Leave>",    lambda _e: self._draw_hazard(hover=False))

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

    def _in_switch(self, x, y):
        h = self.hazard_canvas.winfo_height()
        sw_y = (h - self._ch) // 2
        return (self._hpad <= x <= self._hpad + self._cw and
                sw_y <= y <= sw_y + self._ch)

    def _on_click(self, event):
        if self._in_switch(event.x, event.y) and self._configured and not self.running:
            self._toggle_arm()

    def _on_motion(self, event):
        hover = self._in_switch(event.x, event.y)
        if hover and self._configured and not self.running:
            self.hazard_canvas.configure(cursor="hand2")
        else:
            self.hazard_canvas.configure(cursor="arrow")
        self._draw_hazard(hover=hover)

    def _make_stripe_img(self, w, h, stripe=12):
        img  = Image.new("RGB", (w, h), "#ffaa00")
        draw = ImageDraw.Draw(img)
        for x in range(-h, w + h + stripe, stripe * 2):
            draw.polygon([
                (x,          0),
                (x + stripe, 0),
                (x + stripe + h, h),
                (x + h,      h),
            ], fill="#111111")
        return img

    def _draw_hazard(self, hover=False):
        w = self.hazard_canvas.winfo_width()
        h = self.hazard_canvas.winfo_height()
        if w < 2 or h < 2:
            return

        armed = self.armed.get()
        is_on = armed or self.running

        state = (is_on, self._configured, self.running, hover, w, h)
        if state == self._last_drawn:
            return
        self._last_drawn = state

        if not self._configured:
            track_color = "#555555"
            thumb_color = "#888888"
        elif self.running:
            track_color = "#ff0000"
            thumb_color = "#ffffff"
        elif armed:
            track_color = "#ff0000"
            thumb_color = "#ffffff"
        else:
            track_color = "#aaaaaa"
            thumb_color = "#ffffff"

        # Full hazard background
        img = self._make_stripe_img(w, h)

        # Render switch area at 4x and paste in
        s  = self._scale
        tw = self._tw * s
        th = self._th * s
        p  = self._pad * s
        iw = self._cw * s
        ih = self._ch * s
        r  = th // 2

        sw = Image.new("RGB", (iw, ih), "#000000")
        sd = ImageDraw.Draw(sw)
        hover_active = hover and self._configured and not self.running
        outline = "#888888" if hover_active else track_color
        sd.rounded_rectangle([p, p, p + tw, p + th], radius=r,
                              fill=track_color, outline=outline, width=s)

        inset = s
        td = th - inset * 2
        tx = (p + tw - r) if is_on else (p + r)
        ty = p + th // 2
        sd.ellipse([tx - td//2, ty - td//2, tx + td//2, ty + td//2],
                   fill=thumb_color, outline="#999999", width=s)

        sw = sw.resize((self._cw, self._ch), Image.LANCZOS)
        sw_y = (h - self._ch) // 2
        img.paste(sw, (self._hpad, sw_y))

        self._hazard_img = ImageTk.PhotoImage(img)
        self.hazard_canvas.delete("all")
        self.hazard_canvas.create_image(0, 0, image=self._hazard_img, anchor="nw")

        arm_x = self._hpad + self._cw + self._hpad * 2
        arm_y = h // 2
        font  = ("Helvetica", 20, "bold")
        text_id = self.hazard_canvas.create_text(
            arm_x, arm_y, text="ARM", font=font, fill="white", anchor="w",
        )
        bx1, _by1, bx2, _by2 = self.hazard_canvas.bbox(text_id)
        self.hazard_canvas.create_rectangle(
            bx1 - self._hpad, sw_y, bx2 + self._hpad, sw_y + self._ch,
            fill="black", outline="",
        )
        self.hazard_canvas.tag_raise(text_id)

    def _toggle_arm(self):
        self.armed.set(not self.armed.get())
        self.update_status(configured=self._configured)

    def get_armed(self):
        return self.armed.get()

    def enable_arming(self):
        self._configured = True
        self.update_status(configured=True)

    def disable_arming(self):
        self.update_status(configured=self._configured)

    def set_run_status(self, status, configured=True):
        self._configured = configured
        self.running = status
        self.update_status(configured=configured)

    def update_status(self, configured=True):
        if self.running:
            self.status_label.config(
                text="Running",
                foreground="white",
                background="red"
            )
        elif self.armed.get() and configured:
            self.status_label.config(
                text="Armed",
                foreground="white",
                background="orange"
            )
        elif configured:
            self.status_label.config(
                text="Disarmed",
                foreground="white",
                background="green"
            )
        else:
            self.armed.set(False)
            self.status_label.config(
                text="Not configured",
                foreground="white",
                background="gray"
            )
        self._draw_hazard()
