"""
OMNIUS Card Input Abstraction Layer
Supports keyboard simulation and future RFID/HID hardware.
"""

import json
import os
from app.config import CARD_PROFILES, SIM_CARD_KEYS


class CardInputProvider:
    """
    Abstract card input provider.
    Swap the active provider to switch between keyboard sim and hardware.
    """

    def __init__(self):
        self._profiles = self._load_profiles()

    def _load_profiles(self) -> dict:
        if os.path.exists(CARD_PROFILES):
            with open(CARD_PROFILES, "r") as f:
                return json.load(f)
        return {}

    def validate_card(self, card_id: str) -> bool:
        return card_id in self._profiles

    def map_card_to_profile(self, card_id: str) -> dict | None:
        return self._profiles.get(card_id)

    def get_sim_card_id(self, key_name: str) -> str | None:
        """
        Returns a card ID for a simulated keypress, or None.
        key_name should be the character, e.g. '1', '2', ...
        """
        return SIM_CARD_KEYS.get(key_name)

    def reload_profiles(self):
        self._profiles = self._load_profiles()
