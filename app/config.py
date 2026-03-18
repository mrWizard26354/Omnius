"""
OMNIUS Terminal Configuration
OmniTech Systems Division
"""

import os

# ─── Display ──────────────────────────────────────────────────────────────────
SCREEN_WIDTH  = 1280
SCREEN_HEIGHT = 800
FPS           = 60
FULLSCREEN    = False   # Set True for Raspberry Pi kiosk mode

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR   = os.path.join(BASE_DIR, "assets")
FONTS_DIR    = os.path.join(ASSETS_DIR, "fonts")
SOUNDS_DIR   = os.path.join(ASSETS_DIR, "sounds")
CARD_PROFILES = os.path.join(ASSETS_DIR, "card_profiles.json")

# ─── Timing ───────────────────────────────────────────────────────────────────
TYPEWRITER_DELAY   = 0.03   # seconds per character
BOOT_LINE_PAUSE    = 0.4    # pause between boot lines
AUTH_STEP_DELAY    = 0.6    # delay between auth steps
CURSOR_BLINK_RATE  = 0.55   # seconds per blink cycle
SCANLINE_ALPHA     = 80     # 0-255 opacity of scanline overlay
FLICKER_CHANCE     = 0.002  # probability per frame of screen flicker

# ─── OMNIUS Node ──────────────────────────────────────────────────────────────
NODE_ID = "OMNIUS-03"

# ─── Color Palettes ───────────────────────────────────────────────────────────

# Master OMNIUS palette (cyberpunk)
OMNIUS = {
    "bg":           (5,   0,  15),
    "logo":         (240,  20, 185),   # hot pink — matches CRT phosphor
    "accent":       (0,  200, 230),   # electric cyan — vivid
    "text":         (155, 155, 175),  # soft white
    "dim":          (70,   70,  90),
    "pink":         (220,  25, 160),  # hot pink underline
    "warning":      (195, 148,   0),  # amber — warm and punchy
    "ok":           (0,   205,  95),  # green — vivid
    "error":        (220,  35,  35),
    "header_line":  (140,   0, 100),  # hot pink tint header line
    "footer_bg":    (10,    5,  25),
    "cursor":       (240,  20, 185),
}

# Per-subsystem palettes
PALETTES = {
    "ghostbusters": {
        "bg":      (0,   10,  20),
        "primary": (0,  210, 230),   # cyan
        "accent":  (200, 230, 255),  # ghost blue
        "text":    (180, 210, 220),
        "warning": (255, 210,  50),
        "ok":      (0,  255, 120),
        "error":   (255,  50,  50),
        "dim":     (60,  80,  90),
    },
    "ingen": {
        "bg":      (5,   10,   0),
        "primary": (180, 140,  0),   # amber
        "accent":  (60,  200,  60),  # green
        "text":    (200, 200, 160),
        "warning": (255, 100,  20),
        "ok":      (60,  200,  60),
        "error":   (255,  50,  50),
        "dim":     (60,   70,  40),
    },
    "skynet": {
        "bg":      (10,   0,   0),
        "primary": (220,  40,  40),  # red
        "accent":  (120, 140, 160),  # steel blue
        "text":    (200, 180, 180),
        "warning": (255, 100,   0),
        "ok":      (100, 200, 100),
        "error":   (255,  30,  30),
        "dim":     (80,   50,  50),
    },
    "zion": {
        "bg":      (0,   10,   0),
        "primary": (0,  220,  60),   # matrix green
        "accent":  (0,  180,  40),
        "text":    (160, 200, 160),
        "warning": (200, 200,  50),
        "ok":      (0,  255, 100),
        "error":   (255,  60,  60),
        "dim":     (30,   60,  30),
    },
    "umbrella": {
        "bg":      (10,   0,   0),
        "primary": (220,  30,  30),  # red
        "accent":  (220, 220, 220),  # clinical white
        "text":    (210, 210, 210),
        "warning": (255, 100,   0),
        "ok":      (80,  210, 120),
        "error":   (255,  20,  20),
        "dim":     (80,   60,  60),
    },
    "tron": {
        "bg":      (0,    5,  20),
        "primary": (0,  200, 255),   # cyan/blue
        "accent":  (180, 220, 255),
        "text":    (160, 210, 240),
        "warning": (255, 180,   0),
        "ok":      (0,  255, 200),
        "error":   (255,  60,  80),
        "dim":     (30,   60,  90),
    },
    "wopr": {
        "bg":      (0,    0,  10),
        "primary": (0,  160, 255),   # cold blue
        "accent":  (0,  220, 255),
        "text":    (160, 190, 220),
        "warning": (255, 200,   0),
        "ok":      (60,  220, 100),
        "error":   (255,  40,  40),
        "dim":     (40,   60,  80),
    },
    "event_horizon": {
        "bg":      (5,    0,   5),
        "primary": (180,  60, 180),  # dark magenta / horror violet
        "accent":  (220, 160, 220),
        "text":    (190, 170, 190),
        "warning": (255,  80,  20),
        "ok":      (100, 200, 140),
        "error":   (255,  20,  20),
        "dim":     (70,   40,  70),
    },
    "blade_runner": {
        "bg":      (5,    3,   0),
        "primary": (220, 140,  20),  # amber/neon
        "accent":  (255, 180,  60),
        "text":    (200, 180, 140),
        "warning": (255,  80,   0),
        "ok":      (100, 200, 100),
        "error":   (255,  40,  20),
        "dim":     (80,   60,  30),
    },
    "precrime": {
        "bg":      (0,    5,  15),
        "primary": (60,  160, 255),  # cool blue
        "accent":  (140, 200, 255),
        "text":    (160, 190, 220),
        "warning": (255, 160,  20),
        "ok":      (60,  220, 160),
        "error":   (255,  40,  40),
        "dim":     (40,   70,  100),
    },
}

# ─── Controls ─────────────────────────────────────────────────────────────────
KEY_UP     = "up"
KEY_DOWN   = "down"
KEY_ENTER  = "enter"
KEY_ESCAPE = "escape"
KEY_QUIT   = "q"
KEY_FULL   = "f11"
KEY_DEV    = "d"

# Dev-mode simulated card keys (number row)
SIM_CARD_KEYS = {
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "0": "0",
}

# ─── App States ───────────────────────────────────────────────────────────────
STATE_BOOT               = "BOOT"
STATE_WAITING_FOR_CARD   = "WAITING_FOR_CARD"
STATE_AUTHENTICATING     = "AUTHENTICATING"
STATE_MASTER_MENU        = "MASTER_MENU"
STATE_SUBSYSTEM          = "SUBSYSTEM"
STATE_ERROR              = "ERROR"

# ─── Subsystem registry ───────────────────────────────────────────────────────
# Maps system key -> (module_name, display_name, description, clearance, franchise)
SUBSYSTEMS = {
    "muthur": (
        "muthur",
        "MU/TH/UR 6000 OPERATIONS TERMINAL",
        "Weyland-Yutani shipboard AI command interface",
        "OMEGA",
        "ALIEN",
    ),
    "ghostbusters": (
        "ghostbusters",
        "CONTAINMENT AND COLLECTION INTERFACE",
        "Paranormal research & containment access",
        "TECHNICIAN",
        "GHOSTBUSTERS",
    ),
    "zion": (
        "zion",
        "ZION MAINFRAME",
        "Simulation anomaly monitoring node",
        "OPERATOR",
        "THE MATRIX",
    ),
    "umbrella": (
        "umbrella",
        "UMBRELLA BIOHAZARD RESEARCH NETWORK",
        "Biohazard research & containment division",
        "RESEARCH",
        "RESIDENT EVIL",
    ),
    "ingen": (
        "ingen",
        "INGEN PARK AND WILDLIFE CONTROL",
        "Genetic asset management network",
        "OPERATIONS",
        "JURASSIC PARK",
    ),
    "blade_runner": (
        "blade_runner",
        "OFF-WORLD DATA ARCHIVE",
        "Tyrell Corporation bioengineering database",
        "INVESTIGATOR",
        "BLADE RUNNER",
    ),
    "skynet": (
        "skynet",
        "SKYNET DEFENSE NETWORK",
        "Autonomous defense intelligence grid",
        "RESTRICTED",
        "THE TERMINATOR",
    ),
    "precrime": (
        "precrime",
        "PRECRIME POLICE DATABASE",
        "Predictive crime analysis terminal",
        "DETECTIVE",
        "MINORITY REPORT",
    ),
    "tron": (
        "tron",
        "ENCOM MCP GRID SYSTEM",
        "Digital environment management system",
        "USER",
        "TRON",
    ),
    "event_horizon": (
        "event_horizon",
        "U.S.A.C. SEARCH AND RESCUE LOGS",
        "Classified deep-space incident records",
        "CLASSIFIED",
        "EVENT HORIZON",
    ),
    "wopr": (
        "wopr",
        "WOPR STRATEGIC COMMAND",
        "Global defense simulation core",
        "RESTRICTED",
        "WARGAMES",
    ),
    "fnaf": (
        "fnaf",
        "FAZBEAR ENTERTAINMENT SECURITY SYSTEM",
        "Animatronic activity monitoring & incident logs",
        "TECHNICIAN",
        "FIVE NIGHTS AT FREDDY'S",
    ),
}

# Ordered list for master menu display
SUBSYSTEM_ORDER = [
    "muthur",
    "ghostbusters",
    "zion",
    "umbrella",
    "ingen",
    "blade_runner",
    "skynet",
    "precrime",
    "tron",
    "event_horizon",
    "wopr",
    "fnaf",
]

# Per-franchise name accent colours (used on both boot screen and master menu)
FRANCHISE_COLORS = {
    "ALIEN":           (30,  210,  80),   # green
    "GHOSTBUSTERS":    (40,  190, 255),   # bright blue
    "THE MATRIX":      (30,  210,  80),   # green
    "RESIDENT EVIL":   (220,  35,  35),   # red
    "JURASSIC PARK":   (195, 148,   0),   # amber
    "BLADE RUNNER":    (40,  190, 255),   # bright blue
    "THE TERMINATOR":  (220,  35,  35),   # red
    "MINORITY REPORT": (195, 148,   0),   # amber
    "TRON":            (40,  190, 255),   # bright blue
    "EVENT HORIZON":         (220,  35,  35),   # red
    "WARGAMES":              (195, 148,   0),   # amber
    "FIVE NIGHTS AT FREDDY'S": (30, 210,  80),  # green
}
