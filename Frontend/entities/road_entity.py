"""Base class for moving road users."""

import math

import pygame

from config.constants import FOLLOW_MARGIN, LANE_ALIGN_TOL, STOP_DIST
from routing.routes import STOP_LIGHT_IDS


class RoadEntity:
    """Generic road user entity with logic that other entities use"""

    def __init__(self, coords, keys, color, speed, size):
        """Create an entity from resolved route coordinates and route keys."""
        self.route = coords
        self.keys = keys
        self.color = color
        self.speed = speed
        self.pos = list(coords[0])
        self.target = 1
        self.done = False
        self.waiting = False
        self.wait_reason = None
        self.waiting_train = False
        self.waiting_light_id = None
        self.w, self.h = size

    def angle(self):
        """Return the sprite rotation angle for the current movement direction."""
        if self.target >= len(self.route):
            return 0
        tx, ty = self.route[self.target]
        return math.degrees(math.atan2(-(ty - self.pos[1]), tx - self.pos[0])) - 90

    def movement_axis(self):
        """Return the dominant movement axis, direction step, and lane coordinate."""
        if self.target >= len(self.route):
            return None
        tx, ty = self.route[self.target]
        dx, dy = tx - self.pos[0], ty - self.pos[1]
        if abs(dx) >= abs(dy):
            return ("x", 1 if dx >= 0 else -1, self.pos[1])
        return ("y", 1 if dy >= 0 else -1, self.pos[0])

    def follow_gap(self, other):
        """Return the minimum allowed following gap to another entity."""
        return (max(self.w, self.h) + max(other.w, other.h)) / 2 + FOLLOW_MARGIN

    def can_be_blocked_by(self, other):
        """Return whether this entity treats ``other`` as a blocking entity."""
        return True

    def blocked_by_vehicle(self, vehicles):
        """Return whether another entity is too close ahead on the same lane."""
        info = self.movement_axis()
        if info is None:
            return False
        axis, step, lane = info
        nearest_gap = None
        for other in vehicles:
            if other is self or other.done:
                continue
            if not self.can_be_blocked_by(other):
                continue
            other_info = other.movement_axis()
            if other_info is None:
                continue
            other_axis, other_step, other_lane = other_info
            if axis != other_axis or step != other_step:
                continue
            if abs(lane - other_lane) > LANE_ALIGN_TOL:
                continue
            if axis == "x":
                gap = (other.pos[0] - self.pos[0]) * step
            else:
                gap = (other.pos[1] - self.pos[1]) * step
            if gap <= 0:
                continue
            min_gap = self.follow_gap(other)
            if gap < min_gap and (nearest_gap is None or gap < nearest_gap):
                nearest_gap = gap
        return nearest_gap is not None

    def signal_stop_distance(self):
        """Return how close this entity gets before waiting at a red signal."""
        return STOP_DIST

    def snap_to_signal_stop(self):
        """Return whether the entity should snap exactly onto signal stops."""
        return False

    def update(self, dt, tl_map, vehicles, train_blocked=False):
        """Advance movement and update waiting state for signals and trains."""
        if self.done or self.waiting:
            return
        tx, ty = self.route[self.target]
        dx, dy = tx - self.pos[0], ty - self.pos[1]
        dist = math.hypot(dx, dy)
        cur = self.keys[self.target] if self.target < len(self.keys) else None
        if self.blocked_by_vehicle(vehicles):
            self.waiting = True
            self.wait_reason = "vehicle"
            self.waiting_train = False
            return
        if isinstance(cur, str) and "_stop" in cur and "_train" not in cur and dist < self.signal_stop_distance():
            light_id = STOP_LIGHT_IDS.get(cur)
            tl = tl_map.get(light_id)
            if tl and tl.state in ("Red", "Orange"):
                if self.snap_to_signal_stop():
                    self.pos[0], self.pos[1] = tx, ty
                self.waiting = True
                self.wait_reason = "signal"
                self.waiting_train = False
                self.waiting_light_id = light_id
                return
        if isinstance(cur, str) and "_trainStop" in cur and dist < STOP_DIST:
            if train_blocked:
                self.waiting = True
                self.waiting_train = True
                self.wait_reason = "train"
                self.waiting_light_id = None
                return
        if dist < 3:
            self.target += 1
            self.waiting_light_id = None
            if self.target >= len(self.route):
                self.done = True
        else:
            s = self.speed * dt
            self.pos[0] += (dx / dist) * s
            self.pos[1] += (dy / dist) * s

    def resume_if_green(self, tl_map, train_blocked=False):
        """Clear a waiting state when a signal or train crossing allows movement."""
        if not self.waiting:
            return
        if self.wait_reason == "vehicle":
            self.waiting = False
            self.wait_reason = None
            self.waiting_train = False
            self.waiting_light_id = None
            return
        if self.wait_reason == "train":
            if not train_blocked:
                self.waiting = False
                self.waiting_train = False
                self.wait_reason = None
                self.waiting_light_id = None
            return
        tl = tl_map.get(self.waiting_light_id)
        if tl and tl.state == "Green":
            self.waiting = False
            self.wait_reason = None
            self.waiting_light_id = None

    def draw(self, surface):
        """Draw the entity as a rotated rectangle."""
        surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        pygame.draw.rect(surf, self.color, (0, 0, self.w, self.h), border_radius=3)
        rot = pygame.transform.rotate(surf, self.angle())
        rect = rot.get_rect(center=(int(self.pos[0]), int(self.pos[1])))
        surface.blit(rot, rect)

