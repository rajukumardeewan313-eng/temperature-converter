import tkinter as tk
from tkinter import ttk

# ── Conversion logic ──────────────────────────────────────────
def to_celsius(value, unit):
    if unit == "C": return value
    if unit == "F": return (value - 32) * 5 / 9
    if unit == "K": return value - 273.15
    if unit == "R": return (value - 491.67) * 5 / 9

def from_celsius(c, unit):
    if unit == "C": return c
    if unit == "F": return c * 9 / 5 + 32
    if unit == "K": return c + 273.15
    if unit == "R": return (c + 273.15) * 9 / 5

def fmt(n):
    if not isinstance(n, float): return "—"
    if abs(n) >= 10000: return f"{n:,.0f}"
    if abs(n) >= 100:   return f"{n:.2f}".rstrip("0").rstrip(".")
    return f"{n:.4f}".rstrip("0").rstrip(".")

def get_fact(c):
    if c < -273.15:         return "⚠️",  "Below absolute zero — physically impossible!"
    if abs(c+273.15) < 0.5: return "🔵", "Absolute zero — coldest possible temperature in the universe."
    if c < -89:             return "🥶", "Colder than Earth's record low (−89.2°C, Antarctica 1983)."
    if c < -40:             return "❄️",  "Extremely frigid — exposed skin freezes in minutes."
    if c < 0:               return "🧊", "Below freezing point of water. Ice forms here."
    if abs(c) < 0.5:        return "🧊", "Freezing point of water (0°C / 32°F / 273.15 K)."
    if c < 15:              return "🌬️", "Cool and brisk — grab a jacket!"
    if c < 25:              return "😊", "Comfortable room temperature. Most people love it here."
    if c < 37:              return "☀️",  "Warm — a hot summer day in most of the world."
    if abs(c-37) < 0.5:     return "🤒", "Normal human body temperature (37°C / 98.6°F)."
    if c < 60:              return "🥵", "Dangerously hot — heat exhaustion risk."
    if abs(c-100) < 0.5:    return "♨️",  "Boiling point of water at sea level (100°C / 212°F)."
    if c < 250:             return "🔥", "Scorching hot — above water's boiling point."
    if c < 1000:            return "🌋", "Lava territory! Molten rock flows here."
    if c < 5778:            return "🌟", "Stellar hot — tungsten melts at 3422°C."
    return "☀️", "Around or above the surface temperature of the Sun!"

# ── Palette ───────────────────────────────────────────────────
BG       = "#0f0f1a"
SURFACE  = "#1a1a2e"
SURFACE2 = "#22223b"
BORDER   = "#2a2a4a"
TEXT     = "#f0f0ff"
MUTED    = "#8888aa"

UNIT_COLORS = {
    "C": {"bg": "#0d2137", "fg": "#60a5fa", "accent": "#60a5fa"},
    "F": {"bg": "#2a1010", "fg": "#f87171", "accent": "#f87171"},
    "K": {"bg": "#1e1337", "fg": "#a78bfa", "accent": "#a78bfa"},
    "R": {"bg": "#2a1f00", "fg": "#fbbf24", "accent": "#fbbf24"},
}
UNIT_ICONS = {"C": "🌡️", "F": "🇺🇸", "K": "⚛️",  "R": "🔬"}
UNIT_NAMES = {"C": "Celsius", "F": "Fahrenheit", "K": "Kelvin", "R": "Rankine"}
UNIT_SYMS  = {"C": "°C",      "F": "°F",         "K": "K",      "R": "°R"}

PRESETS = [
    ("🔵 Absolute Zero", -273.15, "C"),
    ("🧊 Water Freezes",  0,      "C"),
    ("🤒 Body Temp",      37,     "C"),
    ("♨️ Water Boils",   100,    "C"),
    ("🍞 Oven (Bake)",   180,    "C"),
    ("☀️ Sun Surface",  5778,   "C"),
]

# ── App ───────────────────────────────────────────────────────
class TempConverter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🌡️ Temperature Converter")
        self.configure(bg=BG)

        # ── Window: start maximized, allow resize & min/max ──
        self.resizable(True, True)
        self.state("zoomed")          # maximized on Windows/Linux
        try:
            self.attributes("-zoomed", True)   # maximized on some Linux WMs
        except Exception:
            pass

        # minimum size so layout never breaks
        self.minsize(600, 650)

        self.selected_unit = tk.StringVar(value="C")
        self.input_var     = tk.StringVar(value="100")
        self.input_var.trace_add("write", lambda *_: self._update())

        self._build_ui()
        self.bind("<Configure>", self._on_resize)
        self._update()

    # ── Build UI ──────────────────────────────────────────────
    def _build_ui(self):
        # Outer canvas + scrollbar so it works at any window size
        self.canvas = tk.Canvas(self, bg=BG, bd=0, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical",
                                      command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # inner frame inside canvas
        self.inner = tk.Frame(self.canvas, bg=BG)
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.inner, anchor="n"
        )
        self.inner.bind("<Configure>", self._on_inner_configure)
        self.canvas.bind("<Configure>",  self._on_canvas_configure)

        # mousewheel scroll
        self.canvas.bind_all("<MouseWheel>",
            lambda e: self.canvas.yview_scroll(-1*(e.delta//120), "units"))
        self.canvas.bind_all("<Button-4>",
            lambda e: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind_all("<Button-5>",
            lambda e: self.canvas.yview_scroll(1, "units"))

        self._fill_inner()

    def _fill_inner(self):
        f = self.inner   # shorthand

        # ── Header ──
        self.title_lbl = tk.Label(f, text="🌡️  Temperature Converter",
                  bg=BG, fg=TEXT, font=("Helvetica", 28, "bold"))
        self.title_lbl.pack(pady=(36, 4))

        tk.Label(f, text="Convert across  Celsius · Fahrenheit · Kelvin · Rankine",
                 bg=BG, fg=MUTED, font=("Helvetica", 13)).pack(pady=(0, 28))

        # ── Center column ──
        self.col = tk.Frame(f, bg=BG)
        self.col.pack(fill="both", expand=True, padx=40)

        # ── Input row ──
        input_frame = tk.Frame(self.col, bg=SURFACE,
                               highlightbackground=BORDER, highlightthickness=1)
        input_frame.pack(fill="x", pady=(0, 18))

        self.entry = tk.Entry(input_frame, textvariable=self.input_var,
                              bg=SURFACE, fg=TEXT, insertbackground=TEXT,
                              font=("Helvetica", 34, "bold"),
                              bd=0, highlightthickness=0, width=10,
                              justify="center")
        self.entry.pack(side="left", padx=18, pady=18)

        tk.Frame(input_frame, bg=BORDER, width=1).pack(
            side="left", fill="y", pady=10)

        btn_frame = tk.Frame(input_frame, bg=SURFACE)
        btn_frame.pack(side="left", fill="both", expand=True)

        for u in ["C", "F", "K", "R"]:
            c = UNIT_COLORS[u]
            tk.Radiobutton(btn_frame,
                text=f"{UNIT_ICONS[u]}  {u}",
                variable=self.selected_unit, value=u,
                bg=SURFACE, fg=c["fg"], selectcolor=c["bg"],
                activebackground=SURFACE, activeforeground=c["fg"],
                font=("Helvetica", 13, "bold"),
                indicatoron=False, bd=0, padx=12, pady=10,
                cursor="hand2", relief="flat",
                command=self._update
            ).pack(side="left", expand=True, fill="both")

        # ── Presets ──
        tk.Label(self.col, text="QUICK PRESETS", bg=BG, fg=MUTED,
                 font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(0, 8))

        preset_frame = tk.Frame(self.col, bg=BG)
        preset_frame.pack(fill="x", pady=(0, 18))

        for i, (label, val, unit) in enumerate(PRESETS):
            r, ci = divmod(i, 3)
            tk.Button(preset_frame, text=label,
                bg=SURFACE2, fg=TEXT,
                activebackground=BORDER, activeforeground=TEXT,
                font=("Helvetica", 11), bd=0, padx=12, pady=9,
                cursor="hand2", relief="flat",
                command=lambda v=val, u=unit: self._set_preset(v, u)
            ).grid(row=r, column=ci, padx=5, pady=4, sticky="ew")
            preset_frame.columnconfigure(ci, weight=1)

        # ── Result cards ──
        tk.Label(self.col, text="RESULTS", bg=BG, fg=MUTED,
                 font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(0, 8))

        cards_frame = tk.Frame(self.col, bg=BG)
        cards_frame.pack(fill="x", pady=(0, 18))
        self.card_frames = {}
        self.card_vals   = {}

        for i, u in enumerate(["C", "F", "K", "R"]):
            c = UNIT_COLORS[u]
            r, ci = divmod(i, 2)
            outer = tk.Frame(cards_frame, bg=c["bg"],
                             highlightbackground=c["accent"], highlightthickness=1)
            outer.grid(row=r, column=ci, padx=6, pady=6, sticky="nsew")
            cards_frame.columnconfigure(ci, weight=1)

            tk.Label(outer, text=f"{UNIT_ICONS[u]}   {UNIT_NAMES[u]}",
                     bg=c["bg"], fg=c["fg"],
                     font=("Helvetica", 13, "bold")).pack(anchor="w", padx=16, pady=(14,2))

            vl = tk.Label(outer, text="—", bg=c["bg"], fg=TEXT,
                          font=("Helvetica", 30, "bold"), anchor="w")
            vl.pack(anchor="w", padx=16, pady=(0,2))
            self.card_vals[u] = vl

            tk.Label(outer, text=UNIT_SYMS[u], bg=c["bg"], fg=c["fg"],
                     font=("Helvetica", 11)).pack(anchor="w", padx=16, pady=(0,14))
            self.card_frames[u] = outer

        # ── Thermometer bar ──
        tk.Label(self.col, text="SCALE POSITION  (−50 °C  →  150 °C)",
                 bg=BG, fg=MUTED, font=("Helvetica", 10, "bold")).pack(
                 anchor="w", pady=(0, 6))

        bar_outer = tk.Frame(self.col, bg=SURFACE2, height=16,
                             highlightbackground=BORDER, highlightthickness=1)
        bar_outer.pack(fill="x", pady=(0, 4))
        bar_outer.pack_propagate(False)

        self.bar_fill = tk.Frame(bar_outer, bg="#60a5fa", height=16)
        self.bar_fill.place(x=0, y=0, relheight=1, relwidth=0)

        tick_frame = tk.Frame(self.col, bg=BG)
        tick_frame.pack(fill="x", pady=(0, 18))
        for t in ["−50°C", "0°C", "50°C", "100°C", "150°C"]:
            tk.Label(tick_frame, text=t, bg=BG, fg=MUTED,
                     font=("Helvetica", 9)).pack(side="left", expand=True)

        # ── Fact banner ──
        fact_frame = tk.Frame(self.col, bg=SURFACE2,
                              highlightbackground=BORDER, highlightthickness=1)
        fact_frame.pack(fill="x", pady=(0, 18))

        self.fact_emoji_lbl = tk.Label(fact_frame, text="ℹ️",
                                       bg=SURFACE2, font=("Helvetica", 26))
        self.fact_emoji_lbl.pack(side="left", padx=(16, 8), pady=16)

        self.fact_text_lbl = tk.Label(fact_frame,
                                      text="Enter a temperature to see a fun fact.",
                                      bg=SURFACE2, fg=MUTED,
                                      font=("Helvetica", 12),
                                      wraplength=600, justify="left")
        self.fact_text_lbl.pack(side="left", pady=16, padx=(0, 16))

        # ── Formulas ──
        tk.Label(self.col, text="CONVERSION FORMULAS", bg=BG, fg=MUTED,
                 font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(0, 8))

        form_frame = tk.Frame(self.col, bg=BG)
        form_frame.pack(fill="x", pady=(0, 36))

        formulas = [
            ("°C → °F", "F = C × 9/5 + 32"),
            ("°F → °C", "C = (F − 32) × 5/9"),
            ("°C → K",  "K = C + 273.15"),
            ("K → °R",  "R = K × 9/5"),
        ]
        for i, (lbl, expr) in enumerate(formulas):
            r, ci = divmod(i, 2)
            ff = tk.Frame(form_frame, bg=SURFACE2,
                          highlightbackground=BORDER, highlightthickness=1)
            ff.grid(row=r, column=ci, padx=5, pady=5, sticky="ew")
            form_frame.columnconfigure(ci, weight=1)
            tk.Label(ff, text=lbl, bg=SURFACE2, fg=MUTED,
                     font=("Helvetica", 10)).pack(anchor="w", padx=14, pady=(10,2))
            tk.Label(ff, text=expr, bg=SURFACE2, fg=TEXT,
                     font=("Helvetica", 12, "bold")).pack(anchor="w", padx=14, pady=(0,10))

    # ── Canvas / resize helpers ───────────────────────────────
    def _on_inner_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event=None):
        w = self.canvas.winfo_width()
        self.canvas.itemconfig(self.canvas_window, width=w)
        # keep fact label wraplength responsive
        try:
            self.fact_text_lbl.config(wraplength=max(300, w - 160))
        except Exception:
            pass

    def _on_resize(self, event=None):
        self._on_canvas_configure()

    # ── Logic ─────────────────────────────────────────────────
    def _set_preset(self, val, unit):
        self.selected_unit.set(unit)
        self.input_var.set(str(val))
        self._update()

    def _update(self):
        raw_str = self.input_var.get().strip()
        unit    = self.selected_unit.get()
        try:
            raw = float(raw_str)
        except ValueError:
            for u in ["C", "F", "K", "R"]:
                self.card_vals[u].config(text="—")
            self.fact_text_lbl.config(text="Enter a valid number.")
            return

        celsius = to_celsius(raw, unit)

        for u in ["C", "F", "K", "R"]:
            self.card_vals[u].config(text=fmt(from_celsius(celsius, u)))
            c  = UNIT_COLORS[u]
            hl = "#ffffff" if u == unit else c["accent"]
            self.card_frames[u].config(highlightbackground=hl,
                                       highlightthickness=3 if u == unit else 1)

        MIN, MAX = -50, 150
        pct = max(0.0, min(1.0, (celsius - MIN) / (MAX - MIN)))
        self.bar_fill.place(relwidth=pct)
        clr = ("#60a5fa" if pct < 0.2 else
               "#34d399" if pct < 0.45 else
               "#fbbf24" if pct < 0.7  else "#f87171")
        self.bar_fill.config(bg=clr)

        emoji, text = get_fact(celsius)
        self.fact_emoji_lbl.config(text=emoji)
        self.fact_text_lbl.config(text=text)


if __name__ == "__main__":
    app = TempConverter()
    app.mainloop()
