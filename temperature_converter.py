import tkinter as tk
from tkinter import font as tkfont

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
    if c < -273.15: return "⚠️", "Below absolute zero — physically impossible!"
    if abs(c + 273.15) < 0.5: return "🔵", "Absolute zero — coldest possible temperature in the universe."
    if c < -89:  return "🥶", "Colder than Earth's record low (−89.2°C, Antarctica 1983)."
    if c < -40:  return "❄️", "Extremely frigid — exposed skin freezes in minutes."
    if c < 0:    return "🧊", "Below freezing point of water. Ice forms here."
    if abs(c) < 0.5: return "🧊", "Freezing point of water (0°C / 32°F / 273.15 K)."
    if c < 15:   return "🌬️", "Cool and brisk — grab a jacket!"
    if c < 25:   return "😊", "Comfortable room temperature. Most people love it here."
    if c < 37:   return "☀️", "Warm — a hot summer day in most of the world."
    if abs(c - 37) < 0.5: return "🤒", "Normal human body temperature (37°C / 98.6°F)."
    if c < 60:   return "🥵", "Dangerously hot — heat exhaustion risk."
    if abs(c - 100) < 0.5: return "♨️", "Boiling point of water at sea level (100°C / 212°F)."
    if c < 250:  return "🔥", "Scorching hot — above water's boiling point."
    if c < 1000: return "🌋", "Lava territory! Molten rock flows here."
    if c < 5778: return "🌟", "Stellar hot — tungsten melts at 3422°C."
    return "☀️", "Around or above the surface temperature of the Sun!"

# ── Color palette ─────────────────────────────────────────────
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

UNIT_ICONS = {"C": "🌡️", "F": "🇺🇸", "K": "⚛️", "R": "🔬"}
UNIT_NAMES = {"C": "Celsius", "F": "Fahrenheit", "K": "Kelvin", "R": "Rankine"}
UNIT_SYMS  = {"C": "°C", "F": "°F", "K": "K", "R": "°R"}

PRESETS = [
    ("🔵 Absolute Zero", -273.15, "C"),
    ("🧊 Water Freezes",  0,      "C"),
    ("🤒 Body Temp",      37,     "C"),
    ("♨️ Water Boils",   100,    "C"),
    ("🍞 Oven (Bake)",   180,    "C"),
    ("☀️ Sun Surface",  5778,   "C"),
]

# ── Main App ──────────────────────────────────────────────────
class TempConverter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🌡️ Temperature Converter")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.geometry("580x750")

        self.selected_unit = tk.StringVar(value="C")
        self.input_var = tk.StringVar(value="100")
        self.input_var.trace_add("write", lambda *_: self.update())

        self._build_ui()
        self.update()

    def _build_ui(self):
        pad = dict(padx=20, pady=0)

        # ── Title ──
        tk.Label(self, text="🌡️ Temperature Converter",
                 bg=BG, fg=TEXT,
                 font=("Helvetica", 20, "bold")).pack(pady=(22, 2))
        tk.Label(self, text="Convert across Celsius · Fahrenheit · Kelvin · Rankine",
                 bg=BG, fg=MUTED, font=("Helvetica", 10)).pack(pady=(0, 18))

        # ── Input row ──
        input_frame = tk.Frame(self, bg=SURFACE, bd=0, highlightbackground=BORDER,
                                highlightthickness=1)
        input_frame.pack(fill="x", padx=20, pady=(0, 14))

        self.entry = tk.Entry(input_frame, textvariable=self.input_var,
                              bg=SURFACE, fg=TEXT, insertbackground=TEXT,
                              font=("Helvetica", 26, "bold"),
                              bd=0, highlightthickness=0, width=12,
                              justify="center")
        self.entry.pack(side="left", padx=14, pady=14)

        sep = tk.Frame(input_frame, bg=BORDER, width=1)
        sep.pack(side="left", fill="y", pady=8)

        btn_frame = tk.Frame(input_frame, bg=SURFACE)
        btn_frame.pack(side="left", fill="both", expand=True)

        for u in ["C", "F", "K", "R"]:
            c = UNIT_COLORS[u]
            b = tk.Radiobutton(btn_frame, text=f"{UNIT_ICONS[u]} {u}",
                               variable=self.selected_unit, value=u,
                               bg=SURFACE, fg=c["fg"], selectcolor=c["bg"],
                               activebackground=SURFACE, activeforeground=c["fg"],
                               font=("Helvetica", 10, "bold"),
                               indicatoron=False, bd=0, padx=8, pady=6,
                               cursor="hand2", relief="flat",
                               command=self.update)
            b.pack(side="left", expand=True, fill="both")

        # ── Presets ──
        tk.Label(self, text="QUICK PRESETS", bg=BG, fg=MUTED,
                 font=("Helvetica", 9, "bold")).pack(anchor="w", padx=22, pady=(0, 6))

        preset_frame = tk.Frame(self, bg=BG)
        preset_frame.pack(fill="x", padx=18, pady=(0, 14))

        for i, (label, val, unit) in enumerate(PRESETS):
            r, c_idx = divmod(i, 3)
            btn = tk.Button(preset_frame, text=label,
                            bg=SURFACE2, fg=TEXT,
                            activebackground=BORDER, activeforeground=TEXT,
                            font=("Helvetica", 9), bd=0, padx=10, pady=6,
                            cursor="hand2", relief="flat",
                            command=lambda v=val, u=unit: self._set_preset(v, u))
            btn.grid(row=r, column=c_idx, padx=4, pady=3, sticky="ew")
            preset_frame.columnconfigure(c_idx, weight=1)

        # ── Result cards ──
        tk.Label(self, text="RESULTS", bg=BG, fg=MUTED,
                 font=("Helvetica", 9, "bold")).pack(anchor="w", padx=22, pady=(0, 6))

        cards_frame = tk.Frame(self, bg=BG)
        cards_frame.pack(fill="x", padx=18, pady=(0, 14))
        self.card_frames = {}
        self.card_vals   = {}
        self.card_labels  = {}

        for i, u in enumerate(["C", "F", "K", "R"]):
            c = UNIT_COLORS[u]
            r, col = divmod(i, 2)
            outer = tk.Frame(cards_frame, bg=c["bg"], bd=0,
                             highlightbackground=c["accent"], highlightthickness=1)
            outer.grid(row=r, column=col, padx=5, pady=5, sticky="nsew")
            cards_frame.columnconfigure(col, weight=1)

            tk.Label(outer, text=f"{UNIT_ICONS[u]}  {UNIT_NAMES[u]}",
                     bg=c["bg"], fg=c["fg"],
                     font=("Helvetica", 10, "bold")).pack(anchor="w", padx=12, pady=(10, 2))

            val_lbl = tk.Label(outer, text="—",
                               bg=c["bg"], fg=TEXT,
                               font=("Helvetica", 22, "bold"), anchor="w")
            val_lbl.pack(anchor="w", padx=12, pady=(0, 2))
            self.card_vals[u] = val_lbl

            sym_lbl = tk.Label(outer, text=UNIT_SYMS[u],
                               bg=c["bg"], fg=c["fg"],
                               font=("Helvetica", 9))
            sym_lbl.pack(anchor="w", padx=12, pady=(0, 10))
            self.card_frames[u] = outer

        # ── Thermometer bar ──
        tk.Label(self, text="SCALE POSITION  (−50°C → 150°C)",
                 bg=BG, fg=MUTED, font=("Helvetica", 9, "bold")).pack(anchor="w", padx=22, pady=(0, 4))

        bar_outer = tk.Frame(self, bg=SURFACE2, height=12, bd=0,
                             highlightbackground=BORDER, highlightthickness=1)
        bar_outer.pack(fill="x", padx=20, pady=(0, 4))
        bar_outer.pack_propagate(False)

        self.bar_fill = tk.Frame(bar_outer, bg="#60a5fa", height=12)
        self.bar_fill.place(x=0, y=0, relheight=1, relwidth=0)

        tick_frame = tk.Frame(self, bg=BG)
        tick_frame.pack(fill="x", padx=20, pady=(0, 14))
        for t in ["−50°C", "0°C", "50°C", "100°C", "150°C"]:
            tk.Label(tick_frame, text=t, bg=BG, fg=MUTED,
                     font=("Helvetica", 8)).pack(side="left", expand=True)

        # ── Fact banner ──
        fact_frame = tk.Frame(self, bg=SURFACE2, bd=0,
                              highlightbackground=BORDER, highlightthickness=1)
        fact_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.fact_emoji_lbl = tk.Label(fact_frame, text="ℹ️",
                                       bg=SURFACE2, font=("Helvetica", 20))
        self.fact_emoji_lbl.pack(side="left", padx=(12, 6), pady=12)

        self.fact_text_lbl = tk.Label(fact_frame, text="Enter a temperature to see a fun fact.",
                                      bg=SURFACE2, fg=MUTED,
                                      font=("Helvetica", 10), wraplength=420, justify="left")
        self.fact_text_lbl.pack(side="left", pady=12, padx=(0, 12))

    def _set_preset(self, val, unit):
        self.selected_unit.set(unit)
        self.input_var.set(str(val))
        self.update()

    def update(self):
        raw_str = self.input_var.get().strip()
        unit = self.selected_unit.get()
        try:
            raw = float(raw_str)
        except ValueError:
            for u in ["C", "F", "K", "R"]:
                self.card_vals[u].config(text="—")
            self.fact_text_lbl.config(text="Enter a valid number.")
            return

        celsius = to_celsius(raw, unit)

        for u in ["C", "F", "K", "R"]:
            val = from_celsius(celsius, u)
            self.card_vals[u].config(text=fmt(val))
            c = UNIT_COLORS[u]
            hl = "#ffffff" if u == unit else c["accent"]
            self.card_frames[u].config(highlightbackground=hl,
                                       highlightthickness=2 if u == unit else 1)

        # Bar
        MIN, MAX = -50, 150
        pct = max(0.0, min(1.0, (celsius - MIN) / (MAX - MIN)))
        self.bar_fill.place(relwidth=pct)
        if pct < 0.2:   clr = "#60a5fa"
        elif pct < 0.45: clr = "#34d399"
        elif pct < 0.7:  clr = "#fbbf24"
        else:            clr = "#f87171"
        self.bar_fill.config(bg=clr)

        # Fact
        emoji, text = get_fact(celsius)
        self.fact_emoji_lbl.config(text=emoji)
        self.fact_text_lbl.config(text=text)


if __name__ == "__main__":
    app = TempConverter()
    app.mainloop()
