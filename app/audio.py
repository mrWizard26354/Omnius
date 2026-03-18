"""
OMNIUS Audio Manager
Procedural tone generation — no external audio files required.
"""

import math
import array
import pygame


_SAMPLE_RATE = 44100
_CHANNELS    = 1


def _generate_tone(freq: float, duration: float, volume: float = 0.3,
                   wave: str = "sine", fade_ms: int = 30) -> pygame.mixer.Sound:
    """Generate a tone as a pygame Sound object."""
    n_samples = int(_SAMPLE_RATE * duration)
    buf       = array.array("h", [0] * n_samples)

    for i in range(n_samples):
        t = i / _SAMPLE_RATE
        if wave == "sine":
            val = math.sin(2 * math.pi * freq * t)
        elif wave == "square":
            val = 1.0 if math.sin(2 * math.pi * freq * t) >= 0 else -1.0
        elif wave == "sawtooth":
            val = 2 * (t * freq - math.floor(t * freq + 0.5))
        else:
            val = math.sin(2 * math.pi * freq * t)

        # Fade in/out
        fade_n = int(_SAMPLE_RATE * fade_ms / 1000)
        if i < fade_n:
            val *= i / fade_n
        elif i > n_samples - fade_n:
            val *= (n_samples - i) / fade_n

        buf[i] = int(val * volume * 32767)

    sound = pygame.sndarray.make_sound(
        pygame.surfarray.pixels_red(
            pygame.Surface((1, 1))
        ).__class__  # just to get the type right
    ) if False else None

    # Use the direct array approach
    import numpy as np
    arr = np.array(buf, dtype=np.int16)
    if _CHANNELS == 2:
        arr = np.column_stack([arr, arr])
    sound = pygame.sndarray.make_sound(arr)
    return sound


class AudioManager:
    """Manages all sounds for OMNIUS."""

    def __init__(self):
        self._enabled = False
        self._sounds  = {}
        self._init()

    def _init(self):
        try:
            pygame.mixer.init(frequency=_SAMPLE_RATE, size=-16,
                              channels=2, buffer=512)
            self._enabled = True
            self._build_sounds()
        except Exception:
            self._enabled = False

    def _build_sounds(self):
        try:
            import numpy as np
            self._sounds = {
                "boot":     self._tone(440, 0.12, wave="sine"),
                "tick":     self._tone(880, 0.04, volume=0.15, wave="square"),
                "accept":   self._tone(660, 0.18, wave="sine"),
                "denied":   self._tone(180, 0.30, wave="square"),
                "select":   self._tone(520, 0.06, wave="sine"),
                "warning":  self._tone(320, 0.22, wave="square"),
                "open":     self._tone(550, 0.20, wave="sine"),
            }
        except Exception:
            self._enabled = False

    def _tone(self, freq: float, duration: float,
              volume: float = 0.3, wave: str = "sine") -> pygame.mixer.Sound | None:
        try:
            import numpy as np
            n  = int(_SAMPLE_RATE * duration)
            t  = np.linspace(0, duration, n, endpoint=False)
            if wave == "sine":
                data = np.sin(2 * np.pi * freq * t)
            elif wave == "square":
                data = np.sign(np.sin(2 * np.pi * freq * t))
            else:
                data = np.sin(2 * np.pi * freq * t)

            # Fade
            fade = min(int(0.03 * _SAMPLE_RATE), n // 4)
            data[:fade]  *= np.linspace(0, 1, fade)
            data[-fade:] *= np.linspace(1, 0, fade)

            data = (data * volume * 32767).astype(np.int16)
            stereo = np.column_stack([data, data])
            return pygame.sndarray.make_sound(stereo)
        except Exception:
            return None

    def play(self, name: str):
        if not self._enabled:
            return
        sound = self._sounds.get(name)
        if sound:
            try:
                sound.play()
            except Exception:
                pass
