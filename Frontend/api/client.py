"""HTTP client helpers for the .NET simulation backend."""

import time

import requests

from config.constants import API_URL


def send_api(traffic_lights, train_arrival_ts, result):
    """Post current frontend detector state and store the backend response."""
    now = int(time.time() * 1000)

    traffic_lights_api_format = []

    for traffic_light in traffic_lights:
        traffic_lights_api_format.append({
            "id": traffic_light.id,
            "hasEntity": traffic_light.has_entity,
            "triggeredTimestamp": traffic_light.triggered_ts or now,
        })

    payload = {
        "currentTimestamp": now,
        "trainArrivalTimestamp": train_arrival_ts,
        "trafficLights": traffic_lights_api_format,
    }
    try:
        response = requests.post(
            API_URL,
            json=payload,
            timeout=2,
            headers={"ngrok-skip-browser-warning": "true"},
        )
        if response.status_code == 200:
            result["data"] = {
                "payload": response.json(),
            }
    except Exception as exc:
        print(f"API error: {exc}")


def apply_response(traffic_lights, data):
    """Apply backend traffic light states and return the railway ``sb`` state."""
    # state_map = {0: "Red", 1: "Orange", 2: "Green"}
    state_map = {0: "Red", 1: "Orange", 2: "Green", 3: "GreenRight", 4: "GreenStraightAndRight"}
    for traffic_light in traffic_lights:
        value = data.get("trafficLights", {}).get(traffic_light.id)
        if value is not None:
            traffic_light.state = state_map.get(value, str(value)) if isinstance(value, int) else str(value)
    return data.get("trafficLights", {}).get("sb")

