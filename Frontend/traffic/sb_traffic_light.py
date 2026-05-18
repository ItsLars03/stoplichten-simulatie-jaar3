"""Railway warning light rendering."""

import pygame

from config.constants import BLINK_RED, DARK_GRAY, GRAY, WHITE


class SbTrafficLight:
    """The trafficlights signaling the arrival of tge train.
    with a red blinking state when the train is approaching."""

    def __init__(self, definition):
        """Create a railway warning light from a dictionary definition."""
        self.id = definition["id"]
        self.pos = definition["pos"]
        self.signal_state = 0
        self.blinking_active = False
        self._blink_t = 0.0

    def update(self, dt):
        """Advance the blink timer."""
        self._blink_t += dt

    def draw(self, surface, font):
        """Draw the traffic light and the sb label for it"""
        x, y = self.pos
        pygame.draw.rect(surface, DARK_GRAY, (x - 7, y - 18, 14, 36), border_radius=3)
        if self.blinking_active:
            lit = int(self._blink_t / 0.4) % 2 == 0
            col = BLINK_RED if lit else GRAY
        else:
            col = GRAY
        pygame.draw.circle(surface, col, (x, y), 5)
        label = font.render("sb", True, WHITE)
        surface.blit(label, (x - label.get_width() // 2, y + 20))

