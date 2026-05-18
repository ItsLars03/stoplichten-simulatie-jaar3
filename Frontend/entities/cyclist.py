"""Cyclist entity."""

import pygame

from config.constants import BICYCLE_COLOR, BICYCLE_SPEED
from entities.road_entity import RoadEntity


class Cyclist(RoadEntity):
    """Cyclist entity different from cars and buses"""

    def __init__(self, coords, keys):
        """Create a cyclist with bicycle speed and footprint."""
        super().__init__(coords, keys, BICYCLE_COLOR, BICYCLE_SPEED, (8, 16))

    def follow_gap(self, other):
        """Return the fixed cyclist following gap."""
        return 15

    def can_be_blocked_by(self, other):
        """Ignore pedestrians when checking for blockers."""
        from .pedestrian import Pedestrian

        return not isinstance(other, Pedestrian)

    def draw(self, surface):
        """Draw the cyclist as a compact rotated rectangle."""
        surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        pygame.draw.rect(surf, self.color, (0, 0, self.w - 5, self.h - 5), 0)
        rot = pygame.transform.rotate(surf, self.angle())
        rect = rot.get_rect(center=(int(self.pos[0]), int(self.pos[1])))
        surface.blit(rot, rect)

