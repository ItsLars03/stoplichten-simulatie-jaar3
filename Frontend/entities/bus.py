"""Bus entity."""

import pygame

from config.constants import BUS_COLOR, CAR_SPEED
from entities.car import Car


class Bus(Car):
    """Bus entity vehicle, slightly different from car"""

    def __init__(self, coords, keys):
        """Create a bus with the configured bus color and larger footprint."""
        super().__init__(coords, keys, BUS_COLOR)
        self.w, self.h = 13, 34

    def draw(self, surface):
        """Draw the bus as a larger rotated rectangle."""
        surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        pygame.draw.rect(surf, self.color, (0, 0, self.w, self.h), border_radius=3)
        rot = pygame.transform.rotate(surf, self.angle())
        rect = rot.get_rect(center=(int(self.pos[0]), int(self.pos[1])))
        surface.blit(rot, rect)

