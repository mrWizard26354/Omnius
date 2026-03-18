"""
OMNIUS Visual Effects
CRT scanlines, flicker, glow, typewriter text.
"""

import random
import time
import pygame
from app.config import SCANLINE_ALPHA, FLICKER_CHANCE, SCREEN_WIDTH, SCREEN_HEIGHT


class CRTOverlay:
    """Scanline overlay surface — create once, blit every frame."""

    def __init__(self, width: int, height: int):
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.surface.fill((0, 0, 0, 0))
        for y in range(0, height, 3):
            pygame.draw.line(self.surface, (0, 0, 0, SCANLINE_ALPHA),     (0, y),     (width, y))
            pygame.draw.line(self.surface, (0, 0, 0, SCANLINE_ALPHA // 2),(0, y + 1), (width, y + 1))

    def draw(self, screen: pygame.Surface):
        screen.blit(self.surface, (0, 0))


class ScreenFlicker:
    """Randomised brief brightness pulse."""

    def apply(self, screen: pygame.Surface):
        if random.random() < FLICKER_CHANCE:
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, random.randint(4, 16)))
            screen.blit(overlay, (0, 0))


class TypewriterText:
    """
    Renders a string character-by-character over time.
    Call update() each frame; draw() renders the current visible slice.
    """

    def __init__(self, text: str, delay: float = 0.03, start_now: bool = True):
        self.text      = text
        self.delay     = delay
        self._index    = 0
        self._last     = time.time() if start_now else float("inf")
        self.complete  = (len(text) == 0)

    def start(self):
        self._last = time.time()

    def update(self):
        if self.complete:
            return
        now = time.time()
        while now - self._last >= self.delay and self._index < len(self.text):
            self._index += 1
            self._last  += self.delay
        if self._index >= len(self.text):
            self.complete = True

    def skip(self):
        self._index   = len(self.text)
        self.complete = True

    @property
    def visible(self) -> str:
        return self.text[: self._index]


class BlinkingCursor:
    """Toggles visibility on a fixed interval."""

    def __init__(self, char: str = "_", rate: float = 0.55):
        self.char    = char
        self.rate    = rate
        self.visible = True
        self._last   = time.time()

    def update(self):
        now = time.time()
        if now - self._last >= self.rate:
            self.visible = not self.visible
            self._last   = now

    @property
    def symbol(self) -> str:
        return self.char if self.visible else " "


def draw_glow_text(
    surface: pygame.Surface,
    text: str,
    font: pygame.font.Font,
    color: tuple,
    pos: tuple,
    glow_color: tuple = None,
    glow_radius: int = 3,
    center: bool = False,
):
    """
    Renders text with an optional glow effect.
    pos is (x, y). If center=True, x/y is the centre of the text rect.
    """
    if glow_color:
        for dx in range(-glow_radius, glow_radius + 1, 2):
            for dy in range(-glow_radius, glow_radius + 1, 2):
                if dx == 0 and dy == 0:
                    continue
                gsurf = font.render(text, True, glow_color)
                if center:
                    r = gsurf.get_rect(center=(pos[0] + dx, pos[1] + dy))
                else:
                    r = gsurf.get_rect(topleft=(pos[0] + dx, pos[1] + dy))
                surface.blit(gsurf, r)
    main_surf = font.render(text, True, color)
    if center:
        r = main_surf.get_rect(center=pos)
    else:
        r = main_surf.get_rect(topleft=pos)
    surface.blit(main_surf, r)


def draw_header_line(
    surface: pygame.Surface,
    color: tuple,
    y: int,
    width: int,
    margin: int = 40,
):
    pygame.draw.line(surface, color, (margin, y), (width - margin, y), 1)


def draw_footer(
    surface: pygame.Surface,
    font: pygame.font.Font,
    palette: dict,
    node: str,
    status: str = "SECURE",
    auth: str = "VERIFIED",
    extra: str = "ESC: RETURN",
    height: int = SCREEN_HEIGHT,
    width: int = SCREEN_WIDTH,
):
    """Draws the standard OMNIUS footer bar."""
    bar_h = 28
    bar_y = height - bar_h
    bar_surf = pygame.Surface((width, bar_h))
    bar_surf.fill(palette.get("footer_bg", (10, 5, 25)))
    surface.blit(bar_surf, (0, bar_y))
    pygame.draw.line(surface, palette.get("dim", (60, 60, 80)), (0, bar_y), (width, bar_y), 1)

    items = [
        f"NODE: {node}",
        f"STATUS: {status}",
        f"AUTH: {auth}",
        extra,
    ]
    gap = width // len(items)
    for i, item in enumerate(items):
        txt = font.render(item, True, palette.get("dim", (80, 80, 100)))
        x   = gap * i + gap // 2
        r   = txt.get_rect(center=(x, bar_y + bar_h // 2))
        surface.blit(txt, r)
