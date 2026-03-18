"""
PreCrime Analysis Network — Minority Report
"""
import random
from systems.base_system import BaseSystem


_NAMES = [
    "James Hartwell", "Susan Kowalski", "Michael Torres", "Elena Voss",
    "David Park", "Rachel Simmons", "Omar Khalil", "Anna Chen",
    "Frank Deluca", "Katherine Morse",
]
_LOCATIONS = [
    "Georgetown District", "Capitol Hill", "Navy Yard", "Adams Morgan",
    "Dupont Circle", "Foggy Bottom", "Bethesda", "Silver Spring",
]
_WEAPONS = ["firearm", "blunt instrument", "kitchen knife", "vehicle", "unknown"]
_MOTIVES = ["domestic dispute", "financial", "unknown", "jealousy", "contract"]


def _random_case():
    name   = random.choice(_NAMES)
    victim = random.choice([n for n in _NAMES if n != name])
    loc    = random.choice(_LOCATIONS)
    t      = f"{random.randint(10,23):02d}:{random.randint(0,59):02d}"
    w      = random.choice(_WEAPONS)
    m      = random.choice(_MOTIVES)
    cid    = random.randint(80000, 99999)
    return [
        f"CASE ID  : {cid}",
        f"SUSPECT  : {name}",
        f"VICTIM   : {victim}",
        f"LOCATION : {loc}",
        f"TIME     : {t}  (predicted — ±4 min)",
        f"WEAPON   : {w}",
        f"MOTIVE   : {m}",
        f"STATUS   : INTERVENTION REQUIRED",
    ]


class PreCrimeTerminal(BaseSystem):
    SYSTEM_TITLE    = "PRECRIME POLICE DATABASE"
    SYSTEM_SUBTITLE = "PREDICTIVE CRIME ANALYSIS TERMINAL"
    NODE_LABEL      = "PC-01"

    def __init__(self, fonts, audio, crt, flicker, palette):
        super().__init__(fonts, audio, crt, flicker, palette)
        self._menu_entries = [
            ("PREDICTED CRIMES",             self._predictions()),
            ("SUSPECT IDENTIFICATION",       self._suspects()),
            ("PRECOGNITIVE VISION ARCHIVE",  self._visions()),
            ("CITYWIDE SURVEILLANCE",        self._surveillance()),
            ("CASE RESOLUTION LOGS",         self._resolved()),
        ]

    def _predictions(self):
        lines = [
            "=== PREDICTED HOMICIDE EVENTS — NEXT 24 HRS ===",
            "",
            "PRECOG AGREEMENT   : 3 of 3  (MAJORITY REPORT)",
            "CONFIDENCE         : 99.2%",
            "",
        ]
        for i in range(3):
            lines.append(f"--- CASE {i + 1} ---")
            lines += _random_case()
            lines.append("")
        lines += [
            "--- PRECOG STATUS ---",
            "",
            "AGATHA (female)    : ACTIVE — majority report confirmed",
            "DASHIELL HOWARD    : ACTIVE — supporting",
            "ARTHUR BROWN       : ACTIVE — supporting",
            "",
            "> NOTE: All three precogs must agree for majority report.",
            "> Minority report flag: 0 cases (current queue).",
            "> Dispatch recommended within 20 minutes of alert.",
        ]
        return lines

    def _suspects(self):
        return [
            "=== SUSPECT IDENTIFICATION SYSTEM ===",
            "",
            "BIOMETRIC DATABASE : 8,200,000 records (DC metro)",
            "RETINAL SCAN SPEED : 0.3 seconds",
            "FACIAL MATCH SPEED : 0.8 seconds",
            "",
            "--- SAMPLE IDENTIFICATION ---",
            "",
            "RETINAL SCAN: [INITIATING]",
            "SCANNING...",
            "",
            "MATCH FOUND",
            "",
            "  NAME          : John Anderton",
            "  BADGE         : PreCrime Chief 01",
            "  CLEARANCE     : Level 5 — PreCrime Command",
            "  STATUS        : FUGITIVE — [SEE ALERT BELOW]",
            "",
            "--- ACTIVE ALERT ---",
            "",
            "SUBJECT: JOHN ANDERTON",
            "CHARGE : Predicted murder — Leo Crow",
            "TIME   : 36 hours from issue",
            "STATUS : ESCAPE FROM CUSTODY — ARMED — DANGEROUS",
            "NOTE   : Anderton is familiar with PreCrime protocols.",
            "         Use non-standard approach.",
            "",
            "--- SECONDARY SUSPECTS ---",
            "",
            "SUBJECT: LEO CROW",
            "STATUS : VICTIM — NOT YET DECEASED",
            "         Predicted murder target of Anderton.",
            "",
            "> NOTE: Anderton claims a minority report exists.",
            "> All minority report inquiries: Director Lamar Burgess eyes only.",
        ]

    def _visions(self):
        return [
            "=== PRECOGNITIVE VISION ARCHIVE ===",
            "",
            "TOTAL VISIONS LOGGED  : 14,882",
            "MAJORITY REPORTS      : 14,880",
            "MINORITY REPORTS      : 2  [SEALED]",
            "",
            "--- RECENT VISION SUMMARY ---",
            "",
            "VISION ID: V-14881",
            "PRECOGS   : All three",
            "TYPE      : Majority report",
            "SUMMARY   : Male suspect (ID confirmed: M. Torres)",
            "            Homicide — Georgetown District",
            "            Victim: Female, 30s (ID: S. Kowalski)",
            "            Method: Firearm",
            "OUTCOME   : Intervention successful — Torres detained.",
            "",
            "VISION ID: V-14882  [LATEST]",
            "PRECOGS   : All three",
            "TYPE      : Majority report",
            "SUMMARY   : [SEE PREDICTED CRIMES — CASE 1]",
            "",
            "--- SEALED RECORDS ---",
            "",
            "VISION ID: V-00001  [SEALED — BURGESS]",
            "NOTE     : First PreCrime vision. Content classified.",
            "           Director Burgess present at time of vision.",
            "",
            "VISION ID: V-09991  [SEALED — BURGESS]",
            "SUBJECT  : Ann Lively (victim)",
            "NOTE     : Minority report exists. Access denied.",
            "           Director Burgess authorisation required.",
            "",
            "> ANDERTON NOTE: 'The precogs are never wrong.",
            "  But it is possible to see the same future... differently.'",
        ]

    def _surveillance(self):
        return [
            "=== CITYWIDE SURVEILLANCE GRID — WASHINGTON DC ===",
            "",
            "CAMERA NODES ACTIVE : 12,443",
            "RETINAL SCANS / MIN : 8,901 (metro average)",
            "ACTIVE ALERTS       : 3",
            "",
            "--- DISTRICT STATUS ---",
            "",
            "Georgetown          : MONITORED — 1 alert active",
            "Capitol Hill        : MONITORED — normal",
            "Navy Yard           : MONITORED — normal",
            "Dupont Circle       : MONITORED — normal",
            "Foggy Bottom        : MONITORED — 1 alert active",
            "Adams Morgan        : MONITORED — 1 alert active",
            "",
            "--- RETINAL SCANNER NETWORK ---",
            "",
            "> Retinal scanners embedded in: shopping centres, transit,",
            "  billboards, ATMs, pharmacies, and public doorways.",
            "> Average citizen scanned: 47 times per day.",
            "> Scanners trigger targeted advertising on proximity.",
            "> PreCrime division has override access to all scanner feeds.",
            "",
            "--- FUGITIVE TRACKING ---",
            "",
            "FUGITIVE: John Anderton",
            "LAST SCAN: Navy Yard metro — 14 minutes ago",
            "DIRECTION: Southbound",
            "NOTE     : Anderton has performed eye replacement.",
            "           Using legacy scans — effectiveness: 60%.",
            "",
            "> ALERT: Old eyes being used. Scan all personnel.",
        ]

    def _resolved(self):
        return [
            "=== CASE RESOLUTION LOG ===",
            "",
            "TOTAL CASES SINCE INCEPTION : 14,882",
            "SUCCESSFUL INTERVENTIONS    : 14,880 (99.99%)",
            "FAILED INTERVENTIONS        : 2",
            "WRONGFUL DETENTIONS         : 0  [OFFICIAL]",
            "",
            "--- RECENT RESOLUTIONS ---",
            "",
            "CASE 14,880",
            "  SUSPECT  : Torres, Michael",
            "  OUTCOME  : Detained 3 minutes before predicted event.",
            "  LOCATION : Georgetown District",
            "  STATUS   : SUCCESSFUL",
            "",
            "CASE 14,879",
            "  SUSPECT  : Park, David",
            "  OUTCOME  : Detained 7 minutes before predicted event.",
            "  STATUS   : SUCCESSFUL",
            "",
            "CASE 14,878",
            "  SUSPECT  : Hartwell, James",
            "  OUTCOME  : Subject complied — no resistance.",
            "  STATUS   : SUCCESSFUL",
            "",
            "--- DETENTION FACILITY STATUS ---",
            "",
            "FACILITY      : PreCrime Detention Facility, Chesapeake Bay",
            "TOTAL HELD    : 14,880",
            "DETENTION TYPE: Halo — suspended animation",
            "RELEASE RATE  : 0",
            "",
            "> LEGAL NOTE: Detention without trial has not been challenged.",
            "> Legislation still pending formal Supreme Court review.",
            "> PreCrime operates under executive order during review period.",
        ]
