"""Car entity."""

from config.constants import CAR_SPEED
from entities.road_entity import RoadEntity


class Car(RoadEntity):
    """Car entity"""

    def __init__(self, coords, keys, color):
        """Create a car with the configured car speed and size."""
        super().__init__(coords, keys, color, CAR_SPEED, (10, 18))

