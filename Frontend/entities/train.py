"""Train entity."""

import pygame

from config.constants import (
    TRAIN_CARS,
    TRAIN_COL,
    TRAIN_EXIT_X,
    TRAIN_GAP,
    TRAIN_H,
    TRAIN_SPAWN_X,
    TRAIN_SPEED,
    TRAIN_TOTAL_W,
    TRAIN_W,
)


class Train:
    """Train entity; behaves differently from the rest of the entities.
    Has its own logic for movement."""

    def __init__(self, y, direction=1):
        """Create a train on track ``y`` moving in ``direction``."""
        self.y = y
        self.direction = direction
        self.x = float(TRAIN_SPAWN_X if direction > 0 else TRAIN_EXIT_X)
        self.done = False

    def update(self, dt):
        """Advance the train and mark it done after it leaves the screen."""
        self.x += TRAIN_SPEED * dt * self.direction
        if self.direction > 0 and self.x > TRAIN_EXIT_X + TRAIN_TOTAL_W:
            self.done = True
        elif self.direction < 0 and self.x < TRAIN_SPAWN_X:
            self.done = True

    def draw(self, surface):
        """Draw the train cars; can be multiple for astetic purposes."""
        for i in range(TRAIN_CARS):
            cx = self.x + i * (TRAIN_W + TRAIN_GAP)
            rect = pygame.Rect(int(cx), self.y - TRAIN_H // 2, TRAIN_W, TRAIN_H)
            pygame.draw.rect(surface, TRAIN_COL, rect, border_radius=4)
