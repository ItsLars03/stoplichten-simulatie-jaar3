"""Pedestrian entity."""

import pygame

from config.constants import PEDESTRIAN_COLOR, PEDESTRIAN_SPEED
from entities.road_entity import RoadEntity


class Pedestrian(RoadEntity):
    """Pedestrian entity different from cars and buses"""

    def __init__(self, coords, keys):
        """Create a pedestrian with a small square footprint."""
        super().__init__(coords, keys, PEDESTRIAN_COLOR, PEDESTRIAN_SPEED, (6, 6))

    def follow_gap(self, other):
        """Return the fixed pedestrian following gap."""
        return 12

    def can_be_blocked_by(self, other):
        """Ignore cyclists when checking for blockers."""
        from .cyclist import Cyclist

        return not isinstance(other, Cyclist)

    def signal_stop_distance(self):
        """Use a tiny threshold so pedestrians wait at the sensor."""
        return 8

    def snap_to_signal_stop(self):
        """Snap pedestrians exactly onto signal sensors when waiting."""
        return True

    def draw(self, surface):
        """Draw the pedestrian as a simple centered square."""
        x, y = int(self.pos[0]), int(self.pos[1])
        pygame.draw.rect(surface, self.color, (x - 3, y - 3, 6, 6))

