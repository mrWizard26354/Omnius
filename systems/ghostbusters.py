"""
Ghostbusters Archive Terminal
"""
from systems.base_system import BaseSystem


class GhostbustersTerminal(BaseSystem):
    SYSTEM_TITLE    = "CONTAINMENT AND COLLECTION INTERFACE"
    SYSTEM_SUBTITLE = "PARANORMAL RESEARCH & CONTAINMENT ACCESS"
    NODE_LABEL      = "GB-01"

    def __init__(self, fonts, audio, crt, flicker, palette):
        super().__init__(fonts, audio, crt, flicker, palette)
        self._menu_entries = [
            ("CONTAINMENT GRID STATUS",       self._containment()),
            ("TOBIN'S SPIRIT GUIDE INDEX",    self._tobin()),
            ("ENTITY RECORDS DATABASE",       self._entities()),
            ("PKE SURGE LOGS",                self._pke()),
            ("FIELD REPORTS",                 self._reports()),
        ]

    def _containment(self):
        return [
            "=== CONTAINMENT GRID STATUS ===",
            "",
            "STATUS         : ONLINE",
            "GRID INTEGRITY : 98.4%",
            "POWER DRAW     : 14,200 kW",
            "OCCUPIED CELLS : 147 / 300",
            "LAST BREACH    : 1989-10-31  [RESOLVED]",
            "",
            "--- CELL INVENTORY ---",
            "",
            "CELL 001  : Class IV Full-Torso Vapour  [CONTAINED]",
            "CELL 014  : Slimer  [CONTAINED]",
            "CELL 023  : Library Ghost / Eleanor Twitty  [CONTAINED]",
            "CELL 044  : Sewer Dragon  [CONTAINED]",
            "CELL 067  : Vigo the Carpathian Possessor  [CONTAINED]",
            "CELL 099  : Class VII Destructor-Form  [CONTAINED]",
            "",
            "--- ALERT LOG ---",
            "",
            "> 1984-10-14: Grid breach. Zuul incursion. Gate event confirmed.",
            "> 1984-10-14: Destructor-Form manifested at 550 Central Park West.",
            "> 1984-10-14: Grid restored. 147 entities re-contained.",
            "> 1989-02-11: Mood slime surge detected below Broadway.",
            "",
            "STATUS: ALL SYSTEMS NOMINAL",
        ]

    def _tobin(self):
        return [
            "=== TOBIN'S SPIRIT GUIDE — DIGITAL INDEX ===",
            "",
            "ENTRIES     : 4,812",
            "LAST UPDATE : 1989-12-15",
            "",
            "--- CLASS BREAKDOWN ---",
            "",
            "Class I   — Residual haunt                    : 2,441 entries",
            "Class II  — Non-corporeal manifestation       : 812 entries",
            "Class III — Full-roaming vapour               : 644 entries",
            "Class IV  — Full-torso vapour                 : 381 entries",
            "Class V   — Ectoplasmic manifestation         : 222 entries",
            "Class VI  — Possessor entity                  : 184 entries",
            "Class VII — Destructor-form / ancient deity   : 128 entries",
            "",
            "--- NOTABLE ENTRIES ---",
            "",
            "Entry 0044  : Zuul, the Gatekeeper of Gozer",
            "             Origin: Sumerian period, circa 6000 BC",
            "             Affiliation: Gozer the Gozerian",
            "             Status: Destroyed / Re-contained",
            "",
            "Entry 0045  : Vinz Clortho, the Keymaster",
            "             Origin: Sumerian period",
            "             Last Seen: New York City, 1984",
            "",
            "Entry 0001  : Gozer the Gozerian",
            "             Also known as: Gozer the Destructor",
            "             Manifestation: Traveller",
            "             THREAT LEVEL: EXTREME",
            "             Status: Expelled — return probability HIGH",
        ]

    def _entities(self):
        return [
            "=== ENTITY RECORDS DATABASE ===",
            "",
            "TOTAL ENTITIES LOGGED     : 1,847",
            "ENTITIES CURRENTLY ACTIVE : 12",
            "ENTITIES CONTAINED        : 147",
            "ENTITIES NEUTRALISED      : 1,688",
            "",
            "--- ACTIVE ENTITIES (CURRENT) ---",
            "",
            "ID: E-1201  |  Class III  |  Location: Queens, NYC",
            "            |  Description: Blue iridescent vapour trail",
            "            |  Behaviour: Non-hostile",
            "",
            "ID: E-1205  |  Class IV   |  Location: Grand Central Terminal",
            "            |  Description: Full-torso male, Victorian dress",
            "            |  Behaviour: Hostile — avoid contact",
            "",
            "ID: E-1211  |  Class V    |  Location: Ellis Island",
            "            |  Description: Group entity, immigrant manifestation",
            "            |  Behaviour: Neutral / reactive",
            "",
            "--- RECOMMENDED EQUIPMENT ---",
            "",
            "> Proton Pack — particle accelerator / containment stream",
            "> Ghost Trap  — portable containment unit",
            "> PKE Meter   — psychokinetic energy detection",
            "> Slime Blower — mood slime dispenser (Mk II only)",
        ]

    def _pke(self):
        return [
            "=== PKE SURGE LOG — PSYCHOKINETIC ENERGY MONITOR ===",
            "",
            "MONITORING STATIONS : 22 (NYC Metro)",
            "BASELINE PKE LEVEL  : 7.2 milli-Roentgens",
            "",
            "--- RECENT READINGS ---",
            "",
            "2024-03-01 08:14  |  Station 04 (Midtown)  |  PKE: 8.1  |  NORMAL",
            "2024-03-01 14:02  |  Station 09 (Downtown) |  PKE: 12.4 |  ELEVATED",
            "2024-03-01 19:45  |  Station 09 (Downtown) |  PKE: 34.8 |  ALERT",
            "2024-03-02 00:01  |  Station 09 (Downtown) |  PKE: 7.9  |  NORMAL",
            "",
            "ALERT: Elevated PKE reading detected at Station 09.",
            "Dispatch recommended. Possible Class IV or greater manifestation.",
            "",
            "--- HISTORICAL PEAKS ---",
            "",
            "1984-10-14  550 Central Park West  |  PKE: 1,147.2  |  EXTREME",
            "            Note: Gate event. Gozer incursion.",
            "1989-12-31  New York City (wide)   |  PKE: 892.3    |  EXTREME",
            "            Note: Mood slime tidal surge.",
        ]

    def _reports(self):
        return [
            "=== FIELD REPORTS — GHOSTBUSTERS OPERATION LOG ===",
            "",
            "REPORT #0847",
            "DATE    : 2024-02-28",
            "TEAM    : Venkman, Stantz",
            "LOCATION: Grand Central Terminal, NYC",
            "ENTITY  : Class IV Full-Torso Vapour (male, 1880s)",
            "OUTCOME : Contained — Cell 144",
            "NOTES   : Subject became hostile when approached.",
            "          Full stream required. Minor property damage.",
            "",
            "---",
            "",
            "REPORT #0846",
            "DATE    : 2024-02-20",
            "TEAM    : Spengler, Zeddemore",
            "LOCATION: Brooklyn Public Library",
            "ENTITY  : Class I Residual (reading room)",
            "OUTCOME : Dispersed — no containment required",
            "NOTES   : Appeared to be former librarian.",
            "          No threat. Ambient PKE drop post-dispersal.",
            "",
            "---",
            "",
            "REPORT #0843",
            "DATE    : 2024-01-14",
            "TEAM    : Full team",
            "LOCATION: Central Park",
            "ENTITY  : Class VII — manifestation category undetermined",
            "OUTCOME : UNRESOLVED — investigation ongoing",
            "WARNING : Unknown entity — do not engage alone.",
        ]
