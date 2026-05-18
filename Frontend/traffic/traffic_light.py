"""Traffic light rendering and state."""

import pygame

from config.constants import DARK_GRAY, GRAY, GREEN_C, ORANGE_C, RED_C, SENSOR_ON, WHITE


class TrafficLight:
    """A trafficlight with one or more stop waypoints."""

    def __init__(self, definition):
        """Create a traffic light from a dictionary definition."""
        self.id = definition["id"]
        self.stop_wps = definition["stops"] if "stops" in definition else [definition["stop"]]
        self.pos = definition["pos"]
        self.kind = definition.get("kind", "vehicle")
        self.label_offset = definition.get("label_offset", (0, 30))
        self.light_offset = definition.get("light_offset", (0, 0))
        self.state = "Red"
        self.has_entity = False
        self.triggered_ts = None

    def draw(self, surface, font):
        """Draw the traffic light, its sensor, and its id label."""
        x, y = self.pos
        color_map = {
            "Red": (RED_C, GRAY, GRAY),
            "Orange": (GRAY, ORANGE_C, GRAY),
            "Green": (GRAY, GRAY, GREEN_C),
        }
        rc, oc, gc = color_map.get(self.state, (GRAY, GRAY, GRAY))
        if self.kind in ("bike", "pedestrian"):
            body_w = 10
            body_h = 28
            light_r = 3
            spacing = 8

            lx, ly = self.light_offset
            hx, hy = x + lx, y + ly

            pygame.draw.rect(
                surface,
                DARK_GRAY,
                (hx - body_w // 2, hy - body_h // 2, body_w, body_h),
                border_radius=3,
            )
            pygame.draw.circle(surface, rc, (hx, hy - spacing), light_r)
            pygame.draw.circle(surface, oc, (hx, hy), light_r)
            pygame.draw.circle(surface, gc, (hx, hy + spacing), light_r)
            pygame.draw.circle(surface, SENSOR_ON if self.has_entity else WHITE, (x, y), 3)

            ox, oy = self.label_offset
            label = font.render(self.id, True, WHITE)
            surface.blit(label, (hx - label.get_width() // 2 + ox, hy + oy))
            return

        pygame.draw.rect(surface, DARK_GRAY, (x - 7, y - 26, 14, 48), border_radius=4)
        pygame.draw.circle(surface, rc, (x, y - 14), 5)
        pygame.draw.circle(surface, oc, (x, y), 5)
        pygame.draw.circle(surface, gc, (x, y + 14), 5)

        _offset_x, offset_y = self.label_offset
        label = font.render(self.id, True, WHITE)
        surface.blit(label, (x - label.get_width() // 2, y + offset_y))
        pygame.draw.circle(surface, SENSOR_ON if self.has_entity else GRAY, (x, y + 25), 3)

