"""Pygame application loop for the traffic simulation."""

import os
import threading
import time

import pygame

from api.client import apply_response, send_api
from config.constants import (
    API_INTERVAL,
    BICYCLE_SPAWN_INTERVAL,
    BUS_SPAWN_INTERVAL,
    CAR_COLOR,
    CAR_SPAWN_INTERVAL,
    FPS,
    HEIGHT,
    INITIAL_TRAIN_DELAY_SECONDS,
    PEDESTRIAN_SPAWN_INTERVAL,
    WIDTH, TRAIN_REPEAT_SECONDS,
)
from config.traffic_lights import TRAFFIC_LIGHT_DEFS, SB_TRAFFIC_LIGHT_DEFS
from config.geometry import TRAIN_Y, TRAIN_Y_LOWER
from entities.bus import Bus
from entities.car import Car
from entities.cyclist import Cyclist
from entities.pedestrian import Pedestrian
from entities.train import Train
from rendering.road import draw_road
from rendering.ui import draw_ui
from routing.routes import BUS_ROUTES, CAR_ROUTES, CYCLIST_ROUTES, PEDESTRIAN_ROUTES, STOP_LIGHT_IDS
from traffic.sb_traffic_light import SbTrafficLight
from traffic.traffic_light import TrafficLight
from train.crossing_controller import TrainCrossingController
from train.railway_barriers import RailwayBarriers


def update_waiting_sensors(vehicles, tls, stop_tl):
    """set trafficlight sensors as having a entity when there is one waiting."""
    for tl in tls:
        tl.has_entity = False
    for vehicle in vehicles:
        if vehicle.waiting and vehicle.target < len(vehicle.keys):
            key = vehicle.keys[vehicle.target]
            if isinstance(key, str) and "_stop" in key and "_train" not in key:
                tl = stop_tl.get(key)
                if tl:
                    tl.has_entity = True
                    if tl.triggered_ts is None:
                        tl.triggered_ts = int(time.time() * 1000)


def clear_served_sensor_timestamps(tls):
    """Clear timestamps for sensors that dont have an entity anymore"""
    for tl in tls:
        if not tl.has_entity:
            if tl.state == "Green":
                tl.triggered_ts = None


def main():
    """Main simulation function for initializing everything and running the sim loop"""
    # os.environ["SDL_VIDEO_WINDOW_POS"] = "500,300"
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simulation")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 12)

    # create traffic lights and map of stop waypoint to traffic light for easy sensor updates
    traffic_lights = [TrafficLight(definition) for definition in TRAFFIC_LIGHT_DEFS]
    traffic_lights_map = {traffic_light.id: traffic_light for traffic_light in traffic_lights}
    sb_traffic_lights = [SbTrafficLight(definition) for definition in SB_TRAFFIC_LIGHT_DEFS]
    stop_tl = {
        stop_wp: traffic_lights_map[light_id]
        for stop_wp, light_id in STOP_LIGHT_IDS.items()
        if light_id in traffic_lights_map
    }

    # variables to track vehicles, trains, barriers, crossing state, and api timing/state
    vehicles = []
    last_car_spawn = time.time()
    last_bus_spawn = time.time()
    last_bike_spawn = time.time()
    last_pedestrian_spawn = time.time()
    last_api = time.time()
    car_route_index = 0
    bus_route_index = 0
    bike_route_index = 0
    pedestrian_route_index = 0
    api_result = {"data": None}
    trains = []
    barriers = RailwayBarriers()
    crossing = TrainCrossingController()
    next_train_time = time.time() + INITIAL_TRAIN_DELAY_SECONDS
    train_arrival_ts = int(next_train_time * 1000)

    # main simulation loop
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        now = time.time()

        # check for quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # spawn train if the crossing controller indicates to and we are at the arrival time
        if crossing.should_spawn_train(now):
            if not crossing.train_spawned:
                trains.append(Train(TRAIN_Y, 1))
                trains.append(Train(TRAIN_Y_LOWER, -1))
                crossing.mark_train_spawned()
                # Set the next train arrival time
                next_train_time = now + TRAIN_REPEAT_SECONDS
                train_arrival_ts = int(next_train_time * 1000)
                crossing.active_arrival_ts = train_arrival_ts

        # remove any trains that have completed their route
        trains = [train for train in trains if not train.done]
        for train in trains:
            train.update(dt)
        for sb_light in sb_traffic_lights:
            sb_light.update(dt)

        # spawn car on interval
        if now - last_car_spawn >= CAR_SPAWN_INTERVAL:
            _tl_id, coords, keys = CAR_ROUTES[car_route_index % len(CAR_ROUTES)]
            vehicles.append(Car(list(coords), list(keys), CAR_COLOR))
            car_route_index += 1
            last_car_spawn = now

        # spawn bus on interval
        if now - last_bus_spawn >= BUS_SPAWN_INTERVAL:
            _tl_id, coords, keys = BUS_ROUTES[bus_route_index % len(BUS_ROUTES)]
            vehicles.append(Bus(list(coords), list(keys)))
            bus_route_index += 1
            last_bus_spawn = now

        # spawn cyclist/bike on interval
        if now - last_bike_spawn >= BICYCLE_SPAWN_INTERVAL:
            _route_id, coords, keys = CYCLIST_ROUTES[bike_route_index % len(CYCLIST_ROUTES)]
            vehicles.append(Cyclist(list(coords), list(keys)))
            bike_route_index += 1
            last_bike_spawn = now

        # spawn pedestrian on interval
        if now - last_pedestrian_spawn >= PEDESTRIAN_SPAWN_INTERVAL:
            _route_id, coords, keys = PEDESTRIAN_ROUTES[pedestrian_route_index % len(PEDESTRIAN_ROUTES)]
            vehicles.append(Pedestrian(list(coords), list(keys)))
            pedestrian_route_index += 1
            last_pedestrian_spawn = now

        # remove any vehicles that have completed their route
        vehicles = [vehicle for vehicle in vehicles if not vehicle.done]

        # update trafficlight sensors based on waiting vehicles at the stop lines
        update_waiting_sensors(vehicles, traffic_lights, stop_tl)
        # clear sensor timestamps for any that no longer have a waiting vehicle
        clear_served_sensor_timestamps(traffic_lights)

        # update vehicles and check if they can move
        # based on trafficlight states and crossing state
        for vehicle in vehicles:
            vehicle.resume_if_green(traffic_lights_map, crossing.road_blocked)
            vehicle.update(dt, traffic_lights_map, vehicles, crossing.road_blocked)

        # send api request on interval
        if now - last_api >= API_INTERVAL:
            last_api = now
            threading.Thread(
                target=send_api,
                args=(traffic_lights, train_arrival_ts, api_result),
                daemon=True,
            ).start()

        # apply api response and sync crossing state from backend sb value
        if api_result["data"]:
            response_data = api_result["data"]
            sb_state = apply_response(traffic_lights, response_data["payload"])
            crossing.active_arrival_ts = train_arrival_ts
            crossing.sync_backend_state(
                sb_state,
                train_arrival_ts,
                now
            )
            api_result["data"] = None

        # update the railway barriers and crossing state
        barriers.update(
            dt,
            crossing.barriers_should_close,
            crossing.barriers_should_open
        )
        crossing.update(now, barriers.is_open())

        # if there isnt an active train arrival time, create new one
        # if crossing.active_arrival_ts is None:
        if train_arrival_ts == 0:
            train_arrival_ts = int(next_train_time * 1000)

        # update sb lights based on crossing state
        for sb_light in sb_traffic_lights:
            sb_light.signal_state = crossing.backend_state
            sb_light.blinking_active = crossing.blinking_active

        # draw the roads
        draw_road(screen, font)

        # draw the trains
        for train in trains:
            train.draw(screen)
        # draw the vehicles and barriers on top
        for vehicle in vehicles:
            vehicle.draw(screen)
        barriers.draw(screen)

        # draw traffic lights
        for tl in traffic_lights:
            tl.draw(screen, font)

        # draw sb traffic lights
        for sb_light in sb_traffic_lights:
            sb_light.draw(screen, font)

        # draw the UI panel
        draw_ui(screen, font, vehicles, traffic_lights, last_api, train_arrival_ts)
        # update the display
        pygame.display.flip()

    pygame.quit()