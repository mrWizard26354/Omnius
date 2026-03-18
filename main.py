#!/usr/bin/env python3
"""
OMNIUS Terminal
OmniTech Systems Division

Entry point.
"""

import sys
import os

# Allow running from any working directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pygame

from app.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, FULLSCREEN,
    OMNIUS, PALETTES, NODE_ID,
    STATE_BOOT, STATE_WAITING_FOR_CARD, STATE_AUTHENTICATING,
    STATE_MASTER_MENU, STATE_SUBSYSTEM, STATE_ERROR,
)
from app.state_manager  import StateManager
from app.card_input     import CardInputProvider
from app.input_manager  import InputManager
from app.renderer       import FontSet
from app.audio          import AudioManager
from app.effects        import CRTOverlay, ScreenFlicker, draw_glow_text, draw_header_line

from systems.boot_screen  import BootScreen
from systems.auth_screen  import AuthScreen
from systems.master_menu  import MasterMenu

# ── Subsystem imports ─────────────────────────────────────────────────────────
from systems.ghostbusters  import GhostbustersTerminal
from systems.ingen         import InGenTerminal
from systems.skynet        import SkynetTerminal
from systems.zion          import ZionTerminal
from systems.umbrella      import UmbrellaTerminal
from systems.tron          import TronTerminal
from systems.wopr          import WOPRTerminal
from systems.event_horizon import EventHorizonTerminal
from systems.blade_runner  import BladeRunnerTerminal
from systems.precrime      import PreCrimeTerminal


SUBSYSTEM_MAP = {
    "ghostbusters":  (GhostbustersTerminal,  "ghostbusters"),
    "ingen":         (InGenTerminal,          "ingen"),
    "skynet":        (SkynetTerminal,         "skynet"),
    "zion":          (ZionTerminal,           "zion"),
    "umbrella":      (UmbrellaTerminal,       "umbrella"),
    "tron":          (TronTerminal,           "tron"),
    "wopr":          (WOPRTerminal,           "wopr"),
    "event_horizon": (EventHorizonTerminal,   "event_horizon"),
    "blade_runner":  (BladeRunnerTerminal,    "blade_runner"),
    "precrime":      (PreCrimeTerminal,       "precrime"),
}


class OmniusApp:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("OMNIUS — OmniTech Systems Division")

        flags = pygame.FULLSCREEN | pygame.SCALED if FULLSCREEN else pygame.RESIZABLE
        self._screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT), flags
        )
        self._clock  = pygame.time.Clock()

        # Core components
        self._fonts   = FontSet()
        self._audio   = AudioManager()
        self._crt     = CRTOverlay(SCREEN_WIDTH, SCREEN_HEIGHT)
        self._flicker = ScreenFlicker()
        self._state   = StateManager()
        self._input   = InputManager()
        self._cards   = CardInputProvider()

        # Screens
        self._boot_screen  = BootScreen(self._fonts, self._audio, self._crt, self._flicker)
        self._auth_screen  = AuthScreen(self._fonts, self._audio, self._crt, self._flicker)
        self._master_menu  = MasterMenu(self._fonts, self._audio, self._crt, self._flicker)
        self._active_sub   = None

        # Error state
        self._error_timer  = 0.0

    # ── Main loop ─────────────────────────────────────────────────────────────

    def run(self):
        running = True
        while running:
            dt = self._clock.tick(FPS) / 1000.0

            events = self._input.process()

            for ev in events:
                if ev.type == "quit":
                    running = False
                elif ev.type == "fullscreen":
                    self._toggle_fullscreen()
                else:
                    self._handle_event(ev)

            self._update(dt)
            self._draw()
            pygame.display.flip()

        pygame.quit()

    def _toggle_fullscreen(self):
        flags = pygame.FULLSCREEN | pygame.SCALED
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)

    # ── Event routing ─────────────────────────────────────────────────────────

    def _handle_event(self, ev):
        s = self._state.state

        if s == STATE_BOOT:
            # Any key skips boot animation after it starts
            if ev.type in ("confirm", "char", "card_sim"):
                if self._boot_screen.done:
                    self._state.boot_complete()
                else:
                    pass   # let animation play

        elif s == STATE_WAITING_FOR_CARD:
            if ev.type == "card_sim":
                self._insert_card(ev.char)

        elif s == STATE_AUTHENTICATING:
            pass   # handled in update

        elif s == STATE_MASTER_MENU:
            if ev.type == "nav":
                if ev.key == "up":
                    self._master_menu.nav_up()
                elif ev.key == "down":
                    self._master_menu.nav_down()
                elif ev.key == "left":
                    self._master_menu.nav_left()
                elif ev.key == "right":
                    self._master_menu.nav_right()
            elif ev.type == "confirm":
                key = self._master_menu.confirm()
                if key:
                    self._launch_subsystem(key)
            elif ev.type == "back":
                # Logout — return to boot
                self._state.return_to_boot()
                self._boot_screen.reset()

        elif s == STATE_SUBSYSTEM:
            if self._active_sub:
                if ev.type == "nav":
                    if ev.key == "up":
                        self._active_sub.nav_up()
                    elif ev.key == "down":
                        self._active_sub.nav_down()
                elif ev.type == "confirm":
                    self._active_sub.confirm()
                elif ev.type == "back":
                    self._active_sub.back()

        elif s == STATE_ERROR:
            if ev.type in ("confirm", "back", "card_sim"):
                self._state.clear_error()
                self._boot_screen.reset()
                self._state.return_to_boot()

    # ── Card handling ─────────────────────────────────────────────────────────

    def _insert_card(self, key_char: str):
        card_id = self._cards.get_sim_card_id(key_char)
        if not card_id:
            return
        profile = self._cards.map_card_to_profile(card_id)
        if profile:
            self._state.card_inserted(profile)
            self._auth_screen.start(profile)
            self._master_menu.set_profile(profile)
        else:
            self._state.card_inserted(None)
            self._auth_screen.start(None)

    def _launch_subsystem(self, key: str):
        if key not in SUBSYSTEM_MAP:
            return
        cls, palette_key = SUBSYSTEM_MAP[key]
        palette = PALETTES.get(palette_key, PALETTES["skynet"])
        self._active_sub = cls(
            self._fonts, self._audio, self._crt, self._flicker, palette
        )
        self._state.select_subsystem(key)
        self._audio.play("open")

    # ── Update ────────────────────────────────────────────────────────────────

    def _update(self, dt: float):
        s = self._state.state

        if s == STATE_BOOT:
            self._boot_screen.update()
            if self._boot_screen.done:
                self._state.boot_complete()

        elif s == STATE_AUTHENTICATING:
            self._auth_screen.update()
            if self._auth_screen.done:
                if self._auth_screen.success:
                    self._state.auth_complete()
                else:
                    self._state.auth_failed()

        elif s == STATE_MASTER_MENU:
            self._master_menu.update()

        elif s == STATE_SUBSYSTEM:
            if self._active_sub:
                self._active_sub.update()
                if self._active_sub.exit_requested:
                    self._active_sub = None
                    self._state.exit_subsystem()

        elif s == STATE_ERROR:
            import time
            if not hasattr(self, "_err_start"):
                self._err_start = __import__("time").time()
            if __import__("time").time() - self._err_start > 4.0:
                del self._err_start
                self._state.clear_error()
                self._state.return_to_boot()
                self._boot_screen.reset()

    # ── Draw ──────────────────────────────────────────────────────────────────

    def _draw(self):
        s = self._state.state

        if s == STATE_BOOT:
            self._boot_screen.draw(self._screen)

        elif s == STATE_WAITING_FOR_CARD:
            self._boot_screen.draw(self._screen)   # same screen, boot fully done

        elif s == STATE_AUTHENTICATING:
            self._auth_screen.draw(self._screen)

        elif s == STATE_MASTER_MENU:
            self._master_menu.draw(self._screen)

        elif s == STATE_SUBSYSTEM:
            if self._active_sub:
                self._active_sub.draw(self._screen)

        elif s == STATE_ERROR:
            self._draw_error()

    def _draw_error(self):
        self._screen.fill(OMNIUS["bg"])
        W, H = SCREEN_WIDTH, SCREEN_HEIGHT
        f    = self._fonts

        draw_glow_text(
            self._screen, "ACCESS DENIED",
            f.huge, OMNIUS["error"],
            (W // 2, H // 2 - 60), center=True,
            glow_color=OMNIUS["error"], glow_radius=8,
        )
        msg = self._state.error_msg or "UNRECOGNIZED AUTHORIZATION PROFILE"
        draw_glow_text(
            self._screen, msg,
            f.medium, OMNIUS["warning"],
            (W // 2, H // 2 + 20), center=True,
        )
        draw_glow_text(
            self._screen, "PRESS ANY KEY TO RETRY",
            f.small, OMNIUS["dim"],
            (W // 2, H // 2 + 70), center=True,
        )
        self._crt.draw(self._screen)
        self._flicker.apply(self._screen)


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = OmniusApp()
    app.run()
