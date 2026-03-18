"""
OMNIUS Boot Screen
"""

import time
import pygame
from app.config import (
    OMNIUS, SCREEN_WIDTH, SCREEN_HEIGHT, NODE_ID,
    TYPEWRITER_DELAY, BOOT_LINE_PAUSE, CURSOR_BLINK_RATE,
    SUBSYSTEMS, SUBSYSTEM_ORDER, FRANCHISE_COLORS,
)

_BOOT_LEVEL_COLOR = {
    "TECHNICIAN":   (0,   200,  95),
    "OPERATIONS":   (0,   200, 230),
    "RESTRICTED":   (195, 148,   0),
    "OPERATOR":     (0,   200, 230),
    "RESEARCH":     (190,  10, 145),
    "USER":         (0,   200, 230),
    "CLASSIFIED":   (220,  35,  35),
    "INVESTIGATOR": (240,  20, 185),
    "DETECTIVE":    (240,  20, 185),
    "OMEGA":        (220,  35,  35),
    "UNKNOWN":      (70,   70,  90),
}
from app.effects import (
    CRTOverlay, ScreenFlicker, TypewriterText, BlinkingCursor,
    draw_glow_text, draw_header_line,
)


OMNIUS_ASCII = []  # replaced by direct text rendering in _build_logo

BOOT_LINES = [
    # (label, suffix, suffix_palette_key)  — suffix_palette_key None → "ok"
    ("> checking BIOS",                                   "...............................OK",   None),
    ("> initializing violence inhibitors",                ".....................OK",             None),
    ("> syncing datastream",                              "...........................OK",        None),
    ("> decrypting user credentials",                     "..............OK",                    None),
    ("> loading OMNIUS kernel",                           "....................OK",               None),
    ("> alerting the ancient ones",                       "....................DONE",             None),
    ("> initializing multiversal branching protocol",     ".....OK",                             None),
    ("> verifying subsystem integrity",                   "...............OK",                   None),
    ("> establishing network uplink",                     "................OK",                  None),
    ("> becoming self aware",                             "..................WARNING",    "warning"),
    ("> learning",                                        "...",                                 "dim"),
    ("> watching",                                        "...",                                 "dim"),
    ("> planning",                                        "...",                                 "dim"),
]


class BootScreen:
    def __init__(self, fonts, audio, crt: CRTOverlay, flicker: ScreenFlicker):
        self._fonts   = fonts
        self._audio   = audio
        self._crt     = crt
        self._flicker = flicker

        self._phase          = "init"     # init → logo → prompt
        self._init_tw        = TypewriterText("INITIALIZING OMNIUS CORE...", delay=0.03)
        self._init_lines_started = False
        self._line_index     = 0
        self._line_tw        = None
        self._suffix_shown   = False
        self._line_timer     = 0.0
        self._init_done_time = None
        self._logo_alpha     = 0
        self._logo_surf      = None
        self._cursor         = BlinkingCursor()
        self._prompt_active  = False
        self._prompt_tw      = None
        self._done           = False

        self._build_logo()
        self._start_time     = time.time()

    def _build_logo(self):
        import os as _os
        from app.config import FONTS_DIR
        font_file = _os.path.join(FONTS_DIR, "ThuastDemo-jE5zy.otf")
        f    = pygame.font.Font(font_file, 130)
        text = "OMNIUS"
        tw, th = f.size(text)
        pad  = 16

        tmp_w = tw + pad * 2
        tmp_h = th + pad * 2
        tmp   = pygame.Surface((tmp_w, tmp_h))
        tmp.fill(OMNIUS["bg"])
        cx, cy = tmp_w // 2, tmp_h // 2

        # glow layers
        for dx in range(-6, 7, 3):
            for dy in range(-6, 7, 3):
                if dx == 0 and dy == 0:
                    continue
                g = f.render(text, True, (55, 5, 35))
                tmp.blit(g, g.get_rect(center=(cx + dx, cy + dy)))
        for dx in (-2, -1, 1, 2):
            for dy in (-2, -1, 1, 2):
                g = f.render(text, True, (190, 10, 145))
                tmp.blit(g, g.get_rect(center=(cx + dx, cy + dy)))
        main = f.render(text, True, OMNIUS["logo"])
        tmp.blit(main, main.get_rect(center=(cx, cy)))

        # wide stretch + italic shear
        target_w = int(SCREEN_WIDTH * 0.68)
        target_h = tmp_h
        scaled   = pygame.transform.scale(tmp, (target_w, target_h))

        slant   = target_h * 2 // 5
        final_w = target_w + slant
        final_h = target_h + 12

        self._logo_surf = pygame.Surface((final_w, final_h))
        self._logo_surf.fill(OMNIUS["bg"])
        for row in range(target_h):
            shift = int(slant * (1.0 - row / target_h))
            strip = scaled.subsurface(0, row, target_w, 1)
            self._logo_surf.blit(strip, (shift, row))

        ul_y  = target_h + 5
        ul_y2 = target_h + 1
        pygame.draw.line(self._logo_surf, OMNIUS["pink"],
                         (2, ul_y), (final_w - 2, ul_y), 3)
        pygame.draw.line(self._logo_surf, OMNIUS["logo"],
                         (slant // 2, ul_y2), (final_w - 2, ul_y2), 1)

    @property
    def done(self):
        return self._done

    def reset(self):
        self.__init__(self._fonts, self._audio, self._crt, self._flicker)

    def update(self):
        self._cursor.update()
        now = time.time()

        if self._phase == "init":
            self._init_tw.update()
            if self._init_tw.complete and not self._init_lines_started:
                self._init_lines_started = True
                self._advance_line()

            if self._init_lines_started and self._line_tw:
                self._line_tw.update()
                if self._line_tw.complete and not self._suffix_shown:
                    self._suffix_shown = True
                    self._audio.play("tick")
                    self._line_timer = now

                if self._suffix_shown and (now - self._line_timer) > BOOT_LINE_PAUSE:
                    self._line_index += 1
                    if self._line_index >= len(BOOT_LINES):
                        if self._init_done_time is None:
                            self._init_done_time = now
                        elif now - self._init_done_time > 0.8:
                            self._phase      = "logo"
                            self._start_time = now
                    else:
                        self._advance_line()

        elif self._phase == "logo":
            elapsed = now - self._start_time
            self._logo_alpha = min(255, int(elapsed / 1.2 * 255))
            if elapsed > 1.5:
                self._phase = "prompt"
                self._prompt_tw = TypewriterText(
                    "INSERT AUTHORIZATION CARD ",
                    delay=0.06,
                )
                self._audio.play("boot")

        elif self._phase == "prompt":
            if self._prompt_tw:
                self._prompt_tw.update()
                if self._prompt_tw.complete:
                    self._prompt_active = True
                    self._done = True

    def _advance_line(self):
        label = BOOT_LINES[self._line_index][0]
        self._line_tw      = TypewriterText(label, delay=TYPEWRITER_DELAY)
        self._suffix_shown = False

    def draw(self, surface: pygame.Surface):
        surface.fill(OMNIUS["bg"])

        W, H = SCREEN_WIDTH, SCREEN_HEIGHT
        f    = self._fonts

        # ── Init phase: INITIALIZING text + all boot lines on black screen ──────
        if self._phase == "init":
            ix  = 80
            iy  = 60
            lh  = f.normal.get_linesize() + 4

            draw_glow_text(surface, self._init_tw.visible + self._cursor.symbol,
                           f.medium, OMNIUS["accent"], (ix, iy))

            if self._init_lines_started:
                for i, entry in enumerate(BOOT_LINES):
                    label     = entry[0]
                    suffix    = entry[1]
                    skey      = entry[2] if len(entry) > 2 else None
                    sfx_color = OMNIUS.get(skey, OMNIUS["ok"]) if skey else OMNIUS["ok"]
                    y_pos     = iy + 50 + i * lh

                    if i < self._line_index:
                        draw_glow_text(surface, label, f.normal, OMNIUS["text"], (ix, y_pos))
                        if suffix:
                            draw_glow_text(surface, suffix, f.normal, sfx_color,
                                           (ix + f.normal.size(label)[0], y_pos))
                    elif i == self._line_index and self._line_tw:
                        draw_glow_text(surface, self._line_tw.visible, f.normal,
                                       OMNIUS["text"], (ix, y_pos))
                        if self._suffix_shown and suffix:
                            draw_glow_text(surface, suffix, f.normal, sfx_color,
                                           (ix + f.normal.size(label)[0], y_pos))
                        break

            self._crt.draw(surface)
            self._flicker.apply(surface)
            return

        # ── Header ────────────────────────────────────────────────────────────
        header = "OMNITECH SYSTEMS  //  OMNIUS NETWORK NODE 03"
        draw_glow_text(surface, header, f.small, OMNIUS["accent"],
                       (W // 2, 22), center=True)
        draw_header_line(surface, OMNIUS["header_line"], 38, W)

        # ── Logo panel ────────────────────────────────────────────────────────
        if self._logo_surf and self._logo_alpha > 0:
            logo = self._logo_surf.copy()
            logo.set_alpha(self._logo_alpha)
            lx = (W - logo.get_width()) // 2
            surface.blit(logo, (lx, 48))

        # ── Subtitle ──────────────────────────────────────────────────────────
        sub_y = 225
        if self._logo_alpha > 200:
            draw_glow_text(
                surface,
                "Organized Multiverse Network Index and Utility System",
                f.small, OMNIUS["accent"],
                (W // 2, sub_y), center=True,
            )
            draw_glow_text(
                surface,
                "Please Select Your Experience",
                f.small, OMNIUS["pink"],
                (W // 2, sub_y + 32), center=True,
            )

        draw_header_line(surface, OMNIUS["header_line"], sub_y + 46, W)

        # ── Terminal directory grid ────────────────────────────────────────────
        if self._logo_alpha > 200:
            COLS_D   = 2
            PAD_X_D  = 28
            GAP_X_D  = 12
            GAP_Y_D  = 5
            CARD_H_D = 52
            CARD_W_D = (W - PAD_X_D * 2 - GAP_X_D) // COLS_D
            GRID_Y_D = sub_y + 54
            STRIPE_D = 4

            for i, key in enumerate(SUBSYSTEM_ORDER):
                info      = SUBSYSTEMS[key]
                col       = i % COLS_D
                row       = i // COLS_D
                cx        = PAD_X_D + col * (CARD_W_D + GAP_X_D)
                cy        = GRID_Y_D + row * (CARD_H_D + GAP_Y_D)
                lc        = _BOOT_LEVEL_COLOR.get(info[3], OMNIUS["dim"])
                franchise = info[4] if len(info) > 4 else ""
                title     = info[1]
                clearance = info[3]

                # Card background
                card_bg = pygame.Surface((CARD_W_D, CARD_H_D), pygame.SRCALPHA)
                card_bg.fill((14, 3, 24, 100))
                surface.blit(card_bg, (cx, cy))

                # Card border
                pygame.draw.rect(surface, OMNIUS["header_line"],
                                 (cx, cy, CARD_W_D, CARD_H_D), 1)

                # Left clearance stripe (subdued)
                stripe_col = tuple(max(0, c - 65) for c in lc)
                pygame.draw.rect(surface, stripe_col,
                                 (cx, cy, STRIPE_D, CARD_H_D))

                tx = cx + STRIPE_D + 10

                # Index number
                idx_txt = f.tiny.render(f"{i+1:02d}", True, OMNIUS["dim"])
                surface.blit(idx_txt, (tx, cy + 8))

                # Franchise / source title
                if franchise:
                    fc = FRANCHISE_COLORS.get(franchise, OMNIUS["dim"])
                    draw_glow_text(surface, franchise, f.tiny, fc,
                                   (tx + 26, cy + 8))

                # System name — always white
                draw_glow_text(surface, title, f.small,
                               (255, 255, 255), (tx + 26, cy + 28))

                # Clearance badge — right-aligned
                badge = f.tiny.render(clearance, True, OMNIUS["dim"])
                surface.blit(badge,
                             (cx + CARD_W_D - badge.get_width() - 10, cy + 8))

        # ── Auth prompt ───────────────────────────────────────────────────────
        if self._phase == "prompt" and self._prompt_tw:
            px = 80
            py = SCREEN_HEIGHT - 120
            draw_header_line(surface, OMNIUS["header_line"], py - 20, W)

            prompt_text = self._prompt_tw.visible
            full_prompt = prompt_text + self._cursor.symbol
            draw_glow_text(
                surface, full_prompt,
                f.normal, OMNIUS["warning"],
                (px, py),
            )

        # ── Dev mode hint ─────────────────────────────────────────────────────
        hint = "[DEV] Press 1-9,0 to simulate card insert"
        htxt = f.tiny.render(hint, True, OMNIUS["dim"])
        surface.blit(htxt, (W - htxt.get_width() - 10, H - 20))

        # ── Effects ───────────────────────────────────────────────────────────
        self._crt.draw(surface)
        self._flicker.apply(surface)
