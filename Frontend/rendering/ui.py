"""Bottom panel UI rendering."""

import time

import pygame

from config.constants import GRAY, GREEN_C, HEIGHT, ORANGE_C, RED_C, WHITE, WIDTH
from entities.bus import Bus
from entities.car import Car
from entities.cyclist import Cyclist
from entities.pedestrian import Pedestrian


def draw_ui(surface, font, vehicles, tls, last_api, train_arrival_ts):
    """Draw the ui stats like:
    active vehicles,
    waiting vehicles,
    counts by type,
    last API call time,
    train arrival time.
    and the traffic light color states."""

    panel_height = 110
    panel_y = HEIGHT - panel_height
    row1_y = panel_y + 8

    pygame.draw.rect(surface, (16, 16, 20), (0, panel_y, WIDTH, panel_height))
    pygame.draw.line(surface, GRAY, (0, panel_y), (WIDTH, panel_y), 1)

    active = [v for v in vehicles if not v.done]
    waiting = [v for v in active if v.waiting]
    cars = sum(isinstance(v, Car) and not isinstance(v, (Bus, Cyclist, Pedestrian)) for v in active)
    buses = sum(isinstance(v, Bus) for v in active)
    bikes = sum(isinstance(v, Cyclist) for v in active)
    pedestrians = sum(isinstance(v, Pedestrian) for v in active)

    time_until = max(0, int(train_arrival_ts / 1000 - time.time())) if train_arrival_ts else None
    stats = [
        f"Active: {len(active)}",
        f"Waiting: {len(waiting)}",
        f"Cars/Buses/Bikes/Peds: {cars}/{buses}/{bikes}/{pedestrians}",
        f"API: {time.strftime('%H:%M:%S', time.localtime(last_api))}",
        f"Train in: {time_until}s" if time_until is not None else "No train",
    ]

    slot_w = WIDTH // len(stats)
    for i, text in enumerate(stats):
        label = font.render(text, True, WHITE)
        x = i * slot_w + (slot_w - label.get_width()) // 2
        surface.blit(label, (x, row1_y))

    x, y = 16, HEIGHT - panel_height + 42
    for tl in tls:
        color = RED_C if tl.state == "Red" else (ORANGE_C if tl.state == "Orange" else GREEN_C)
        label_w = max(48, font.size(tl.id)[0] + 20)
        if x + label_w > WIDTH - 20:
            x = 16
            y += 20
        pygame.draw.circle(surface, color, (x + 5, y), 5)
        surface.blit(font.render(tl.id, True, WHITE), (x + 13, y - 6))
        x += label_w
