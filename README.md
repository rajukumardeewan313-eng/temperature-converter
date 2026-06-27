# 🌡️ Temperature Converter

> **Python + Tkinter** — Real-time temperature conversion with a beautiful dark UI
> Single file · No extra libraries · Windows / macOS / Linux

---

## 📌 Project Overview

A Python Desktop Application that converts temperatures across **4 units** in real-time.
As you type, all results update instantly — no button press needed.

---

## ⚙️ Requirements

| Requirement | Version | Note |
|---|---|---|
| Python | 3.x (3.8+ recommended) | Download from python.org |
| Tkinter | Built-in | No separate install needed |

> ⚠️ **Linux users only:**
> ```bash
> sudo apt install python3-tk
> ```

---

## ▶️ How to Run

```bash
python temperature_converter.py
```

- App opens **fullscreen maximized** (`self.state("zoomed")`)
- **Minimize / Maximize / Restore** — all three title bar buttons work
- Window is **freely resizable** (`self.resizable(True, True)`)
- **Minimum size** is 600×650 — layout never breaks
- **Mouse wheel scroll** works on smaller windows

---

## ✨ Features

| Feature | Detail |
|---|---|
| 🔄 Live Conversion | `trace_add("write")` updates results as you type |
| 🌡️ 4 Temperature Units | Celsius · Fahrenheit · Kelvin · Rankine |
| 🎨 Colorful Result Cards | Blue · Red · Purple · Amber per unit |
| ⚡ 6 Quick Presets | Absolute Zero to Sun Surface |
| 📊 Animated Color Bar | Blue → Green → Yellow → Red |
| 💡 Smart Fun Facts | 15+ emoji facts that auto-update |
| 📐 Formula Reference | All 4 conversion formulas on screen |
| 🖥️ Fullscreen + Resizable | `zoomed` state, `minsize(600, 650)` |
| 📜 Scrollable Canvas | Canvas + Scrollbar for any window size |
| 🖱️ Mouse Wheel Support | `<MouseWheel>` `<Button-4>` `<Button-5>` bound |

---

## 🔢 Conversion Formulas

```
°C  →  °F  :   F = C × 9/5 + 32
°F  →  °C  :   C = (F − 32) × 5/9
°C  →  K   :   K = C + 273.15
K   →  °C  :   C = K − 273.15
°C  →  °R  :   R = (C + 273.15) × 9/5
°R  →  °C  :   C = (R − 491.67) × 5/9
```

> 💡 **Code Trick:** `to_celsius()` first converts any unit to Celsius,
> then `from_celsius()` converts from Celsius to any target unit — a "bridge" approach.

---

## 🎨 Color Theme

| Unit | Color | Hex |
|---|---|---|
| 🌡️ Celsius | Blue | `#60a5fa` |
| 🇺🇸 Fahrenheit | Red | `#f87171` |
| ⚛️ Kelvin | Purple | `#a78bfa` |
| 🔬 Rankine | Amber | `#fbbf24` |

**Dark background palette used in code:**

```python
BG       = "#0f0f1a"   # Main background
SURFACE  = "#1a1a2e"   # Input row
SURFACE2 = "#22223b"   # Presets, fact banner, formulas
BORDER   = "#2a2a4a"   # All borders
TEXT     = "#f0f0ff"   # Primary text
MUTED    = "#8888aa"   # Labels and hints
```

---

## ⚡ Quick Presets

| Button | Value | Description |
|---|---|---|
| 🔵 Absolute Zero | −273.15°C | Coldest possible temperature in the universe |
| 🧊 Water Freezes | 0°C | Freezing point of water at sea level |
| 🤒 Body Temp | 37°C | Normal human body temperature |
| ♨️ Water Boils | 100°C | Boiling point of water at sea level |
| 🍞 Oven (Bake) | 180°C | Standard baking temperature |
| ☀️ Sun Surface | 5778°C | Surface temperature of the Sun |

---

## 🗂️ Code Structure

```
temperature_converter.py
│
├── FUNCTIONS
│   ├── to_celsius(value, unit)
│   │       Converts any unit → Celsius
│   │       if/elif chain handles C, F, K, R
│   │
│   ├── from_celsius(c, unit)
│   │       Converts Celsius → any unit
│   │       if/elif chain handles C, F, K, R
│   │
│   ├── fmt(n)
│   │       Formats a number into a clean readable string
│   │       >= 10000 : commas  |  >= 100 : 2 decimals
│   │       < 100    : 4 decimals  |  trailing zeros removed
│   │
│   └── get_fact(c)
│           Takes Celsius value → returns (emoji, text) tuple
│           Covers 15+ temperature ranges
│           From −273°C (absolute zero) to 5778°C (Sun surface)
│
└── CLASS TempConverter(tk.Tk)
    │
    ├── __init__()
    │       Sets window title and background
    │       resizable(True, True) + state("zoomed") → fullscreen
    │       minsize(600, 650) → minimum window size
    │       StringVar: selected_unit="C", input_var="100"
    │       trace_add → calls _update() on every keystroke
    │
    ├── _build_ui()
    │       Creates Canvas + vertical Scrollbar
    │       Embeds inner Frame inside Canvas
    │       Binds MouseWheel events (Windows / Mac / Linux)
    │       Calls _fill_inner()
    │
    ├── _fill_inner()
    │       ── Header (title + subtitle labels)
    │       ── Input row (Entry + 4 Radiobuttons for units)
    │       ── Quick Presets (6 buttons in 2×3 grid)
    │       ── Result Cards (4 cards in 2×2 grid)
    │       ── Thermometer bar (Frame inside Frame, place())
    │       ── Tick labels (−50°C to 150°C)
    │       ── Fun fact banner (emoji label + text label)
    │       ── Formula grid (4 formulas in 2×2 grid)
    │
    ├── _on_inner_configure(event)
    │       Inner frame size changes → updates scrollregion
    │
    ├── _on_canvas_configure(event)
    │       Canvas resizes → matches inner frame width
    │       Also keeps wraplength responsive
    │
    ├── _on_resize(event)
    │       Window Configure event → calls _on_canvas_configure()
    │
    ├── _set_preset(val, unit)
    │       Preset button clicked → sets selected_unit + input_var
    │       trace_add automatically triggers _update()
    │
    └── _update()
            Parses input as float
            Calls to_celsius() → gets celsius value
            Loops through 4 units → updates each result card
            Highlights active unit card with white border (3px)
            Calculates bar pct → sets relwidth + color
            Calls get_fact() → updates emoji + text labels
```

---

## 🖥️ UI Layout

```
┌──────────────────────────────────────────────────────┐
│           🌡️  Temperature Converter                  │ ← Title (Helvetica 28 bold)
│   Convert across Celsius · Fahrenheit · Kelvin · °R  │ ← Subtitle
├──────────────────────────────────────────────────────┤
│  [    100         ] │ [🌡°C] [🇺🇸°F] [⚛K] [🔬°R]  │ ← Entry + Radiobuttons
├──────────────────────────────────────────────────────┤
│  [🔵 Zero] [🧊 Freeze] [🤒 Body]                    │
│  [♨️ Boil] [🍞 Oven  ] [☀️ Sun ]                   │ ← Presets (2 rows × 3 cols)
├─────────────────────┬────────────────────────────────┤
│  🌡️ Celsius         │  🇺🇸 Fahrenheit               │
│  100                │  212                          │ ← Result Cards (2×2 grid)
│  °C                 │  °F                           │
├─────────────────────┼────────────────────────────────┤
│  ⚛️  Kelvin         │  🔬 Rankine                   │
│  373.15             │  671.67                       │
│  K                  │  °R                           │
├──────────────────────────────────────────────────────┤
│  SCALE POSITION  (−50°C  →  150°C)                  │
│  [████████████████░░░░░]                            │ ← Color bar (place())
│  −50°C   0°C   50°C   100°C   150°C                │
├──────────────────────────────────────────────────────┤
│  ♨️   Boiling point of water at sea level...        │ ← Fun Fact banner
├─────────────────────┬────────────────────────────────┤
│  °C → °F            │  °F → °C                     │
│  F = C × 9/5 + 32   │  C = (F−32) × 5/9           │ ← Formulas (2×2 grid)
├─────────────────────┼────────────────────────────────┤
│  °C → K             │  K → °R                      │
│  K = C + 273.15     │  R = K × 9/5                 │
└─────────────────────┴────────────────────────────────┘
```

---

## 💡 Step-by-Step Example — Entering 100°C

```python
# User types "100", unit = "C"

raw = float("100")               # → 100.0

celsius = to_celsius(100, "C")   # → 100.0 (returns as-is)

from_celsius(100, "F")           # → 100 * 9/5 + 32   =  212.0   °F
from_celsius(100, "K")           # → 100 + 273.15      =  373.15   K
from_celsius(100, "R")           # → (100+273.15)*9/5  =  671.67  °R

# Thermometer bar:
MIN, MAX = -50, 150
pct = (100 - (-50)) / (150 - (-50))   # = 150/200 = 0.75 → 75% filled
# pct >= 0.7 → color = "#f87171" (red)

# Fun fact:
get_fact(100)   # abs(100 - 100) < 0.5 → True
# → ("♨️", "Boiling point of water at sea level (100°C / 212°F).")
```

---

## 🖱️ Controls

| Action | Result |
|---|---|
| Type in input field | Live conversion update |
| Click unit button (°C / °F / K / °R) | Switch unit + recalculate |
| Click preset button | Auto-sets input and unit |
| Mouse wheel / trackpad scroll | Scrolls the canvas |
| Drag window edge | Resize — layout adjusts automatically |
| Minimize button | Minimizes the window |
| Maximize button | Maximizes / restores the window |

---

## 🖥️ Platform Support

| OS | Status | Note |
|---|---|---|
| Windows 10 / 11 | ✅ Works | Direct run |
| macOS 12+ | ✅ Works | Direct run |
| Ubuntu / Debian | ✅ Works | `sudo apt install python3-tk` |
| Other Linux | ✅ Works | Install tkinter via package manager |

---

## 📚 Beginner Learning Order

If you are learning Python, follow this order:

```
1️⃣  fmt()              →  f-strings, rstrip, number formatting
2️⃣  to_celsius()       →  if/elif chain, return values
    from_celsius()
3️⃣  get_fact()         →  Multiple conditions, tuple return
4️⃣  __init__()         →  Class, super(), StringVar, trace_add
5️⃣  _fill_inner()      →  Tkinter widgets:
                           Label, Entry, Button, Radiobutton,
                           Frame, pack(), grid(), place()
6️⃣  _build_ui()        →  Canvas, Scrollbar, create_window,
                           event binding
7️⃣  _update()          →  Connecting everything — live UI updates
```

---

## 📁 File Structure

```
project/
│
├── temperature_converter.py    ← Full app (single file, ~220 lines)
└── README.md                   ← This file
```

---

*Made with Python 3 + Tkinter · Zero dependencies · ~220 lines* 🚀


## 📬 Contact

- 💼 **LinkedIn:** [linkedin.com/in/raju-kumar-ai](https://www.linkedin.com/in/raju-kumar-ai)
- 📧 **Gmail:** [rajukumardeewan313@gmail.com](mailto:rajukumardeewan313@gmail.com)
