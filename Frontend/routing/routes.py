"""Route definitions for cars, buses, cyclists, and pedestrians."""
from config.geometry import (
    BIKE_EAST_X_IN,
    BIKE_EAST_X_OUT,
    BIKE_EAST_Y_IN,
    BIKE_EAST_Y_OUT,
    BIKE_MID_Y,
    BIKE_NORTH_Y_IN,
    BIKE_NORTH_Y_OUT,
    BIKE_SOUTH_E_X_IN,
    BIKE_SOUTH_E_X_OUT,
    BIKE_SOUTH_W_X_IN,
    BIKE_SOUTH_W_X_OUT,
    BIKE_WEST_X_IN,
    BIKE_WEST_X_OUT,
    BIKE_WEST_Y_IN,
    BIKE_WEST_Y_OUT,
    BOX_B,
    BOX_R,
    BOX_T,
    LANE_W,
    PED_EAST_X,
    PED_EAST_Y,
    PED_NORTH_E_X,
    PED_NORTH_Y,
    PED_SOUTH_E_X,
    PED_SOUTH_JOIN_Y,
    PED_SOUTH_W_X,
    PED_WEST_X,
    PED_WEST_Y,
    TRAIN_Y,
    WAYPOINT,
    get_east_lane_y,
    get_north_lane_x,
    pt,
    get_south_lane_x,
    get_west_lane_y,
)
from routing.pathfinding import build_boundary_routes
from config.traffic_lights import TRAFFIC_LIGHT_DEFS, BUS_TL_ID


def build_routes():
    """Build the fixed car and bus routes through the intersection."""
    routes = []
    routes.append(("10.1", ["N1_entry", "N1_stop", "N1_box", pt(get_north_lane_x(1), get_west_lane_y(1)), "W1_exit"]))
    routes.append(("11.1", ["N2_entry", "N2_stop", "N2_box", pt(get_south_lane_x(1), BOX_B - LANE_W // 2), "S1_trainStop", "S1_exit"]))
    routes.append(("12.1", ["N3_entry", "N3_stop", "N3_box", pt(BOX_R - LANE_W // 2, get_east_lane_y(5)), "E5_exit"]))
    routes.append(("12.1", ["N4_entry", "N4_stop", "N4_box", pt(BOX_R - LANE_W // 2, get_east_lane_y(4)), "E4_exit"]))
    routes.append(("42", ["E1_entry", "E1_stop", "E1_box", pt(get_north_lane_x(5), BOX_T + LANE_W // 2), "N5_exit"]))
    routes.append(("42", ["E1_entry", "E1_stop", "E1_box", pt(get_north_lane_x(5), get_west_lane_y(1)), "W1_exit"]))
    routes.append(("1.1", ["E2_entry", "E2_stop", "E2_box", pt(get_north_lane_x(5), BOX_T + LANE_W // 2), "N5_exit"]))
    routes.append(("2.1", ["E3_entry", "E3_stop", "E3_box", pt(get_north_lane_x(1), get_west_lane_y(1)), "W1_exit"]))
    routes.append(("6.1", ["S2_entry", "S2_stop", "S2_box", pt(get_north_lane_x(1), get_west_lane_y(1)), "W1_exit"]))
    routes.append(("5.1", ["S3_entry", "S3_stop", "S3_box", pt(get_north_lane_x(5), BOX_T + LANE_W // 2), "N5_exit"]))
    routes.append(("5.1", ["S3_entry", "S3_stop", "S3_box", pt(BOX_R - LANE_W // 2, get_east_lane_y(5)), "E5_exit"]))
    routes.append(("9.1", ["W2_entry", "W2_stop", "W2_box", pt(get_north_lane_x(5), BOX_T + LANE_W // 2), "N5_exit"]))
    routes.append(("8.1", ["W3_entry", "W3_stop", "W3_box", pt(BOX_R - LANE_W // 2, get_east_lane_y(5)), "E5_exit"]))
    routes.append(("7.1", ["W4_entry", "W4_stop", "W4_box", pt(get_south_lane_x(1), BOX_B - LANE_W // 2), "S1_trainStop", "S1_exit"]))
    return routes


def build_cyclist_routes():
    """Build all cyclist routes between bicycle lane entry and exit points."""
    graph = {
        "N0": ["NW"],
        "NW": ["N0", "SW", "NE"],
        "W5": ["SW"],
        "SW": ["W5", "S0", "NW"],
        "S0": ["SW"],
        "N6": ["NE"],
        "NE": ["N6", "E0", "NW", "SE"],
        "E0": ["NE"],
        "SE": ["NE", "S4"],
        "S4": ["SE"],
    }
    segments = {
        ("N0", "NW"): ["N0_entry", pt(BIKE_WEST_X_IN, BIKE_NORTH_Y_OUT)],
        ("NW", "N0"): [pt(BIKE_WEST_X_OUT, BIKE_NORTH_Y_OUT), "N0_exit"],
        ("W5", "SW"): ["W5_entry", pt(BIKE_WEST_X_IN, BIKE_WEST_Y_IN)],
        ("SW", "W5"): [pt(BIKE_WEST_X_OUT, BIKE_WEST_Y_OUT), "W5_exit"],
        ("S0", "SW"): [
            "S0_entry",
            "S0_in_trainStop",
            pt(BIKE_SOUTH_W_X_IN, TRAIN_Y + 10),
            pt(BIKE_SOUTH_W_X_IN - 8, BIKE_MID_Y),
            pt(BIKE_WEST_X_OUT, BIKE_WEST_Y_IN),
        ],
        ("SW", "S0"): [
            pt(BIKE_WEST_X_IN, BIKE_WEST_Y_IN),
            pt(BIKE_SOUTH_W_X_OUT - 4, BIKE_MID_Y),
            "S0_out_trainStop",
            "S0_exit",
        ],
        ("NW", "SW"): ["B26_1_stop", pt(BIKE_WEST_X_IN, BIKE_WEST_Y_IN)],
        ("SW", "NW"): ["B86_1_stop", pt(BIKE_WEST_X_OUT, BIKE_NORTH_Y_IN)],
        ("NW", "NE"): ["B88_1_stop", pt(BIKE_EAST_X_OUT, BIKE_NORTH_Y_IN)],
        ("NE", "NW"): ["B28_1_stop", pt(BIKE_WEST_X_OUT, BIKE_NORTH_Y_OUT)],
        ("N6", "NE"): ["N6_entry", pt(BIKE_EAST_X_IN, BIKE_NORTH_Y_OUT)],
        ("NE", "N6"): [pt(BIKE_EAST_X_OUT, BIKE_NORTH_Y_OUT), "N6_exit"],
        ("E0", "NE"): ["E0_entry", pt(BIKE_EAST_X_OUT, BIKE_EAST_Y_IN)],
        ("NE", "E0"): [pt(BIKE_EAST_X_OUT, BIKE_EAST_Y_OUT), "E0_exit"],
        ("NE", "SE"): ["B22_in_stop", pt(BIKE_EAST_X_IN, BIKE_WEST_Y_IN)],
        ("SE", "NE"): ["B22_out_stop", pt(BIKE_EAST_X_OUT, BIKE_NORTH_Y_IN)],
        ("S4", "SE"): [
            "S4_entry",
            "S4_in_trainStop",
            pt(BIKE_SOUTH_E_X_IN, TRAIN_Y + 10),
            pt(BIKE_SOUTH_E_X_IN - 12, BIKE_MID_Y),
            pt(BIKE_EAST_X_OUT, BIKE_WEST_Y_IN),
        ],
        ("SE", "S4"): [
            pt(BIKE_EAST_X_IN, BIKE_WEST_Y_IN),
            pt(BIKE_SOUTH_E_X_OUT - 8, BIKE_MID_Y),
            "S4_out_trainStop",
            "S4_exit",
        ],
    }
    return build_boundary_routes(graph, segments, ["N0", "N6", "E0", "S0", "S4", "W5"])


def build_pedestrian_routes():
    """Build all pedestrian routes between pedestrian lane entry and exit points."""
    graph = {
        "NZ": ["NW"],
        "NW": ["NZ", "SW", "NE"],
        "W6": ["SW"],
        "SW": ["W6", "SZ", "NW"],
        "SZ": ["SW"],
        "N7": ["NE"],
        "NE": ["N7", "EZ", "NW", "SE"],
        "EZ": ["NE"],
        "SE": ["NE", "S5"],
        "S5": ["SE"],
    }
    segments = {
        ("NZ", "NW"): ["NZ_entry", pt(PED_WEST_X, PED_NORTH_Y)],
        ("NW", "NZ"): [pt(PED_WEST_X, PED_NORTH_Y), "NZ_exit"],
        ("W6", "SW"): ["W6_entry", pt(PED_WEST_X, PED_WEST_Y)],
        ("SW", "W6"): [pt(PED_WEST_X, PED_WEST_Y), "W6_exit"],
        ("SZ", "SW"): [
            "SZ_entry",
            "SZ_in_trainStop",
            pt(PED_SOUTH_W_X, PED_SOUTH_JOIN_Y),
            pt(PED_WEST_X, PED_WEST_Y),
        ],
        ("SW", "SZ"): [
            pt(PED_SOUTH_W_X, PED_SOUTH_JOIN_Y),
            "SZ_out_trainStop",
            "SZ_exit",
        ],
        ("NW", "SW"): ["P36_2_stop", "P35_1_stop", pt(PED_WEST_X, PED_WEST_Y)],
        ("SW", "NW"): ["P35_2_stop", "P36_1_stop", pt(PED_WEST_X, PED_NORTH_Y)],
        ("NW", "NE"): ["P37_2_stop", "P38_1_stop", pt(PED_EAST_X, PED_NORTH_Y)],
        ("NE", "NW"): ["P38_2_stop", "P37_1_stop", pt(PED_WEST_X, PED_NORTH_Y)],
        ("N7", "NE"): ["N7_entry", pt(PED_NORTH_E_X, PED_NORTH_Y), pt(PED_EAST_X, PED_NORTH_Y)],
        ("NE", "N7"): [pt(PED_NORTH_E_X, PED_NORTH_Y), "N7_exit"],
        ("EZ", "NE"): ["EZ_entry", pt(PED_EAST_X, PED_EAST_Y)],
        ("NE", "EZ"): [pt(PED_EAST_X, PED_EAST_Y), "EZ_exit"],
        ("NE", "SE"): ["P31_2_stop", "P32_1_stop", pt(PED_EAST_X, PED_WEST_Y)],
        ("SE", "NE"): ["P32_2_stop", "P31_1_stop", pt(PED_EAST_X, PED_NORTH_Y)],
        ("S5", "SE"): [
            "S5_entry",
            "S5_in_trainStop",
            pt(PED_SOUTH_E_X, PED_SOUTH_JOIN_Y),
            pt(PED_EAST_X, PED_WEST_Y),
        ],
        ("SE", "S5"): [
            pt(PED_SOUTH_E_X, PED_SOUTH_JOIN_Y),
            "S5_out_trainStop",
            "S5_exit",
        ],
    }
    return build_boundary_routes(graph, segments, ["NZ", "N7", "EZ", "SZ", "S5", "W6"])


def resolve_routes(raw):
    """Resolve waypoint keys into coordinates while keeping the original keys."""
    out = []
    for tl_id, keys in raw:
        coords = [WAYPOINT[k] if isinstance(k, str) else k for k in keys]
        out.append((tl_id, coords, keys))
    return out


# Mapping of stop waypoint keys to traffic light IDs for signal stopping logic.
# so the logic knows which trafficlight belongs to which stop waypoint
STOP_LIGHT_IDS = {
    stop_wp: d["id"]
    for d in TRAFFIC_LIGHT_DEFS
    for stop_wp in d.get("stops", ([d["stop"]] if "stop" in d else []))
}

_ALL_ROUTES = resolve_routes(build_routes())
CAR_ROUTES = [(tl, c, k) for tl, c, k in _ALL_ROUTES if tl != BUS_TL_ID]
BUS_ROUTES = [(tl, c, k) for tl, c, k in _ALL_ROUTES if tl == BUS_TL_ID]
CYCLIST_ROUTES = resolve_routes(build_cyclist_routes())
PEDESTRIAN_ROUTES = resolve_routes(build_pedestrian_routes())
