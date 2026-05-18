"""Animated railway barriers."""

import math

import pygame

from config.constants import (
    BARRIER_ANIM_SECONDS,
    BARRIER_ARM,
    BARRIER_POST,
    DARK_GRAY,
    RED_C,
)
from config.geometry import (
    BARRIER_ARM_LEN,
    BARRIER_LEFT_X,
    BARRIER_RIGHT_X,
    BARRIER_YS,
    pt
)


class RailwayBarriers:
    """Animated crossing barriers that open and close near the tracks."""

    def __init__(self):
        """Create barriers in the fully open state."""
        self.progress = 0.0

    def update(self, dt, should_lower):
        """Move the barrier animation toward lowered or opened state."""
        step = dt / BARRIER_ANIM_SECONDS
        if should_lower:
            self.progress = min(1.0, self.progress + step)
        else:
            self.progress = max(0.0, self.progress - step)

    def is_open(self):
        """Return whether the barriers are effectively open."""
        return self.progress <= 0.001

    def _arm_endpoint(self, pivot, side):
        """Return the endpoint of a barrier arm for the current progress."""
        start_angle = -90
        end_angle = 0 if side == "left" else -180
        angle = math.radians(start_angle + (end_angle - start_angle) * self.progress)
        return (
            pivot[0] + math.cos(angle) * BARRIER_ARM_LEN,
            pivot[1] + math.sin(angle) * BARRIER_ARM_LEN,
        )

    def _draw_arm(self, surface, pivot, side):
        """Draw a single striped barrier arm."""
        end = self._arm_endpoint(pivot, side)
        pygame.draw.circle(surface, BARRIER_POST, pt(*pivot), 7)
        pygame.draw.line(surface, DARK_GRAY, pt(*pivot), pt(*end), 8)
        pygame.draw.line(surface, BARRIER_ARM, pt(*pivot), pt(*end), 5)
        dx, dy = end[0] - pivot[0], end[1] - pivot[1]
        length = math.hypot(dx, dy)
        if length == 0:
            return
        ux, uy = dx / length, dy / length
        for d in range(12, int(length) - 6, 22):
            p1 = (pivot[0] + ux * d, pivot[1] + uy * d)
            p2 = (pivot[0] + ux * (d + 10), pivot[1] + uy * (d + 10))
            pygame.draw.line(surface, RED_C, pt(*p1), pt(*p2), 4)

    def draw(self, surface):
        """Draw all barrier arms."""
        for y in BARRIER_YS:
            self._draw_arm(surface, (BARRIER_LEFT_X, y), "left")
            self._draw_arm(surface, (BARRIER_RIGHT_X, y), "right")
