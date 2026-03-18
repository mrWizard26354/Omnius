"""
OMNIUS Base Subsystem
All themed terminals inherit from this.
"""

import time
import pygame
from app.config import SCREEN_WIDTH, SCREEN_HEIGHT, NODE_ID
from app.effects import (
    CRTOverlay, ScreenFlicker, BlinkingCursor,
    draw_glow_text, draw_header_line, draw_footer,
)


class BaseSystem:
    """
    Base class for all OMNIUS subsystem terminals.
    Provides:
    - palette-aware rendering helpers
    - menu navigation
    - CRT/flicker effects
    - standard header/footer
    Subclasses define self._menu_entries and override handle_confirm().
    """

    # Override in subclass
    SYSTEM_TITLE    = "UNKNOWN SYSTEM"
    SYSTEM_SUBTITLE = "ARCHIVE ACCESS"
    NODE_LABEL      = "XX-00"

    def __init__(self, fonts, audio, crt: CRTOverlay, flicker: ScreenFlicker, palette: dict):
        self._fonts    = fonts
        self._audio    = audio
        self._crt      = crt
        self._flicker  = flicker
        self._pal      = palette
        self._cursor   = BlinkingCursor()
        self._sel      = 0
        self._view     = "menu"      # "menu" or "detail"
        self._detail   = None        # detail content list[str]
        self._detail_title = ""
        self._scroll   = 0
        self._exit_req = False

        # Subclass populates this: list of (label, content_lines)
        self._menu_entries: list[tuple[str, list[str]]] = []

    @property
    def exit_requested(self):
        return self._exit_req

    # ── Input ─────────────────────────────────────────────────────────────────

    def nav_up(self):
        if self._view == "detail":
            self._scroll = max(0, self._scroll - 1)
        else:
            self._sel = (self._sel - 1) % max(1, len(self._menu_entries))
        self._audio.play("tick")

    def nav_down(self):
        if self._view == "detail":
            self._scroll += 1
        else:
            self._sel = (self._sel + 1) % max(1, len(self._menu_entries))
        self._audio.play("tick")

    def confirm(self):
        if self._view == "menu" and self._menu_entries:
            label, content = self._menu_entries[self._sel]
            self._detail_title = label
            self._detail       = content
            self._scroll       = 0
            self._view         = "detail"
            self._audio.play("open")

    def back(self):
        if self._view == "detail":
            self._view   = "menu"
            self._detail = None
            self._audio.play("tick")
        else:
            self._exit_req = True

    def update(self):
        self._cursor.update()

    # ── Draw ──────────────────────────────────────────────────────────────────

    def draw(self, surface: pygame.Surface):
        surface.fill(self._pal["bg"])
        W, H = SCREEN_WIDTH, SCREEN_HEIGHT
        f    = self._fonts

        # Header
        header_txt = f"OMNIUS // {self.SYSTEM_TITLE}"
        draw_glow_text(surface, header_txt, f.small, self._pal["primary"],
                       (W // 2, 20), center=True,
                       glow_color=self._pal["primary"], glow_radius=3)
        draw_glow_text(surface, self.SYSTEM_SUBTITLE, f.tiny, self._pal["accent"],
                       (W // 2, 40), center=True)
        draw_header_line(surface, self._pal["dim"], 54, W)

        if self._view == "menu":
            self._draw_menu(surface)
        else:
            self._draw_detail(surface)

        draw_footer(surface, f.tiny, self._pal,
                    f"{NODE_ID} / {self.NODE_LABEL}",
                    auth="VERIFIED",
                    extra="ESC: BACK")
        self._crt.draw(surface)
        self._flicker.apply(surface)

    def _draw_menu(self, surface: pygame.Surface):
        W, H = SCREEN_WIDTH, SCREEN_HEIGHT
        f    = self._fonts
        x    = 60
        y    = 70
        row  = 38

        for i, (label, _) in enumerate(self._menu_entries):
            is_sel = (i == self._sel)
            if is_sel:
                bar = pygame.Surface((W - 80, row - 4), pygame.SRCALPHA)
                bar.fill((*self._pal["primary"][:3], 35))
                surface.blit(bar, (40, y + i * row - 2))
                pygame.draw.rect(surface, self._pal["primary"],
                                 (40, y + i * row - 2, W - 80, row - 4), 1)
            col = self._pal["accent"] if is_sel else self._pal["text"]
            idx = f"[{i + 1:02d}]"
            draw_glow_text(surface, idx,   f.normal, self._pal["dim"],  (x, y + i * row))
            draw_glow_text(surface, label, f.normal, col, (x + 60, y + i * row))

        prompt_y = H - 110
        draw_header_line(surface, self._pal["dim"], prompt_y - 8, W)
        draw_glow_text(surface, f"ENTER COMMAND {self._cursor.symbol}",
                       f.medium, self._pal["primary"],
                       (x, prompt_y),
                       glow_color=self._pal["primary"], glow_radius=2)

    def _draw_detail(self, surface: pygame.Surface):
        W, H = SCREEN_WIDTH, SCREEN_HEIGHT
        f    = self._fonts

        # Title
        draw_glow_text(surface, self._detail_title, f.medium, self._pal["accent"],
                       (W // 2, 68), center=True)
        draw_header_line(surface, self._pal["dim"], 90, W)

        if not self._detail:
            draw_glow_text(surface, "NO DATA", f.normal, self._pal["dim"],
                           (W // 2, 200), center=True)
            return

        # Scrollable text
        visible_h = H - 180
        lh        = f.normal.get_linesize() + 2
        max_lines = visible_h // lh
        lines     = self._detail
        start     = min(self._scroll, max(0, len(lines) - max_lines))
        self._scroll = start

        for i, line in enumerate(lines[start: start + max_lines]):
            color = self._pal["text"]
            if line.startswith("===") or line.startswith("---"):
                color = self._pal["dim"]
            elif line.startswith(">") or line.startswith("WARNING") or line.startswith("ALERT"):
                color = self._pal["warning"]
            elif line.startswith("ERROR") or line.startswith("CRITICAL"):
                color = self._pal["error"]
            elif line.startswith("STATUS") or line.startswith("OK") or line.startswith("ONLINE"):
                color = self._pal["ok"]
            draw_glow_text(surface, line, f.normal, color, (60, 100 + i * lh))

        # Scroll indicator
        if len(lines) > max_lines:
            pct = int(start / max(1, len(lines) - max_lines) * 100)
            stxt = f.tiny.render(f"[ {pct}% ]  \u2191\u2193 scroll", True, self._pal["dim"])
            surface.blit(stxt, (W - stxt.get_width() - 10, H - 50))
