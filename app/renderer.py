"""
OMNIUS Renderer
Font loading, shared drawing utilities.
"""

import os
import pygame
from app.config import FONTS_DIR, SCREEN_WIDTH, SCREEN_HEIGHT


# Bundled fallback font names (pygame system fonts)
_FALLBACK_MONO = ["couriernew", "courier", "lucidaconsole", "consolas", "monospace"]


def _load_font(size: int, bold: bool = False) -> pygame.font.Font:
    """
    Try to load VT323 or similar from assets/fonts/.
    Falls back to system monospace if unavailable.
    """
    candidates = []
    if os.path.isdir(FONTS_DIR):
        for f in os.listdir(FONTS_DIR):
            if f.lower().endswith(".ttf") or f.lower().endswith(".otf"):
                candidates.append(os.path.join(FONTS_DIR, f))

    # Prefer VT323 or any retro-named font
    preferred_order = ["vt323", "terminus", "ibm", "px", "retro", "mono"]
    candidates.sort(key=lambda p: next(
        (i for i, k in enumerate(preferred_order) if k in os.path.basename(p).lower()),
        99
    ))

    for path in candidates:
        try:
            return pygame.font.Font(path, size)
        except Exception:
            continue

    # Fallback: system monospace
    for name in _FALLBACK_MONO:
        font = pygame.font.SysFont(name, size, bold=bold)
        if font:
            return font

    return pygame.font.SysFont(None, size)


class FontSet:
    """Pre-loaded font sizes for the application."""

    def __init__(self):
        self.tiny    = _load_font(16)
        self.small   = _load_font(20)
        self.normal  = _load_font(24)
        self.medium  = _load_font(30)
        self.large   = _load_font(40)
        self.xlarge  = _load_font(52)
        self.huge    = _load_font(68)
        self.logo    = _load_font(76)
        self.display = _load_font(130)  # boot logo title
        self.ascii   = _load_font(16)   # ASCII art logo rendering


def wrap_text(text: str, font: pygame.font.Font, max_width: int) -> list[str]:
    """Word-wrap text to fit within max_width pixels."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        if font.size(test)[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines
