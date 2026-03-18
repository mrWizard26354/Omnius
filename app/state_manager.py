"""
OMNIUS State Manager
Manages application state transitions.
"""

from app.config import (
    STATE_BOOT, STATE_WAITING_FOR_CARD, STATE_AUTHENTICATING,
    STATE_MASTER_MENU, STATE_SUBSYSTEM, STATE_ERROR
)


class StateManager:
    def __init__(self):
        self._state         = STATE_BOOT
        self._prev_state    = None
        self._subsystem_key = None   # active subsystem identifier
        self._card_profile  = None   # authenticated card profile dict
        self._error_msg     = None

    # ── Accessors ─────────────────────────────────────────────────────────────

    @property
    def state(self):
        return self._state

    @property
    def subsystem_key(self):
        return self._subsystem_key

    @property
    def card_profile(self):
        return self._card_profile

    @property
    def error_msg(self):
        return self._error_msg

    # ── Transitions ───────────────────────────────────────────────────────────

    def boot_complete(self):
        self._transition(STATE_WAITING_FOR_CARD)

    def card_inserted(self, card_profile: dict):
        self._card_profile = card_profile
        self._transition(STATE_AUTHENTICATING)

    def auth_complete(self):
        self._transition(STATE_MASTER_MENU)

    def auth_failed(self, reason: str = "UNRECOGNIZED AUTHORIZATION PROFILE"):
        self._error_msg = reason
        self._transition(STATE_ERROR)

    def select_subsystem(self, key: str):
        self._subsystem_key = key
        self._transition(STATE_SUBSYSTEM)

    def exit_subsystem(self):
        self._subsystem_key = None
        self._transition(STATE_MASTER_MENU)

    def return_to_boot(self):
        self._card_profile  = None
        self._subsystem_key = None
        self._transition(STATE_BOOT)

    def clear_error(self):
        self._error_msg = None
        self._transition(STATE_WAITING_FOR_CARD)

    # ── Internal ──────────────────────────────────────────────────────────────

    def _transition(self, new_state: str):
        self._prev_state = self._state
        self._state      = new_state
