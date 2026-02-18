import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageDraw, ImageTk


class ArmSwitch:
    def __init__(self, parent, on_toggle=None):
        self.armed     = tk.BooleanVar(value=False)
        self._configured = False
        self._running    = False
        self._on_toggle  = on_toggle
        self._hazard_img = None  # prevent GC
        self._last_drawn = None  # skip redraw if state unchanged

        self._tw    = 50   # track width
        self._th    = 24   # track height
        self._pad   = 10   # canvas padding around track
        self._scale = 4    # supersampling factor
        self._hpad  = 12   # padding inside hazard zone

        cw = self._tw + self._pad * 2
        ch = self._th + self._pad * 2
        self._cw = cw
        self._ch = ch

        self.canvas = tk.Canvas(
            parent,
            height=ch + self._hpad * 2,
            highlightthickness=3,
            highlightbackground="#222222",
        )
        self.canvas.pack(side="top", fill="x", padx=10, pady=20)

        self.canvas.bind("<Configure>", lambda _e: self._draw())
        self.canvas.bind("<Button-1>",  self._on_click)
        self.canvas.bind("<Motion>",    self._on_motion)
        self.canvas.bind("<Leave>",     lambda _e: self._draw(hover=False))

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_armed(self):
        return self.armed.get()

    def reset_armed(self):
        self.armed.set(False)

    def enable_arming(self):
        self._configured = True
        self._draw()

    def disable_arming(self):
        self._draw()

    def set_run_status(self, running, configured):
        self._configured = configured
        self._running    = running
        self._draw()

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _toggle(self):
        self.armed.set(not self.armed.get())
        self._draw()
        if self._on_toggle:
            self._on_toggle()

    def _in_switch(self, x, y):
        h    = self.canvas.winfo_height()
        sw_y = (h - self._ch) // 2
        return (self._hpad <= x <= self._hpad + self._cw and
                sw_y <= y <= sw_y + self._ch)

    def _on_click(self, event):
        if self._in_switch(event.x, event.y) and self._configured and not self._running:
            self._toggle()

    def _on_motion(self, event):
        hover = self._in_switch(event.x, event.y)
        self.canvas.configure(
            cursor="hand2" if hover and self._configured and not self._running else "arrow"
        )
        self._draw(hover=hover)

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

    def _draw(self, hover=False):
        c = self.canvas
        w = c.winfo_width()
        h = c.winfo_height()
        if w < 2 or h < 2:
            return

        armed = self.armed.get()
        is_on = armed or self._running

        state = (is_on, self._configured, self._running, hover, w, h)
        if state == self._last_drawn:
            return
        self._last_drawn = state

        if not self._configured:
            track_color = "#555555"
            thumb_color = "#888888"
        elif self._running or armed:
            track_color = "#ff0000"
            thumb_color = "#ffffff"
        else:
            track_color = "#aaaaaa"
            thumb_color = "#ffffff"

        img = self._make_stripe_img(w, h)

        s  = self._scale
        tw = self._tw * s
        th = self._th * s
        p  = self._pad * s
        iw = self._cw * s
        ih = self._ch * s
        r  = th // 2

        sw = Image.new("RGB", (iw, ih), "#000000")
        sd = ImageDraw.Draw(sw)
        outline = "#888888" if (hover and self._configured and not self._running) else track_color
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
        c.delete("all")
        c.create_image(0, 0, image=self._hazard_img, anchor="nw")

        arm_x  = self._hpad + self._cw + self._hpad * 2
        arm_y  = h // 2
        font   = ("Helvetica", 20, "bold")
        text_id = c.create_text(arm_x, arm_y, text="ARM", font=font,
                                 fill="white", anchor="w")
        bx1, _by1, bx2, _by2 = c.bbox(text_id)
        c.create_rectangle(bx1 - self._hpad, sw_y,
                           bx2 + self._hpad, sw_y + self._ch,
                           fill="black", outline="")
        c.tag_raise(text_id)
