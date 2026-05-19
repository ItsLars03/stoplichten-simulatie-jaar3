"""State machine for the train crossing lifecycle."""

from config.constants import (
    TRAIN_BARRIER_LOWER_OFFSET,
    TRAIN_BARRIER_RELEASE_SECONDS,
    TRAIN_LIGHTS_OFF_DELAY_SECONDS,
    TRAIN_REPEAT_SECONDS,
)


class TrainCrossingController:
    """Frontend state machine for railway crossing."""

    WARNING_TO_BARRIER_SECONDS = 5
    GREEN_RELEASE_DELAY = 5

    def __init__(self):
        self.backend_state = 2

        self.active_arrival_ts = None

        self.warning_started_at = None
        self.green_started_at = None

        self.train_spawned = False

        self.blinking_active = False
        self.road_blocked = False

        self.barriers_should_close = False
        self.barriers_should_open = True

    # ------------------------------------------------------------
    # BACKEND SYNC
    # ------------------------------------------------------------
    def sync_backend_state(self, sb_state, train_arrival_ts, now):
        """Sync backend sb state (0/1/2)."""
        if sb_state is None:
            return

        self.backend_state = sb_state

        if self.active_arrival_ts != train_arrival_ts:
            self.active_arrival_ts = train_arrival_ts
            self.train_spawned = False  # Only reset train_spawned when a new arrival time is set
            self.warning_started_at = None
            self.green_started_at = None

        # -------------------------
        # WARNING (1)
        # -------------------------
        if sb_state == 1:
            self.blinking_active = True
            self.road_blocked = True

            if self.warning_started_at is None:
                self.warning_started_at = now

            if now - self.warning_started_at >= self.WARNING_TO_BARRIER_SECONDS:
                self.barriers_should_close = True

        # -------------------------
        # TRAIN ACTIVE (0)
        # -------------------------
        elif sb_state == 0:
            self.blinking_active = True
            self.road_blocked = True
            self.barriers_should_close = True

        # -------------------------
        # CLEAR / NORMAL (2)
        # -------------------------
        elif sb_state == 2:
            self.barriers_should_open = True

            if self.green_started_at is None:
                self.green_started_at = now

            if now - self.green_started_at >= self.GREEN_RELEASE_DELAY:
                self._reset()

    # ------------------------------------------------------------
    # TRAIN SPAWN LOGIC (RESTORED)
    # ------------------------------------------------------------
    def should_spawn_train(self, now):
        print("should spawn?", {
            "active_arrival_ts": self.active_arrival_ts,
            "train_spawned": self.train_spawned,
            "now": now,
            "arrival_time_sec": self.active_arrival_ts / 1000.0 if self.active_arrival_ts else None,
        })
        return (
                self.active_arrival_ts is not None
                and not self.train_spawned
                and now >= self.active_arrival_ts / 1000.0
        )

    def mark_train_spawned(self):
        self.train_spawned = True
        # self.active_arrival_ts = None  # Clear the arrival timestamp after spawning
        print("yes")


    # ------------------------------------------------------------
    # RESET
    # ------------------------------------------------------------
    def _reset(self):
        self.warning_started_at = None
        self.green_started_at = None

        self.blinking_active = False
        self.road_blocked = False

        self.barriers_should_close = False
        self.barriers_should_open = False


