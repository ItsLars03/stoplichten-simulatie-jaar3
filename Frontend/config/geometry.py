"""Geometry calculations and waypoint definitions."""

from config.constants import (
    WIDTH, HEIGHT, CX, CY, LANE_W, LANE_SPLIT_GAP,
    N_LANES, E_LANES, S_LANES, W_LANES, APPROACH_BACKSET,
    TRAIN_BOX_CLEARANCE, RAIL_GAP, TRAIN_STOP_MARGIN,
)

# --- Lane Centers ---
def build_lane_centers(count, gap_after_lanes=()):
    """Build local lane center positions, including optional split gaps."""
    centers = []
    cursor = LANE_W // 2
    split_after = set(gap_after_lanes)
    for lane in range(1, count + 1):
        centers.append(cursor)
        if lane < count:
            cursor += LANE_W
            if lane in split_after:
                cursor += LANE_SPLIT_GAP
    return centers

def lane_span(local_centers):
    """Return the full rendered span for a list of local lane centers."""
    return local_centers[-1] + LANE_W // 2

N_LOCAL_CENTERS = build_lane_centers(N_LANES, (4,))
E_LOCAL_CENTERS = build_lane_centers(E_LANES, (3,))
S_LOCAL_CENTERS = build_lane_centers(S_LANES, (1,))
W_LOCAL_CENTERS = build_lane_centers(W_LANES, (1,))

N_ARM_W = lane_span(N_LOCAL_CENTERS)
S_ARM_W = lane_span(S_LOCAL_CENTERS)
E_ARM_H = lane_span(E_LOCAL_CENTERS)
W_ARM_H = lane_span(W_LOCAL_CENTERS)

BOX_W = max(N_ARM_W, S_ARM_W)
BOX_H = max(E_ARM_H, W_ARM_H)
BOX_L = CX - BOX_W // 2
BOX_R = CX + BOX_W // 2
BOX_T = CY - BOX_H // 2
BOX_B = CY + BOX_H // 2

S_ARM_L = BOX_R - S_ARM_W
S_ARM_R = BOX_R
W_ARM_T = BOX_B - W_ARM_H
W_ARM_B = BOX_B

# --- Lane Coordinate Helpers ---
def get_north_lane_x(n):
    """Return the x coordinate for north-side lane `n`."""
    return BOX_L + N_LOCAL_CENTERS[n - 1]

def get_south_lane_x(n):
    """Return the x coordinate for south-side lane `n`."""
    return S_ARM_L + S_LOCAL_CENTERS[n - 1]

def get_east_lane_y(n):
    """Return the y coordinate for east-side lane `n`."""
    return BOX_T + E_LOCAL_CENTERS[n - 1]

def get_west_lane_y(n):
    """Return the y coordinate for west-side lane `n`."""
    return W_ARM_T + W_LOCAL_CENTERS[n - 1]

# --- Separators ---
STOP_GAP = 5
N_SEPARATORS = [int((get_north_lane_x(n) + get_north_lane_x(n + 1)) / 2) for n in range(1, N_LANES)]
S_SEPARATORS = [int((get_south_lane_x(n) + get_south_lane_x(n + 1)) / 2) for n in range(1, S_LANES)]
E_SEPARATORS = [int((get_east_lane_y(n) + get_east_lane_y(n + 1)) / 2) for n in range(1, E_LANES)]
W_SEPARATORS = [int((get_west_lane_y(n) + get_west_lane_y(n + 1)) / 2) for n in range(1, W_LANES)]

# --- Stop Lines ---
N_STOP_L = get_north_lane_x(1) - LANE_W // 2
N_STOP_R = get_north_lane_x(4) + LANE_W // 2
S_STOP_L = get_south_lane_x(2) - LANE_W // 2
S_STOP_R = get_south_lane_x(3) + LANE_W // 2
E_STOP_T = get_east_lane_y(1) - LANE_W // 2
E_STOP_B = get_east_lane_y(3) + LANE_W // 2
W_STOP_T = get_west_lane_y(2) - LANE_W // 2
W_STOP_B = get_west_lane_y(4) + LANE_W // 2

# --- Grass Gaps ---
N_GRASS_GAP_X = get_north_lane_x(4) + LANE_W // 2
S_GRASS_GAP_X = get_south_lane_x(1) + LANE_W // 2
E_GRASS_GAP_Y = get_east_lane_y(3) + LANE_W // 2
W_GRASS_GAP_Y = get_west_lane_y(1) + LANE_W // 2

# --- Stop Y/X Coordinates ---
NORTH_STOP_Y = BOX_T - APPROACH_BACKSET
EAST_STOP_X = BOX_R + APPROACH_BACKSET
WEST_STOP_X = BOX_L - APPROACH_BACKSET

# --- Train Geometry ---
TRAIN_Y = BOX_B + TRAIN_BOX_CLEARANCE
TRAIN_Y_LOWER = TRAIN_Y + 40
TRAIN_TRACK_YS = (TRAIN_Y, TRAIN_Y_LOWER)
TRAIN_STOP_Y_N = TRAIN_Y - RAIL_GAP - TRAIN_STOP_MARGIN
TRAIN_STOP_Y_S = TRAIN_Y_LOWER + RAIL_GAP + TRAIN_STOP_MARGIN
SOUTH_STOP_Y = TRAIN_STOP_Y_S + STOP_GAP

# --- Barrier Geometry ---
_SB_XS = [S_ARM_L - 18, S_ARM_R + 18]
_SB_YS_TOP = TRAIN_Y - RAIL_GAP - 22
_SB_YS_BOTTOM = TRAIN_Y_LOWER + RAIL_GAP + 22

def pt(x, y):
    """Convert coordinates into pixel positions, for pygame."""
    return (int(x), int(y))

BARRIER_LEFT_X = S_ARM_L - 65
BARRIER_RIGHT_X = S_ARM_R + 70
BARRIER_ARM_LEN = (BARRIER_RIGHT_X - BARRIER_LEFT_X) / 2 - 6
BARRIER_YS = (
    TRAIN_Y - RAIL_GAP - 15,
    TRAIN_Y_LOWER + RAIL_GAP + 15,
)

# --- Bicycle Geometry ---
BIKE_WEST_X_IN = BOX_L - 14
BIKE_WEST_X_OUT = BOX_L - 4
BIKE_EAST_X_IN = BOX_R + 8
BIKE_EAST_X_OUT = BOX_R + 16
BIKE_NORTH_Y_OUT = BOX_T - 30
BIKE_NORTH_Y_IN = BOX_T - 19
BIKE_WEST_Y_IN = BOX_B + 16
BIKE_WEST_Y_OUT = BOX_B + 8
BIKE_EAST_Y_IN = BOX_T - 11
BIKE_EAST_Y_OUT = BOX_T - 3
BIKE_SOUTH_W_X_IN = S_ARM_L - 30
BIKE_SOUTH_W_X_OUT = S_ARM_L - 38
BIKE_SOUTH_E_X_IN = S_ARM_R + 40
BIKE_SOUTH_E_X_OUT = S_ARM_R + 32
BIKE_MID_Y = BOX_B + 60
BIKE_TRAIN_STOP_TOP = TRAIN_Y - RAIL_GAP - 22
BIKE_TRAIN_STOP_BOTTOM = TRAIN_Y_LOWER + RAIL_GAP + 22

BIKE_LANE_PATHS = [
    [pt(BIKE_WEST_X_OUT - 1, -30), pt(BIKE_WEST_X_OUT - 1, BIKE_WEST_Y_IN)],
    [pt(-30, BOX_B + 12), pt(BIKE_WEST_X_OUT - 1, BOX_B + 12)],
    [pt(BIKE_WEST_X_OUT - 1, BOX_T - 25), pt(BIKE_EAST_X_IN + 4, BOX_T - 25)],
    [pt(BIKE_EAST_X_IN + 4, -30), pt(BIKE_EAST_X_IN + 4, BOX_B + 12)],
    [pt(BIKE_EAST_X_IN + 4, BOX_T - 7), pt(WIDTH + 30, BOX_T - 7)],
    [pt(BIKE_WEST_X_OUT - 1, BOX_B + 12), pt(BIKE_SOUTH_W_X_IN - 3, BIKE_MID_Y), pt(BIKE_SOUTH_W_X_IN - 3, HEIGHT + 30)],
    [pt(BIKE_EAST_X_IN + 4, BOX_B + 12), pt(BIKE_SOUTH_E_X_OUT + 3, BIKE_MID_Y), pt(BIKE_SOUTH_E_X_OUT + 3, HEIGHT + 30)],
]

# --- Pedestrian Geometry ---
PED_WEST_X = BIKE_WEST_X_IN - 12
PED_NORTH_E_X = BIKE_EAST_X_OUT
PED_EAST_X = BIKE_EAST_X_OUT + 20
PED_SOUTH_W_X = BIKE_SOUTH_W_X_OUT - 8
PED_SOUTH_E_X = BIKE_SOUTH_E_X_OUT + 25
PED_NORTH_Y = BOX_T - 36
PED_WEST_Y = BOX_B + 22
PED_EAST_Y = PED_NORTH_Y
PED_SOUTH_JOIN_Y = TRAIN_Y - RAIL_GAP - 6
PED_TRAIN_STOP_TOP = TRAIN_Y - RAIL_GAP - 28
PED_TRAIN_STOP_BOTTOM = TRAIN_Y_LOWER + RAIL_GAP + 58
PED_NORTH_SPLIT_X = N_GRASS_GAP_X + LANE_SPLIT_GAP // 2
PED_WEST_SPLIT_Y = (get_west_lane_y(1) + get_west_lane_y(2)) // 2
PED_EAST_SPLIT_Y = (get_east_lane_y(3) + get_east_lane_y(4)) // 2

PEDESTRIAN_LANE_PATHS = [
    [pt(PED_WEST_X, -30), pt(PED_WEST_X, PED_WEST_Y)],
    [pt(-30, PED_WEST_Y), pt(PED_WEST_X, PED_WEST_Y)],
    [pt(PED_WEST_X, PED_NORTH_Y), pt(PED_EAST_X, PED_NORTH_Y)],
    [pt(PED_NORTH_E_X, -30), pt(PED_NORTH_E_X, PED_NORTH_Y)],
    [pt(PED_EAST_X, PED_EAST_Y), pt(WIDTH + 30, PED_EAST_Y)],
    [pt(PED_EAST_X, PED_EAST_Y), pt(PED_EAST_X, PED_WEST_Y)],
    [pt(PED_WEST_X, PED_WEST_Y), pt(PED_SOUTH_W_X, PED_SOUTH_JOIN_Y), pt(PED_SOUTH_W_X, HEIGHT + 30)],
    [pt(PED_EAST_X, PED_WEST_Y), pt(PED_SOUTH_E_X, PED_SOUTH_JOIN_Y), pt(PED_SOUTH_E_X, HEIGHT + 30)],
]

# --- Waypoints ---
# waypoints refer to a specific point in the simulation
# and are given a name to easily use them in multiple places
WAYPOINT = {}
for n in range(1, N_LANES + 1):
    x = get_north_lane_x(n)
    WAYPOINT[f"N{n}_entry"] = pt(x, -30)
    WAYPOINT[f"N{n}_stop"] = pt(x, NORTH_STOP_Y)
    WAYPOINT[f"N{n}_box"] = pt(x, BOX_T + LANE_W // 2)
    WAYPOINT[f"N{n}_exit"] = pt(x, -30)

for n in range(1, S_LANES + 1):
    x = get_south_lane_x(n)
    WAYPOINT[f"S{n}_entry"] = pt(x, HEIGHT + 30)
    WAYPOINT[f"S{n}_stop"] = pt(x, SOUTH_STOP_Y)
    WAYPOINT[f"S{n}_box"] = pt(x, BOX_B - LANE_W // 2)
    WAYPOINT[f"S{n}_exit"] = pt(x, HEIGHT + 30)
    WAYPOINT[f"S{n}_trainStop"] = pt(x, TRAIN_STOP_Y_S)

WAYPOINT["S1_trainStop"] = pt(get_south_lane_x(1), TRAIN_STOP_Y_N)

for n in range(1, E_LANES + 1):
    y = get_east_lane_y(n)
    WAYPOINT[f"E{n}_entry"] = pt(WIDTH + 30, y)
    WAYPOINT[f"E{n}_stop"] = pt(EAST_STOP_X, y)
    WAYPOINT[f"E{n}_box"] = pt(BOX_R - LANE_W // 2, y)
    WAYPOINT[f"E{n}_exit"] = pt(WIDTH + 30, y)

for n in range(1, W_LANES + 1):
    y = get_west_lane_y(n)
    WAYPOINT[f"W{n}_entry"] = pt(-30, y)
    WAYPOINT[f"W{n}_stop"] = pt(WEST_STOP_X, y)
    WAYPOINT[f"W{n}_box"] = pt(BOX_L + LANE_W // 2, y)
    WAYPOINT[f"W{n}_exit"] = pt(-30, y)

WAYPOINT.update({
    "N0_entry": pt(BIKE_WEST_X_IN, -30),
    "N0_exit": pt(BIKE_WEST_X_OUT, -30),
    "N6_entry": pt(BIKE_EAST_X_IN, -30),
    "N6_exit": pt(BIKE_EAST_X_OUT, -30),
    "E0_entry": pt(WIDTH + 30, BIKE_EAST_Y_IN),
    "E0_exit": pt(WIDTH + 30, BIKE_EAST_Y_OUT),
    "S0_entry": pt(BIKE_SOUTH_W_X_IN, HEIGHT + 30),
    "S0_exit": pt(BIKE_SOUTH_W_X_OUT, HEIGHT + 30),
    "S4_entry": pt(BIKE_SOUTH_E_X_IN, HEIGHT + 30),
    "S4_exit": pt(BIKE_SOUTH_E_X_OUT, HEIGHT + 30),
    "W5_entry": pt(-30, BIKE_WEST_Y_IN),
    "W5_exit": pt(-30, BIKE_WEST_Y_OUT),
    "B26_1_stop": pt(BIKE_WEST_X_IN, BOX_T + 22),
    "B86_1_stop": pt(BIKE_WEST_X_OUT, BOX_B + 2),
    "B88_1_stop": pt(BIKE_WEST_X_OUT, BIKE_NORTH_Y_IN),
    "B28_1_stop": pt(BIKE_EAST_X_IN, BIKE_NORTH_Y_OUT),
    "B22_in_stop": pt(BIKE_EAST_X_IN, BOX_T + 22),
    "B22_out_stop": pt(BIKE_EAST_X_OUT, BOX_B + 2),
    "S0_in_trainStop": pt(BIKE_SOUTH_W_X_IN, BIKE_TRAIN_STOP_BOTTOM),
    "S0_out_trainStop": pt(BIKE_SOUTH_W_X_OUT, BIKE_TRAIN_STOP_TOP),
    "S4_in_trainStop": pt(BIKE_SOUTH_E_X_IN, BIKE_TRAIN_STOP_BOTTOM),
    "S4_out_trainStop": pt(BIKE_SOUTH_E_X_OUT, BIKE_TRAIN_STOP_TOP),
})

WAYPOINT.update({
    "NZ_entry": pt(PED_WEST_X, -30),
    "NZ_exit": pt(PED_WEST_X, -30),
    "N7_entry": pt(PED_NORTH_E_X, -30),
    "N7_exit": pt(PED_NORTH_E_X, -30),
    "EZ_entry": pt(WIDTH + 30, PED_EAST_Y),
    "EZ_exit": pt(WIDTH + 30, PED_EAST_Y),
    "SZ_entry": pt(PED_SOUTH_W_X, HEIGHT + 30),
    "SZ_exit": pt(PED_SOUTH_W_X, HEIGHT + 30),
    "S5_entry": pt(PED_SOUTH_E_X, HEIGHT + 30),
    "S5_exit": pt(PED_SOUTH_E_X, HEIGHT + 30),
    "W6_entry": pt(-30, PED_WEST_Y),
    "W6_exit": pt(-30, PED_WEST_Y),
    "P36_2_stop": pt(PED_WEST_X, BOX_T + 16),
    "P36_1_stop": pt(PED_WEST_X, PED_WEST_SPLIT_Y),
    "P35_1_stop": pt(PED_WEST_X, PED_WEST_SPLIT_Y),
    "P35_2_stop": pt(PED_WEST_X, BOX_B + 2),
    "P37_2_stop": pt(BOX_L, PED_NORTH_Y),
    "P37_1_stop": pt(PED_NORTH_SPLIT_X, PED_NORTH_Y),
    "P38_1_stop": pt(PED_NORTH_SPLIT_X, PED_NORTH_Y),
    "P38_2_stop": pt(BIKE_EAST_X_IN, PED_NORTH_Y),
    "P31_2_stop": pt(PED_EAST_X, BOX_T - 5),
    "P31_1_stop": pt(PED_EAST_X, PED_EAST_SPLIT_Y),
    "P32_1_stop": pt(PED_EAST_X, PED_EAST_SPLIT_Y),
    "P32_2_stop": pt(PED_EAST_X, BOX_B + 2),
    "SZ_in_trainStop": pt(PED_SOUTH_W_X, PED_TRAIN_STOP_BOTTOM),
    "SZ_out_trainStop": pt(PED_SOUTH_W_X, PED_TRAIN_STOP_TOP),
    "S5_in_trainStop": pt(PED_SOUTH_E_X, PED_TRAIN_STOP_BOTTOM),
    "S5_out_trainStop": pt(PED_SOUTH_E_X, PED_TRAIN_STOP_TOP),
})