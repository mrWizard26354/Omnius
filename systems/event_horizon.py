"""
Event Horizon Ship Archive
"""
import random
from systems.base_system import BaseSystem


# Corruption glitch strings that randomly appear in some content
_GLITCH = [
    "̸͔͝Ì̶̩T̶̜͝ ̵͖̈́K̶̲͝N̷͖̑O̷͉͝W̵̱̒S̷̰̊",
    "[DATA CORRUPTED]",
    "LIBERATE TUTEMET EX INFERIS",
    "̢̛̺̗͙̲̯̥̤͉̙̻̩̩̘̤̖͖̦̟̟̀̀͐̌̌",
    "SAVE YOURSELF",
    "[SIGNAL LOST]",
]


def _maybe_glitch(line: str, rate: float = 0.06) -> str:
    if random.random() < rate:
        return random.choice(_GLITCH)
    return line


class EventHorizonTerminal(BaseSystem):
    SYSTEM_TITLE    = "U.S.A.C. SEARCH AND RESCUE LOGS"
    SYSTEM_SUBTITLE = "CLASSIFIED DEEP-SPACE INCIDENT RECORDS"
    NODE_LABEL      = "EH-01"

    def __init__(self, fonts, audio, crt, flicker, palette):
        super().__init__(fonts, audio, crt, flicker, palette)
        self._menu_entries = [
            ("SHIP OPERATIONAL LOGS",     self._ship_logs()),
            ("CREW PERSONAL LOGS",        self._crew_logs()),
            ("GRAVITY DRIVE DATA",        self._gravity()),
            ("PSYCHOLOGICAL EVALUATIONS", self._psych()),
            ("INCIDENT REPORTS",          self._incidents()),
        ]

    def _ship_logs(self):
        base = [
            "=== USG EVENT HORIZON — SHIP LOG ARCHIVE ===",
            "",
            "VESSEL       : USG Event Horizon",
            "CLASS        : Research / Experimental",
            "OPERATOR     : Lewis & Clark Aerospace (LCSA)",
            "STATUS       : MISSING — 2040 to 2047  [FOUND]",
            "MISSION      : Classified — experimental gravity drive test",
            "",
            "--- OPERATIONAL LOG ---",
            "",
            "LOG 001  2040-01-15 : Departure — Neptune orbital station.",
            "LOG 014  2040-01-22 : Gravity drive test — Day 1. Nominal.",
            "LOG 015  2040-01-22 : GRAVITY DRIVE ACTIVATION. [TIMESTAMP CORRUPTED]",
            "LOG 016  [DATE UNKNOWN] : [DATA CORRUPTED]",
            "LOG 017  [DATE UNKNOWN] : [SIGNAL LOST]",
            "LOG 018  2047-08-01 : Event Horizon reappears near Neptune.",
            "          Distress beacon active. No crew contact established.",
            "",
            "--- RESCUE MISSION LOG — Lewis & Clark ---",
            "",
            "LOG R-001  2047-08-09 : Lewis & Clark departs for Neptune.",
            "LOG R-012  2047-08-19 : Boarding of Event Horizon.",
            "           First contact: ship systems partially functional.",
            "           Gravity drive: ACTIVE and PULSING.",
            "           Crew: 0 survivors found — 7 bodies recovered.",
            "LOG R-028  2047-08-21 : Anomalous events begin — [CLASSIFIED]",
        ]
        return [_maybe_glitch(l) for l in base]

    def _crew_logs(self):
        base = [
            "=== CREW PERSONAL LOGS — EVENT HORIZON ===",
            "",
            "NOTE: Recovered from ship memory. Partial corruption.",
            "",
            "--- DR. WILLIAM WEIR — CHIEF ENGINEER ---",
            "",
            "LOG ENTRY: WEIR-04",
            "DATE: 2040-01-20",
            "'The drive performed beyond expectations today.",
            " Claire appeared to me in the corridor last night.",
            " I know that is impossible. She has been dead for years.",
            " I am under stress. That is the only explanation.'",
            "",
            "LOG ENTRY: WEIR-09",
            "DATE: [CORRUPTED]",
            "'The ship is speaking to me. I can hear it clearly now.",
            " It is not a malfunction. It is not the drive noise.",
            " It wants us here. It wants us.',",
            "",
            "LOG ENTRY: WEIR-12",
            "DATE: [CORRUPTED]",
            "[DATA CORRUPTED — 847 characters]",
            "",
            "--- CAPTAIN JOHN KILPACK ---",
            "",
            "LOG ENTRY: KILPACK-07",
            "DATE: 2040-01-23",
            "'Crew morale declining. Weir is concerning me.",
            " Strange sounds in decks B and C at night.",
            " Recommend aborting mission — denied by LCSA.'",
            "",
            "LOG ENTRY: KILPACK-FINAL",
            "DATE: [CORRUPTED]",
            "'It will not let us leave. The drive — it opened something.",
            " Do not send another ship. Do not come here.",
            " LIBERATE TUTEMET EX INFERIS —'",
            "[SIGNAL LOST]",
        ]
        return [_maybe_glitch(l) for l in base]

    def _gravity(self):
        base = [
            "=== EXPERIMENTAL GRAVITY DRIVE — DATA LOG ===",
            "",
            "DRIVE DESIGNATION  : Gravity Drive Mk I",
            "PRINCIPLE          : Artificial black hole — space-time folding",
            "DESIGNER           : Dr. William Weir",
            "POWER SOURCE       : Anti-matter core",
            "",
            "--- TEST PARAMETERS ---",
            "",
            "DESTINATION        : Proxima Centauri (4.2 light years)",
            "METHOD             : Fold space — create point singularity",
            "                     Travel through folded space.",
            "EXPECTED DURATION  : Instantaneous",
            "",
            "--- TEST RESULTS ---",
            "",
            "TEST DATE          : 2040-01-22",
            "RESULT             : [CLASSIFIED — CLEARANCE OMEGA]",
            "",
            "DIMENSIONAL STABILITY  : [UNDEFINED VALUE]",
            "SPATIAL RIFT DETECTED  : YES",
            "RIFT DESTINATION       : [DOES NOT CORRESPOND TO KNOWN SPACE]",
            "",
            "> ANALYSIS: The drive did not fold space within this universe.",
            "> It opened a gateway to another dimension.",
            "> The nature of that dimension is unknown.",
            "> What returned with the ship is unknown.",
            "",
            "DR. WEIR NOTES:",
            "'Where we're going, we won't need eyes to see.'",
            "",
            "[DATA CORRUPTED — REMAINING 4,441 CHARACTERS UNRECOVERABLE]",
        ]
        return [_maybe_glitch(l) for l in base]

    def _psych(self):
        base = [
            "=== PSYCHOLOGICAL EVALUATION RECORDS ===",
            "",
            "EVALUATING OFFICER : Dr. D.J. (Lewis & Clark crew)",
            "SUBJECTS           : Event Horizon rescue team",
            "",
            "--- SUBJECT: CPT. MILLER ---",
            "",
            "PRE-MISSION        : Stable. PTSD (previous accident, noted).",
            "DAY 1 BOARDING     : Professional. Cautious.",
            "DAY 2              : Reports seeing crewman Justin — deceased.",
            "                    Claims he 'saw something in the core'.",
            "DAY 3              : PSYCHOLOGICAL STABILITY: CRITICAL",
            "                    Experiencing vivid hallucinations.",
            "                    Refuses to elaborate on content.",
            "",
            "--- SUBJECT: DR. WEIR ---",
            "",
            "PRE-MISSION        : Obsessive personality. Grief (wife, suicide).",
            "DAY 1 BOARDING     : Agitated. Excited.",
            "DAY 2              : Reports seeing his wife repeatedly.",
            "DAY 3              : EYE TRAUMA — unexplained.",
            "                    PSYCHOLOGICAL STABILITY: FAILED",
            "                    Subject is hostile. Do not approach alone.",
            "",
            "--- SUBJECT: PETERS ---",
            "",
            "DAY 2              : Reports seeing her son. Graphic hallucination.",
            "                    Son described with severe injuries not matching",
            "                    any known prior trauma.",
            "",
            "=== CONCLUSION ===",
            "",
            "RECOMMENDATION: Immediate evacuation of Event Horizon.",
            "The ship is inducing shared psychosis through unknown mechanism.",
            "The drive core must not be reactivated.",
            "",
            "WARNING WARNING WARNING",
        ]
        return [_maybe_glitch(l) for l in base]

    def _incidents(self):
        base = [
            "=== INCIDENT REPORT — EVENT HORIZON ===",
            "",
            "CLASSIFICATION    : OMEGA — DO NOT FILE — DESTROY AFTER READING",
            "",
            "INCIDENT DATE     : 2047-08-20",
            "REPORTING OFFICER : Lt. Starck — Lewis & Clark",
            "",
            "SUMMARY:",
            "",
            "> Event Horizon crew found dead — 7 bodies in various states.",
            "> Cause of death: self-inflicted and mutually inflicted injuries.",
            "> Evidence suggests crew entered psychotic state simultaneously.",
            "> Video log recovered: crew performing acts of extreme violence.",
            "",
            "GRAVITY DRIVE STATUS AT RECOVERY: ACTIVE — PULSING",
            "",
            "SUBSEQUENT EVENTS (Lewis & Clark mission):",
            "",
            "> Justin (crew) entered drive core — catatonic on retrieval.",
            "> Cooper (crew) fatally injured — EVA without suit.",
            "> Dr. Weir — hostile. Murdered crew members.",
            "> Weir entered drive core. Reappeared with eye injuries.",
            "> Weir appeared to be possessed or fundamentally altered.",
            "",
            "STARCK FINAL REPORT: 'The ship went somewhere. Something came back.'",
            "",
            "LCSA RESPONSE: RECORD SUPPRESSED. DRIVE PROGRAM CLASSIFIED.",
            "",
            "[LIBERATE TUTEMET EX INFERIS]",
            "[SAVE YOURSELF FROM HELL]",
        ]
        return [_maybe_glitch(l) for l in base]
