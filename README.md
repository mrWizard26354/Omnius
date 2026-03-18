# OMNIUS Terminal
### OmniTech Systems Division

A fullscreen retro-futuristic master terminal application. OMNIUS is the umbrella access system that authenticates users via RFID cards and routes them into a collection of fictional archive terminals from classic sci-fi films.

---

## System Overview

```
OMNIUS
└── Master Access Shell
    ├── Ghostbusters Archive Terminal
    ├── InGen Park Operations Database
    ├── Skynet Strategic Command
    ├── Zion Mainframe Access (The Matrix)
    ├── Umbrella Research Network (Resident Evil)
    ├── ENCOM Grid Terminal (Tron)
    ├── WOPR Strategic Command (WarGames)
    ├── Event Horizon Ship Archive
    ├── Replicant Registry (Blade Runner)
    ├── PreCrime Analysis Network (Minority Report)
    └── [Future: MU/TH/UR 6000 — Weyland-Yutani]
```

---

## Requirements

- Python 3.13+
- pygame 2.6+

Install dependencies:
```
pip install pygame
```

---

## Running OMNIUS

From inside the `omnius/` directory:
```
python main.py
```

Or from the parent directory:
```
python omnius/main.py
```

---

## Controls

| Key             | Action                              |
|-----------------|-------------------------------------|
| `1` – `9`, `0`  | Insert simulated card (dev mode)    |
| `↑` / `↓`       | Navigate menu                       |
| `Enter`         | Confirm selection                   |
| `Escape`        | Back / exit subsystem / logout      |
| `F11`           | Toggle fullscreen                   |
| `Ctrl+Q`        | Quit                                |

---

## Simulated Card Keys (Dev Mode)

| Key | Destination                        |
|-----|------------------------------------|
| `1` | Ghostbusters Archive Terminal      |
| `2` | InGen Park Operations Database     |
| `3` | Skynet Strategic Command           |
| `4` | Zion Mainframe (Matrix)            |
| `5` | Umbrella Research Network          |
| `6` | ENCOM Grid Terminal (Tron)         |
| `7` | WOPR Strategic Command (WarGames)  |
| `8` | Event Horizon Ship Archive         |
| `9` | Replicant Registry (Blade Runner)  |
| `0` | PreCrime Analysis Network          |

---

## Adding Real RFID Cards

1. Get the RFID UID of your card (use any RFID reader test utility)
2. Open `assets/card_profiles.json`
3. Add an entry matching your card's UID to one of the destinations:

```json
"YOUR-CARD-UID": {
    "label": "Ghostbusters Archive Terminal",
    "system": "ghostbusters",
    "access_level": "Technician",
    "node": "GB-01"
}
```

4. For USB HID RFID readers (keyboard-emulating): the reader types the card ID and presses Enter. You can integrate this into `app/card_input.py` by adding a text-input listener.

---

## Adding a New Subsystem

1. Create `systems/your_system.py` — inherit from `BaseSystem`:

```python
from systems.base_system import BaseSystem

class YourTerminal(BaseSystem):
    SYSTEM_TITLE    = "YOUR SYSTEM NAME"
    SYSTEM_SUBTITLE = "SUBTITLE LINE"
    NODE_LABEL      = "YS-01"

    def __init__(self, fonts, audio, crt, flicker, palette):
        super().__init__(fonts, audio, crt, flicker, palette)
        self._menu_entries = [
            ("MENU ITEM",  ["line 1", "line 2"]),
        ]
```

2. Add a palette to `app/config.py` in `PALETTES`
3. Register the system in `app/config.py` under `SUBSYSTEMS` and `SUBSYSTEM_ORDER`
4. Import and add to `SUBSYSTEM_MAP` in `main.py`
5. Add a card profile to `assets/card_profiles.json`

---

## Custom Fonts

Drop any `.ttf` or `.otf` retro monospace font into `assets/fonts/`. The renderer prefers fonts with "vt323", "terminus", "ibm", or "px" in the filename. Good choices:
- **VT323** (free — Google Fonts)
- **PxPlus IBM VGA8** (free — int10h.org)
- **Terminus** (free — terminus-font.sourceforge.net)

---

## Raspberry Pi Kiosk Mode

1. In `app/config.py`, set `FULLSCREEN = True`
2. Add to `/etc/xdg/autostart/omnius.desktop`:
```ini
[Desktop Entry]
Name=OMNIUS Terminal
Exec=python3 /home/pi/omnius/main.py
```
3. Or add to crontab:
```
@reboot python3 /home/pi/omnius/main.py
```

For a connected USB RFID reader, extend `app/card_input.py` to read from the device. Most USB HID readers emulate a keyboard — no driver needed.

---

## Hardware Build Notes

Designed to run inside a custom 3D-printed retro workstation case with:
- 10.1" HDMI LCD (1280×800)
- Raspberry Pi 5
- 60% mechanical keyboard
- USB RFID card reader (front panel slot)
- 2× 40mm speakers

Target case dimensions: 420mm W × 320mm D × 210mm H

---

## Project Structure

```
omnius/
├── main.py                  Entry point
├── app/
│   ├── config.py            All configuration, colors, timing
│   ├── state_manager.py     App state machine
│   ├── renderer.py          Font loading, drawing utilities
│   ├── effects.py           CRT scanlines, typewriter, cursor, glow
│   ├── input_manager.py     Keyboard / input abstraction
│   ├── card_input.py        Card authentication layer
│   └── audio.py             Procedural audio
├── systems/
│   ├── base_system.py       Base class all terminals inherit from
│   ├── boot_screen.py       OMNIUS boot screen
│   ├── auth_screen.py       Authorization sequence
│   ├── master_menu.py       Master index menu
│   ├── ghostbusters.py      Ghostbusters terminal
│   ├── ingen.py             InGen/Jurassic Park terminal
│   ├── skynet.py            Skynet terminal
│   ├── zion.py              Matrix/Zion terminal
│   ├── umbrella.py          Umbrella/Resident Evil terminal
│   ├── tron.py              ENCOM/Tron terminal
│   ├── wopr.py              WOPR/WarGames terminal
│   ├── event_horizon.py     Event Horizon terminal
│   ├── blade_runner.py      Blade Runner terminal
│   └── precrime.py          PreCrime/Minority Report terminal
├── assets/
│   ├── card_profiles.json   Card ID → destination mapping
│   ├── fonts/               Drop .ttf/.otf retro fonts here
│   └── sounds/              Optional audio files
└── README.md
```

---

## Future Terminals (Planned)

- **X-Files Case Archive** — FBI / Syndicate
- **Dune Archive** — Bene Gesserit / CHOAM

---

*OMNIUS — Operational Machine Network Intelligence Utility System*
*OmniTech Systems Division*
