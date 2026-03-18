"""
OMNIUS Master Index (main menu)
"""

import pygame
from app.config import (
    OMNIUS, SCREEN_WIDTH, SCREEN_HEIGHT, NODE_ID,
    SUBSYSTEMS, SUBSYSTEM_ORDER, FRANCHISE_COLORS,
)
from app.effects import (
    CRTOverlay, ScreenFlicker, BlinkingCursor,
    draw_glow_text, draw_header_line, draw_footer,
)


# Placeholder for future terminals not yet implemented
FUTURE_SLOTS = [
    ("CLASSIFIED",    "RESTRICTED ARCHIVES",   "Higher clearance required",              "OMEGA"),
    ("EXPERIMENTAL",  "EXPERIMENTAL NODES",    "Unstable systems — access at own risk",  "UNKNOWN"),
]

# Left stripe accent colour keyed by clearance level
_LEVEL_COLOR = {
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

COLS = 2   # card grid columns


class MasterMenu:
    def __init__(self, fonts, audio, crt: CRTOverlay, flicker: ScreenFlicker):
        self._fonts    = fonts
        self._audio    = audio
        self._crt      = crt
        self._flicker  = flicker
        self._cursor   = BlinkingCursor()
        self._sel      = 0
        self._profile  = None

        # Build available entries
        self._entries  = []
        for key in SUBSYSTEM_ORDER:
            info = SUBSYSTEMS[key]
            self._entries.append({
                "key":       key,
                "index":     f"[{len(self._entries) + 1:02d}]",
                "title":     info[1],
                "desc":      info[2],
                "level":     info[3],
                "franchise": info[4] if len(info) > 4 else "",
                "available": True,
            })

        self._n_avail = len(self._entries)

        # Future / locked slots
        for slot in FUTURE_SLOTS:
            self._entries.append({
                "key":   None,
                "index": f"[{len(self._entries) + 1:02d}]",
                "title": slot[1],
                "desc":  slot[2],
                "level": slot[3],
                "available": False,
                "label": slot[0],
            })

        self._n_locked        = len(self._entries) - self._n_avail
        self._selected_system = None

    # ── Properties ────────────────────────────────────────────────────────────

    @property
    def selected_system(self):
        return self._selected_system

    def set_profile(self, profile: dict):
        self._profile = profile
        self._sel     = 0
        self._selected_system = None

    # ── Navigation ────────────────────────────────────────────────────────────

    def nav_up(self):
        if self._sel < self._n_avail:
            new = self._sel - COLS
            if new < 0:
                # Wrap into locked row at same column (clamped)
                self._sel = self._n_avail + min(self._sel % COLS, self._n_locked - 1)
            else:
                self._sel = new
        else:
            # Locked → last grid row, same column (clamped)
            col = (self._sel - self._n_avail) % COLS
            last_row_base = ((self._n_avail - 1) // COLS) * COLS
            self._sel = min(last_row_base + col, self._n_avail - 1)
        self._audio.play("tick")

    def nav_down(self):
        if self._sel < self._n_avail:
            new = self._sel + COLS
            if new >= self._n_avail:
                # Wrap into locked row at same column (clamped)
                self._sel = self._n_avail + min(self._sel % COLS, self._n_locked - 1)
            else:
                self._sel = new
        else:
            # Locked → first grid row, same column (clamped)
            col = (self._sel - self._n_avail) % COLS
            self._sel = min(col, self._n_avail - 1)
        self._audio.play("tick")

    def nav_left(self):
        if self._sel < self._n_avail:
            if self._sel % COLS > 0:
                self._sel -= 1
                self._audio.play("tick")
        else:
            if self._sel > self._n_avail:
                self._sel -= 1
                self._audio.play("tick")

    def nav_right(self):
        if self._sel < self._n_avail:
            if self._sel % COLS < COLS - 1 and self._sel + 1 < self._n_avail:
                self._sel += 1
                self._audio.play("tick")
        else:
            if self._sel < len(self._entries) - 1:
                self._sel += 1
                self._audio.play("tick")

    def confirm(self) -> str | None:
        entry = self._entries[self._sel]
        if not entry["available"]:
            self._audio.play("denied")
            return None
        self._audio.play("select")
        self._selected_system = entry["key"]
        return entry["key"]

    def update(self):
        self._cursor.update()

    # ── Draw ──────────────────────────────────────────────────────────────────

    def draw(self, surface: pygame.Surface):
        surface.fill(OMNIUS["bg"])
        W, H = SCREEN_WIDTH, SCREEN_HEIGHT
        f    = self._fonts

        # ── Header ────────────────────────────────────────────────────────────
        draw_glow_text(surface, "OMNITECH SYSTEMS  //  OMNIUS NETWORK NODE 03",
                       f.small, OMNIUS["accent"], (W // 2, 20), center=True)
        draw_header_line(surface, OMNIUS["header_line"], 36, W)

        draw_glow_text(surface, "Please Select Your Experience",
                       f.large, OMNIUS["logo"], (W // 2, 52), center=True)
        draw_glow_text(surface, "// AUTHORIZED ACCESS ONLY //",
                       f.small, OMNIUS["pink"], (W // 2, 88), center=True)
        draw_header_line(surface, OMNIUS["header_line"], 106, W)

        # ── Card grid (available entries) ─────────────────────────────────────
        PAD_X  = 28
        GAP_X  = 12
        GAP_Y  = 6
        CARD_H = 80
        CARD_W = (W - PAD_X * 2 - GAP_X) // COLS
        GRID_Y = 114
        STRIPE = 5   # left accent stripe width

        for idx in range(self._n_avail):
            entry     = self._entries[idx]
            col       = idx % COLS
            row       = idx // COLS
            cx        = PAD_X + col * (CARD_W + GAP_X)
            cy        = GRID_Y + row * (CARD_H + GAP_Y)
            is_sel    = (idx == self._sel)
            lc        = _LEVEL_COLOR.get(entry["level"], OMNIUS["dim"])
            franchise = entry.get("franchise", "")

            # Card background
            bg = pygame.Surface((CARD_W, CARD_H), pygame.SRCALPHA)
            bg.fill((70, 0, 90, 75) if is_sel else (16, 4, 28, 90))
            surface.blit(bg, (cx, cy))

            # Border
            pygame.draw.rect(surface,
                             OMNIUS["logo"] if is_sel else OMNIUS["header_line"],
                             (cx, cy, CARD_W, CARD_H), 2 if is_sel else 1)

            # Top highlight on selected
            if is_sel:
                pygame.draw.line(surface, OMNIUS["pink"],
                                 (cx + 1, cy + 1), (cx + CARD_W - 2, cy + 1), 1)

            # Left clearance stripe
            stripe_col = lc if is_sel else tuple(max(0, c - 60) for c in lc)
            pygame.draw.rect(surface, stripe_col, (cx, cy, STRIPE, CARD_H))

            text_x = cx + STRIPE + 10

            # Franchise name (top line)
            if franchise:
                fc = FRANCHISE_COLORS.get(franchise, OMNIUS["dim"])
                draw_glow_text(surface, franchise, f.tiny, fc,
                               (text_x, cy + 7))

            # System title (middle line) — always white
            draw_glow_text(surface, entry["title"], f.normal,
                           (255, 255, 255),
                           (text_x, cy + 26))

            # Description (bottom line)
            draw_glow_text(surface, entry["desc"], f.tiny, OMNIUS["dim"],
                           (text_x, cy + 58))

            # Clearance badge (top-right corner)
            badge = f.tiny.render(entry["level"], True,
                                  lc if is_sel else OMNIUS["dim"])
            surface.blit(badge, (cx + CARD_W - badge.get_width() - 10, cy + 7))

        # ── Locked entries strip ───────────────────────────────────────────────
        rows_used   = (self._n_avail + COLS - 1) // COLS
        locked_y    = GRID_Y + rows_used * (CARD_H + GAP_Y) + 6
        draw_header_line(surface, OMNIUS["header_line"], locked_y - 2, W)
        locked_y   += 10

        lock_gap    = 10
        lock_card_w = (W - PAD_X * 2 - lock_gap * (self._n_locked - 1)) // self._n_locked
        lock_card_h = 50

        for li in range(self._n_locked):
            gi     = self._n_avail + li
            entry  = self._entries[gi]
            cx     = PAD_X + li * (lock_card_w + lock_gap)
            is_sel = (gi == self._sel)

            bg = pygame.Surface((lock_card_w, lock_card_h), pygame.SRCALPHA)
            bg.fill((40, 0, 55, 50) if is_sel else (10, 3, 18, 70))
            surface.blit(bg, (cx, locked_y))

            pygame.draw.rect(surface,
                             OMNIUS["header_line"] if is_sel else (40, 20, 55),
                             (cx, locked_y, lock_card_w, lock_card_h),
                             2 if is_sel else 1)

            # Dim left stripe
            pygame.draw.rect(surface, (50, 20, 50),
                             (cx, locked_y, STRIPE, lock_card_h))

            label = entry.get("label", entry["title"])
            draw_glow_text(surface, label, f.small,
                           OMNIUS["text"] if is_sel else OMNIUS["dim"],
                           (cx + lock_card_w // 2, locked_y + 12), center=True)

            lock_txt = f.tiny.render("[LOCKED]", True, OMNIUS["dim"])
            surface.blit(lock_txt,
                         (cx + lock_card_w // 2 - lock_txt.get_width() // 2,
                          locked_y + 32))

        # ── Prompt ────────────────────────────────────────────────────────────
        prompt = f"SELECT DESTINATION {self._cursor.symbol}"
        draw_glow_text(surface, prompt, f.medium, OMNIUS["warning"],
                       (PAD_X, H - 80))

        nav_hint = "\u2191\u2193\u2190\u2192  navigate    ENTER  confirm    ESC  logout"
        draw_glow_text(surface, nav_hint, f.tiny, OMNIUS["dim"],
                       (W - f.tiny.size(nav_hint)[0] - 10, H - 60))

        draw_footer(surface, f.tiny, OMNIUS, NODE_ID,
                    auth="VERIFIED", extra="ESC: LOGOUT")
        self._crt.draw(surface)
        self._flicker.apply(surface)
