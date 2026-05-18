"""State machine for the train crossing lifecycle."""

from config.constants import (
    TRAIN_BARRIER_LOWER_OFFSET,
    TRAIN_BARRIER_RELEASE_SECONDS,
    TRAIN_LIGHTS_OFF_DELAY_SECONDS,
    TRAIN_REPEAT_SECONDS,
)


class TrainCrossingController:
    """Coordinate backend train state, warning lights, barriers, and spawning."""

    def __init__(self):
        """Create a controller in the idle crossing state."""
        self.backend_state = 0
        self.active_arrival_ts = None
        self.green_started_at = None
        self.barriers_opened_at = None
        self.train_spawned = False
        self.blinking_active = False
        self.road_blocked = False

    def sync_backend_state(self, sb_state, train_arrival_ts, now):
        """Synchronize crossing state from the backend ``sb`` value."""
        if sb_state is None:
            return

        if sb_state == 1 and train_arrival_ts:
            if self.active_arrival_ts != train_arrival_ts:
                self.active_arrival_ts = train_arrival_ts
                self.green_started_at = None
                self.barriers_opened_at = None
                self.train_spawned = False
            self.backend_state = sb_state
            self.blinking_active = True
            self.road_blocked = True
            return

        if sb_state == 0 and self.active_arrival_ts == train_arrival_ts:
            self.backend_state = sb_state
            if self.green_started_at is None:
                self.green_started_at = now
                self.barriers_opened_at = None
            self.blinking_active = True
            self.road_blocked = True
            return

        if sb_state == 2 and self.active_arrival_ts is None:
            self.backend_state = sb_state

    def should_spawn_train(self, now):
        """Return whether the train should spawn now."""
        if not self.active_arrival_ts or self.train_spawned:
            return False
        return now >= self.active_arrival_ts / 1000.0

    def mark_train_spawned(self):
        """Record that the current active train has spawned."""
        self.train_spawned = True

    def wants_barriers_lowered(self, now):
        """Return whether the railway barriers should be lowered."""
        if not self.active_arrival_ts:
            return False

        if self.green_started_at is not None:
            return now < self.green_started_at + TRAIN_BARRIER_RELEASE_SECONDS

        return now >= (self.active_arrival_ts / 1000.0) - TRAIN_BARRIER_LOWER_OFFSET

    def update(self, now, barriers_open):
        """Advance crossing state and return the next train time if scheduled."""
        next_train_time = None

        if self.green_started_at is not None:
            if barriers_open:
                if self.barriers_opened_at is None:
                    self.barriers_opened_at = now
                elif now - self.barriers_opened_at >= TRAIN_LIGHTS_OFF_DELAY_SECONDS:
                    next_train_time = now + TRAIN_REPEAT_SECONDS
                    self.backend_state = 0
                    self.active_arrival_ts = None
                    self.green_started_at = None
                    self.barriers_opened_at = None
                    self.train_spawned = False
                    self.blinking_active = False
                    self.road_blocked = False
            else:
                self.barriers_opened_at = None

        return next_train_time

