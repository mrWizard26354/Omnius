"""
OMNIUS Authentication Screen
Plays after a card is detected; transitions to master menu on success.
"""

import time
import pygame
from app.config import OMNIUS, SCREEN_WIDTH, SCREEN_HEIGHT, AUTH_STEP_DELAY, NODE_ID
from app.effects import (
    CRTOverlay, ScreenFlicker, TypewriterText, BlinkingCursor,
    draw_glow_text, draw_header_line, draw_footer,
)


AUTH_STEPS_OK = [
    "CARD DETECTED",
    "READING CREDENTIAL HASH...",
    "DECRYPTING PROFILE DATA...",
    "ACCESS PROFILE VERIFIED",
    "AUTHORIZATION ACCEPTED",
    "LOADING OMNIUS MASTER INDEX...",
]

AUTH_STEPS_FAIL = [
    "CARD DETECTED",
    "READING CREDENTIAL HASH...",
    "PROFILE NOT FOUND IN REGISTRY",
    "ACCESS DENIED",
]


class AuthScreen:
    def __init__(self, fonts, audio, crt: CRTOverlay, flicker: ScreenFlicker):
        self._fonts   = fonts
        self._audio   = audio
        self._crt     = crt
        self._flicker = flicker
        self._reset()

    def _reset(self):
        self._step        = 0
        self._lines_shown = []
        self._step_timer  = 0.0
        self._started     = False
        self._success     = None    # None = pending, True/False = result
        self._done        = False
        self._profile     = None
        self._cursor      = BlinkingCursor()

    @property
    def done(self):
        return self._done

    @property
    def success(self):
        return self._success

    def start(self, profile: dict | None):
        self._reset()
        self._profile  = profile
        self._success  = profile is not None
        self._started  = True
        self._steps    = AUTH_STEPS_OK if self._success else AUTH_STEPS_FAIL
        self._step_timer = time.time()
        self._audio.play("tick")

    def update(self):
        self._cursor.update()
        if not self._started or self._done:
            return

        now = time.time()
        if now - self._step_timer >= AUTH_STEP_DELAY:
            if self._step < len(self._steps):
                self._lines_shown.append(self._steps[self._step])
                self._step       += 1
                self._step_timer  = now
                if self._step == len(self._steps):
                    if self._success:
                        self._audio.play("accept")
                    else:
                        self._audio.play("denied")
                else:
                    self._audio.play("tick")
            else:
                # Hold last frame briefly then signal done
                if now - self._step_timer > AUTH_STEP_DELAY * 1.5:
                    self._done = True

    def draw(self, surface: pygame.Surface):
        surface.fill(OMNIUS["bg"])
        W, H = SCREEN_WIDTH, SCREEN_HEIGHT
        f    = self._fonts

        # Header
        draw_glow_text(surface, "OMNITECH SYSTEMS  //  OMNIUS NETWORK NODE 03",
                       f.small, OMNIUS["accent"], (W // 2, 22), center=True,
                       glow_color=(*OMNIUS["accent"][:3], 60), glow_radius=3)
        draw_header_line(surface, OMNIUS["header_line"], 38, W)

        # Title
        draw_glow_text(surface, "AUTHORIZATION SEQUENCE", f.large, OMNIUS["logo"],
                       (W // 2, 60), center=True,
                       glow_color=(*OMNIUS["logo"][:3], 60), glow_radius=4)

        # Auth step lines
        base_y = 130
        lh     = f.medium.get_linesize() + 6

        for i, line in enumerate(self._lines_shown):
            is_last = (i == len(self._lines_shown) - 1)
            if line in ("ACCESS DENIED",):
                color = OMNIUS["error"]
            elif line in ("AUTHORIZATION ACCEPTED", "ACCESS PROFILE VERIFIED"):
                color = OMNIUS["ok"]
            elif line.startswith("LOADING"):
                color = OMNIUS["warning"]
            elif is_last:
                color = OMNIUS["accent"]
            else:
                color = OMNIUS["dim"]

            draw_glow_text(surface, line, f.medium, color,
                           (W // 2, base_y + i * lh), center=True)

        # Profile info (after success)
        if self._success and self._profile and len(self._lines_shown) >= 5:
            info_y = base_y + len(self._steps) * lh + 20
            draw_header_line(surface, OMNIUS["header_line"], info_y - 10, W)
            label = self._profile.get("label", "UNKNOWN SYSTEM")
            lvl   = self._profile.get("access_level", "UNKNOWN")
            node  = self._profile.get("node", "??-00")
            draw_glow_text(surface, f"DESTINATION : {label}", f.normal,
                           OMNIUS["text"], (W // 2, info_y + 10), center=True)
            draw_glow_text(surface, f"ACCESS LEVEL: {lvl}", f.normal,
                           OMNIUS["pink"], (W // 2, info_y + 38), center=True)
            draw_glow_text(surface, f"NODE        : {node}", f.normal,
                           OMNIUS["dim"], (W // 2, info_y + 66), center=True)

        draw_footer(surface, f.tiny, OMNIUS, NODE_ID,
                    auth="PENDING" if not self._success else "VERIFIED",
                    extra="")
        self._crt.draw(surface)
        self._flicker.apply(surface)
