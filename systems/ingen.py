"""
InGen Park Operations Database
"""
from systems.base_system import BaseSystem


class InGenTerminal(BaseSystem):
    SYSTEM_TITLE    = "INGEN PARK AND WILDLIFE CONTROL"
    SYSTEM_SUBTITLE = "GENETIC ASSET MANAGEMENT NETWORK"
    NODE_LABEL      = "JP-01"

    def __init__(self, fonts, audio, crt, flicker, palette):
        super().__init__(fonts, audio, crt, flicker, palette)
        self._menu_entries = [
            ("PARK STATUS",           self._park_status()),
            ("DNA SEQUENCE LOGS",     self._dna()),
            ("PADDOCK MONITORING",    self._paddocks()),
            ("SPECIES INDEX",         self._species()),
            ("SECURITY OVERRIDES",    self._security()),
        ]

    def _park_status(self):
        return [
            "=== JURASSIC PARK — SYSTEM STATUS ===",
            "",
            "PARK NAME          : Jurassic Park",
            "LOCATION           : Isla Nublar, Costa Rica",
            "OPERATIONAL STATUS : OFFLINE",
            "LAST ACTIVE        : 1993-06-11",
            "",
            "--- SYSTEM COMPONENTS ---",
            "",
            "POWER GRID         : OFFLINE   [Main generator failure]",
            "ELECTRIC FENCES    : OFFLINE   [CRITICAL]",
            "SECURITY CAMERAS   : 12% ONLINE",
            "PADDOCK LOCKS      : OVERRIDE ACTIVE  [UNAUTHORISED]",
            "VISITOR CENTER     : EMERGENCY LOCKDOWN",
            "VEHICLE SYSTEM     : OFFLINE   [Track failure]",
            "COMMUNICATIONS     : DEGRADED  [Satellite dish offline]",
            "",
            "--- INCIDENT LOG ---",
            "",
            "> 1993-06-11  11:02: Employee Nedry, Dennis deactivates security.",
            "> 1993-06-11  11:08: Paddock 09 fence power loss. Tyrannosaurus breach.",
            "> 1993-06-11  14:31: Raptors escape Paddock 11.",
            "> 1993-06-11  20:44: Primary power restored. Fences reactivated.",
            "> 1993-06-12  07:00: InGen crisis team en route.",
            "",
            "STATUS: ISLAND QUARANTINE ACTIVE. DO NOT APPROACH.",
        ]

    def _dna(self):
        return [
            "=== DNA SEQUENCING LABORATORY — ARCHIVE ===",
            "",
            "LEAD RESEARCHER    : Dr. Henry Wu",
            "FACILITY           : Hammond Creation Lab, Isla Nublar",
            "TOTAL SEQUENCES    : 14,847 on record",
            "",
            "--- ACTIVE GENOME PROJECTS ---",
            "",
            "SPECIES                  COMPLETENESS  METHOD",
            "Tyrannosaurus rex        100%          Amber extraction + frog DNA fill",
            "Velociraptor             100%          Amber extraction + snake DNA fill",
            "Triceratops              100%          Amber extraction",
            "Brachiosaurus            100%          Amber extraction",
            "Dilophosaurus            100%          Amber extraction + monitor lizard",
            "Parasaurolophus          100%          Amber extraction",
            "Gallimimus               100%          Amber extraction",
            "Pteranodon               100%          Amber extraction",
            "Indominus rex            100%          [CLASSIFIED — Dr. Wu authorization]",
            "",
            "--- DNA FILL NOTES ---",
            "",
            "> WARNING: Frog DNA fill introduced unforeseen sex-change capability.",
            "> Some animals have begun breeding in the wild.",
            "> Full lifecycle analysis recommended before resuming operations.",
            "",
            "--- LYSINE CONTINGENCY ---",
            "",
            "All animals engineered with lysine deficiency.",
            "Without dietary supplement, neural inhibition occurs within 7-10 days.",
            "",
            "> NOTE: Field observation suggests animals have bypassed this restriction.",
            "> Arginase enzyme found in park vegetation — contingency may be INACTIVE.",
        ]

    def _paddocks(self):
        return [
            "=== PADDOCK MONITORING SYSTEM ===",
            "",
            "TOTAL PADDOCKS     : 24",
            "ACTIVE FENCES      : 0 / 24   [POWER OFFLINE]",
            "",
            "--- PADDOCK STATUS ---",
            "",
            "PADDOCK  01  Brachiosaurus       FENCE: OFFLINE  OCCUPANTS: 6",
            "PADDOCK  02  Triceratops         FENCE: OFFLINE  OCCUPANTS: 4",
            "PADDOCK  04  Parasaurolophus     FENCE: OFFLINE  OCCUPANTS: 22",
            "PADDOCK  05  Gallimimus          FENCE: OFFLINE  OCCUPANTS: 37",
            "PADDOCK  06  Dilophosaurus       FENCE: OFFLINE  OCCUPANTS: 3",
            "PADDOCK  08  Pteranodon          AVIARY OFFLINE  OCCUPANTS: UNKNOWN",
            "PADDOCK  09  Tyrannosaurus rex   FENCE: OFFLINE  OCCUPANTS: UNCONFIRMED",
            "             NOTE: Occupant last GPS ping: Visitor Center, 1993-06-11",
            "PADDOCK  11  Velociraptor        FENCE: OFFLINE  OCCUPANTS: 0",
            "             NOTE: BREACH CONFIRMED. All three raptors unaccounted for.",
            "",
            "--- ALERTS ---",
            "",
            "CRITICAL: Paddock 09 breach — T-rex outside perimeter.",
            "CRITICAL: Paddock 11 breach — Raptors uncontained.",
            "WARNING : Motion sensors offline. Animal locations unverified.",
        ]

    def _species(self):
        return [
            "=== SPECIES ASSET INDEX ===",
            "",
            "TOTAL SPECIES CLONED : 15",
            "TOTAL ANIMALS        : 238 (estimated)",
            "",
            "SPECIES               ERA            THREAT  COUNT",
            "Tyrannosaurus rex     Late Cretaceous  HIGH     2",
            "Velociraptor          Late Cretaceous  EXTREME  3",
            "Dilophosaurus         Early Jurassic   HIGH     3",
            "Brachiosaurus         Late Jurassic    LOW      6",
            "Triceratops           Late Cretaceous  MED      4",
            "Parasaurolophus       Late Cretaceous  LOW     22",
            "Gallimimus            Late Cretaceous  LOW     37",
            "Pteranodon            Late Cretaceous  MED      8",
            "Stegosaurus           Late Jurassic    LOW      7",
            "Ankylosaurus          Late Cretaceous  MED      4",
            "Spinosaurus           Early Cretaceous HIGH     2",
            "Indominus rex         [HYBRID]         EXTREME  1",
            "  Source code: [CLASSIFIED — Dr. Wu clearance]",
            "",
            "--- BEHAVIOURAL NOTES ---",
            "",
            "> Velociraptors demonstrate pack intelligence exceeding initial projections.",
            "> T-rex shows stronger olfactory response than modelled.",
            "> Indominus exhibits thermal masking — evades IR detection.",
        ]

    def _security(self):
        return [
            "=== SECURITY OVERRIDE LOG ===",
            "",
            "WARNING: UNAUTHORISED ACCESS DETECTED",
            "",
            "1993-06-11  10:58  User: D.Nedry  — Security bypass initiated",
            "                   Whiterabbit unlock sequence executed",
            "                   24 paddock locks disengaged",
            "                   Camera feeds interrupted — 97 of 102 cameras",
            "",
            "CURRENT LOCK STATUS: ALL LOCKS DISENGAGED",
            "",
            "--- AUTHORISED USERS ---",
            "",
            "John Hammond       — Level 5  (Owner)",
            "Dr. Henry Wu       — Level 5  (Chief Geneticist)",
            "Robert Muldoon     — Level 4  (Park Warden)",
            "Ray Arnold         — Level 4  (Chief Engineer) [DECEASED]",
            "Dr. Ellie Sattler  — Level 3  (Botanist) [TEMPORARY]",
            "Dr. Alan Grant     — Level 3  (Palaeontologist) [TEMPORARY]",
            "Dennis Nedry       — Level 2  (Programmer) [TERMINATED]",
            "",
            "--- RESTORE PROCEDURE ---",
            "",
            "> Manual fuse reset required at Maintenance Shed B.",
            "> Utility shed coordinates: Grid 7-G, south perimeter.",
            "> Restoring power requires physical presence at shed.",
            "",
            "ALERT: Restoring power to fences is top priority.",
            "ALERT: Do not enter paddock zones without power restored.",
        ]
