"""Traffic light definitions and related mappings."""

from config.constants import SMALL_LABEL_OFFSET

from config.geometry import (
    pt, get_north_lane_x, get_south_lane_x, get_east_lane_y, get_west_lane_y,
    NORTH_STOP_Y, SOUTH_STOP_Y, EAST_STOP_X, WEST_STOP_X,
    WAYPOINT, S_ARM_L, S_ARM_R, TRAIN_Y, RAIL_GAP, TRAIN_Y_LOWER
)

# --- Main Traffic Light Definitions ---
TRAFFIC_LIGHT_DEFS = [
    # North outgoing
    {"id": "10.1", "stops": ["N1_stop"], "pos": pt(get_north_lane_x(1) + 0, NORTH_STOP_Y - 43)},
    {"id": "11.1", "stops": ["N2_stop"], "pos": pt(get_north_lane_x(2) + 0, NORTH_STOP_Y - 43)},
    {"id": "12.1", "stops": ["N3_stop", "N4_stop"], "pos": pt(get_north_lane_x(3) + 10, NORTH_STOP_Y - 43)},
    # East outgoing
    {"id": "42", "stops": ["E1_stop"], "pos": pt(EAST_STOP_X + 10, get_east_lane_y(1) - 32)},
    {"id": "1.1", "stops": ["E2_stop"], "pos": pt(EAST_STOP_X + 30, get_east_lane_y(2) - 32)},
    {"id": "2.1", "stops": ["E3_stop"], "pos": pt(EAST_STOP_X + 50, get_east_lane_y(3) - 32)},
    # South outgoing
    {"id": "6.1", "stops": ["S2_stop"], "pos": pt(get_south_lane_x(2) - 2, SOUTH_STOP_Y)},
    {"id": "5.1", "stops": ["S3_stop"], "pos": pt(get_south_lane_x(3) + 2, SOUTH_STOP_Y)},
    # West outgoing
    {"id": "9.1", "stops": ["W2_stop"], "pos": pt(WEST_STOP_X - 47, get_west_lane_y(2) - 36)},
    {"id": "8.1", "stops": ["W3_stop"], "pos": pt(WEST_STOP_X - 30, get_west_lane_y(3) - 35)},
    {"id": "7.1", "stops": ["W4_stop"], "pos": pt(WEST_STOP_X - 13, get_west_lane_y(4) - 32)},

    # Bicycle crossings
    {"id": "26.1", "stops": ["B26_1_stop"], "pos": WAYPOINT["B26_1_stop"], "kind": "bike", "light_offset": (-1500, -1500), "label_offset": SMALL_LABEL_OFFSET},
    {"id": "88.1", "stops": ["B88_1_stop"], "pos": WAYPOINT["B88_1_stop"], "kind": "bike", "light_offset": (10, 10), "label_offset": SMALL_LABEL_OFFSET},
    {"id": "28.1", "stops": ["B28_1_stop"], "pos": WAYPOINT["B28_1_stop"], "kind": "bike", "light_offset": (28, -35), "label_offset": SMALL_LABEL_OFFSET},
    {"id": "22", "stops": ["B22_in_stop", "B22_out_stop"], "pos": WAYPOINT["B22_out_stop"], "kind": "bike", "light_offset": (-20, 0), "label_offset": SMALL_LABEL_OFFSET},
    {"id": "86.1", "stops": ["B86_1_stop"], "pos": WAYPOINT["B86_1_stop"], "kind": "bike", "light_offset": (20, -25), "label_offset": SMALL_LABEL_OFFSET},

    # Pedestrian crossings
    {"id": "36.2", "stops": ["P36_2_stop"], "pos": WAYPOINT["P36_2_stop"], "kind": "pedestrian", "light_offset": (-20, -25), "label_offset": SMALL_LABEL_OFFSET},
    {"id": "36.1", "stops": ["P36_1_stop"], "pos": WAYPOINT["P36_1_stop"], "kind": "pedestrian", "light_offset": (-20, -15), "label_offset": SMALL_LABEL_OFFSET},
    {"id": "35.1", "stops": ["P35_1_stop"], "pos": WAYPOINT["P35_1_stop"], "kind": "pedestrian", "light_offset": (15, -15), "label_offset": SMALL_LABEL_OFFSET},
    {"id": "35.2", "stops": ["P35_2_stop"], "pos": WAYPOINT["P35_2_stop"], "kind": "pedestrian", "label_offset": SMALL_LABEL_OFFSET, "light_offset": (-8, -28)},
    {"id": "37.2", "stops": ["P37_2_stop"], "pos": WAYPOINT["P37_2_stop"], "kind": "pedestrian", "light_offset": (-10, -30), "label_offset": SMALL_LABEL_OFFSET},
    {"id": "37.1", "stops": ["P37_1_stop"], "pos": WAYPOINT["P37_1_stop"], "kind": "pedestrian", "light_offset": (0, -30), "label_offset": SMALL_LABEL_OFFSET},
    {"id": "38.1", "stops": ["P38_1_stop"], "pos": WAYPOINT["P38_1_stop"], "kind": "pedestrian", "light_offset": (0, 25), "label_offset": SMALL_LABEL_OFFSET},
    {"id": "38.2", "stops": ["P38_2_stop"], "pos": WAYPOINT["P38_2_stop"], "kind": "pedestrian", "light_offset": (-7, -30), "label_offset": SMALL_LABEL_OFFSET},
    {"id": "31.2", "stops": ["P31_2_stop"], "pos": WAYPOINT["P31_2_stop"], "kind": "pedestrian", "light_offset": (-10, -8), "label_offset": SMALL_LABEL_OFFSET},
    {"id": "31.1", "stops": ["P31_1_stop"], "pos": WAYPOINT["P31_1_stop"], "kind": "pedestrian", "light_offset": (-15, 0), "label_offset": SMALL_LABEL_OFFSET},
    {"id": "32.1", "stops": ["P32_1_stop"], "pos": WAYPOINT["P32_1_stop"], "kind": "pedestrian", "light_offset": (20, 0), "label_offset": SMALL_LABEL_OFFSET},
    {"id": "32.2", "stops": ["P32_2_stop"], "pos": WAYPOINT["P32_2_stop"], "kind": "pedestrian", "light_offset": (20, 0), "label_offset": SMALL_LABEL_OFFSET},
]

# --- Special Barrier Traffic Light Definitions ---
_SB_XS = [S_ARM_L - 18, S_ARM_R + 18]
_SB_YS_TOP = TRAIN_Y - RAIL_GAP - 22
_SB_YS_BOTTOM = TRAIN_Y_LOWER + RAIL_GAP + 22

SB_TRAFFIC_LIGHT_DEFS = [
    {"id": "sb", "pos": pt(_SB_XS[0], _SB_YS_TOP)},
    {"id": "sb", "pos": pt(_SB_XS[0], _SB_YS_BOTTOM)},
    {"id": "sb", "pos": pt(_SB_XS[1], _SB_YS_TOP)},
    {"id": "sb", "pos": pt(_SB_XS[1], _SB_YS_BOTTOM)},
]

# --- Mappings ---
STOP_LIGHT_IDS = {
    stop_wp: d["id"]
    for d in TRAFFIC_LIGHT_DEFS
    for stop_wp in d.get("stops", [])
}

BUS_TL_ID = "42"
