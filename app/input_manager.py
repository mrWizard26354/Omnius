"""
OMNIUS Input Manager
Handles keyboard and future hardware input.
"""

import pygame
from app.config import SIM_CARD_KEYS


class InputEvent:
    """Normalised input event."""
    __slots__ = ("type", "key", "char")

    def __init__(self, etype: str, key: str = "", char: str = ""):
        self.type = etype   # "nav", "confirm", "back", "quit", "card_sim",
                            # "fullscreen", "dev_toggle", "char"
        self.key  = key
        self.char = char


class InputManager:
    def __init__(self):
        self.dev_mode = True   # start in dev mode for keyboard simulation

    def process(self) -> list[InputEvent]:
        """Convert pygame events into InputEvent list."""
        events = []
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                events.append(InputEvent("quit"))
                continue

            if ev.type != pygame.KEYDOWN:
                continue

            key  = pygame.key.name(ev.key).lower()
            char = ev.unicode

            # Quit
            if key == "q" and (ev.mod & pygame.KMOD_CTRL):
                events.append(InputEvent("quit"))

            # Fullscreen toggle
            elif key == "f11":
                events.append(InputEvent("fullscreen"))

            # Dev mode toggle
            elif key == "d" and (ev.mod & pygame.KMOD_CTRL):
                self.dev_mode = not self.dev_mode
                events.append(InputEvent("dev_toggle"))

            # Navigation
            elif ev.key == pygame.K_UP:
                events.append(InputEvent("nav", "up"))
            elif ev.key == pygame.K_DOWN:
                events.append(InputEvent("nav", "down"))
            elif ev.key == pygame.K_LEFT:
                events.append(InputEvent("nav", "left"))
            elif ev.key == pygame.K_RIGHT:
                events.append(InputEvent("nav", "right"))
            elif ev.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                events.append(InputEvent("confirm"))
            elif ev.key == pygame.K_ESCAPE:
                events.append(InputEvent("back"))

            # Simulated card insertion (number keys in dev mode)
            elif self.dev_mode and char in SIM_CARD_KEYS:
                events.append(InputEvent("card_sim", char=char))

            # Generic character input (for sub-system prompts)
            else:
                events.append(InputEvent("char", char=char))

        return events
