"""Road, lane, track, and label rendering."""

import pygame

from config.constants import (
    BG,
    BICYCLE_EDGE,
    BICYCLE_LANE,
    BIKE_LANE_W,
    BOX_COL,
    DASH,
    HEIGHT,
    LANE_SPLIT_GAP,
    PEDESTRIAN_EDGE,
    PEDESTRIAN_LANE,
    PEDESTRIAN_LANE_W,
    RAIL_COL,
    ROAD,
    S_LANES,
    STOP_LINE,
    TIE_COL,
    RAIL_GAP,
    WHITE,
    WIDTH,
    W_LANES,
)
from config.geometry import (
    BIKE_EAST_X_IN,
    BIKE_EAST_Y_IN,
    BIKE_LANE_PATHS,
    BIKE_SOUTH_E_X_IN,
    BIKE_SOUTH_W_X_IN,
    BIKE_WEST_X_IN,
    BIKE_WEST_Y_IN,
    BOX_B,
    BOX_H,
    BOX_L,
    BOX_R,
    BOX_T,
    BOX_W,
    E_ARM_H,
    EAST_STOP_X,
    E_GRASS_GAP_Y,
    E_LANES,
    E_SEPARATORS,
    E_STOP_B,
    E_STOP_T,
    N_ARM_W,
    NORTH_STOP_Y,
    N_GRASS_GAP_X,
    N_LANES,
    N_SEPARATORS,
    PEDESTRIAN_LANE_PATHS,
    PED_EAST_Y,
    PED_NORTH_E_X,
    PED_SOUTH_E_X,
    PED_SOUTH_W_X,
    PED_WEST_X,
    PED_WEST_Y,
    N_STOP_L,
    N_STOP_R,
    S_ARM_L,
    S_ARM_R,
    S_ARM_W,
    SOUTH_STOP_Y,
    S_GRASS_GAP_X,
    S_SEPARATORS,
    S_STOP_L,
    S_STOP_R,
    STOP_GAP,
    TRAIN_TRACK_YS,
    W_ARM_H,
    W_ARM_T,
    WEST_STOP_X,
    W_GRASS_GAP_Y,
    W_SEPARATORS,
    W_STOP_B,
    W_STOP_T,
    get_east_lane_y,
    get_north_lane_x,
    get_south_lane_x,
    get_west_lane_y,
)

def draw_horizontal_dashes(surface, x0, x1, y):
    """Draw dashed lane separators on a horizontal road segment."""
    for x in range(x0, x1 - 4, 22):
        pygame.draw.rect(surface, DASH, (x, y - 1, 12, 2))


def draw_vertical_dashes(surface, x, y0, y1):
    """Draw dashed lane separators on a vertical road segment."""
    for y in range(y0, y1 - 4, 22):
        pygame.draw.rect(surface, DASH, (x - 1, y, 2, 12))


def draw_lane_labels(surface):
    """Draw car, bicycle, and pedestrian lane labels."""
    label_font = pygame.font.SysFont("monospace", 9)
    lane_label_color = (150, 150, 150)
    for n in range(1, N_LANES + 1):
        surface.blit(label_font.render(f"N{n}", True, lane_label_color), (get_north_lane_x(n) - 8, 6))
    for n in range(1, S_LANES + 1):
        surface.blit(label_font.render(f"S{n}", True, lane_label_color), (get_south_lane_x(n) - 8, HEIGHT - 125))
    for n in range(1, E_LANES + 1):
        surface.blit(label_font.render(f"E{n}", True, lane_label_color), (WIDTH - 22, get_east_lane_y(n) - 5))
    for n in range(1, W_LANES + 1):
        surface.blit(label_font.render(f"W{n}", True, lane_label_color), (4, get_west_lane_y(n) - 5))

    bike_labels = {
        "N0": (BIKE_WEST_X_IN - 18, 6),
        "N6": (BIKE_EAST_X_IN - 14, 6),
        "E0": (WIDTH - 26, BIKE_EAST_Y_IN - 4),
        "S0": (BIKE_SOUTH_W_X_IN - 10, HEIGHT - 16),
        "S4": (BIKE_SOUTH_E_X_IN - 10, HEIGHT - 16),
        "W5": (4, BIKE_WEST_Y_IN - 5),
    }
    for label, pos in bike_labels.items():
        surface.blit(label_font.render(label, True, WHITE), pos)

    pedestrian_labels = {
        "NZ": (PED_WEST_X - 18, 6),
        "N7": (PED_NORTH_E_X + 6, 6),
        "EZ": (WIDTH - 26, PED_EAST_Y - 4),
        "SZ": (PED_SOUTH_W_X - 14, HEIGHT - 16),
        "S5": (PED_SOUTH_E_X - 8, HEIGHT - 16),
        "W6": (4, PED_WEST_Y - 5),
    }
    for label, pos in pedestrian_labels.items():
        surface.blit(label_font.render(label, True, PEDESTRIAN_EDGE), pos)


def draw_road(surface, font):
    """Draw the static simulation background and road infrastructure."""
    surface.fill(BG)
    pygame.draw.rect(surface, ROAD, (BOX_L, 0, N_ARM_W, BOX_T))
    pygame.draw.rect(surface, ROAD, (S_ARM_L, BOX_B, S_ARM_W, HEIGHT - BOX_B))
    pygame.draw.rect(surface, ROAD, (BOX_R, BOX_T, WIDTH - BOX_R, E_ARM_H))
    pygame.draw.rect(surface, ROAD, (0, W_ARM_T, BOX_L, W_ARM_H))
    pygame.draw.rect(surface, BOX_COL, (BOX_L, BOX_T, BOX_W, BOX_H))

    for path in BIKE_LANE_PATHS:
        pygame.draw.lines(surface, BICYCLE_LANE, False, path, BIKE_LANE_W)
        pygame.draw.lines(surface, BICYCLE_EDGE, False, path, 1)
    for path in PEDESTRIAN_LANE_PATHS:
        pygame.draw.lines(surface, PEDESTRIAN_LANE, False, path, PEDESTRIAN_LANE_W)
        pygame.draw.lines(surface, PEDESTRIAN_EDGE, False, path, 1)

    for x in N_SEPARATORS:
        draw_vertical_dashes(surface, x, 0, BOX_T - 4)
    for x in S_SEPARATORS:
        draw_vertical_dashes(surface, x, BOX_B + 4, HEIGHT)
    for y in E_SEPARATORS:
        draw_horizontal_dashes(surface, BOX_R + 4, WIDTH, y)
    for y in W_SEPARATORS:
        draw_horizontal_dashes(surface, 0, BOX_L - 4, y)

    pygame.draw.rect(surface, BG, (N_GRASS_GAP_X, 0, LANE_SPLIT_GAP, BOX_T))
    pygame.draw.rect(surface, BG, (S_GRASS_GAP_X, BOX_B, LANE_SPLIT_GAP, HEIGHT - BOX_B))
    pygame.draw.rect(surface, BG, (BOX_R, E_GRASS_GAP_Y, WIDTH - BOX_R, LANE_SPLIT_GAP))
    pygame.draw.rect(surface, BG, (0, W_GRASS_GAP_Y, BOX_L, LANE_SPLIT_GAP))

    pygame.draw.rect(surface, STOP_LINE, (N_STOP_L, NORTH_STOP_Y + 2, N_STOP_R - N_STOP_L, 3))
    pygame.draw.rect(surface, STOP_LINE, (S_STOP_L, SOUTH_STOP_Y, S_STOP_R - S_STOP_L, 3))
    pygame.draw.rect(surface, STOP_LINE, (EAST_STOP_X - STOP_GAP, E_STOP_T, 3, E_STOP_B - E_STOP_T))
    pygame.draw.rect(surface, STOP_LINE, (WEST_STOP_X + 2, W_STOP_T, 3, W_STOP_B - W_STOP_T))

    for track_y in TRAIN_TRACK_YS:
        for tx in range(S_ARM_L - 6, S_ARM_R + 7, 10):
            pygame.draw.rect(surface, TIE_COL, (tx, track_y - RAIL_GAP - 4, 7, (RAIL_GAP + 4) * 2))
        pygame.draw.rect(surface, RAIL_COL, (0, track_y - RAIL_GAP - 2, WIDTH, 3))
        pygame.draw.rect(surface, RAIL_COL, (0, track_y + RAIL_GAP - 1, WIDTH, 3))

    draw_lane_labels(surface)

