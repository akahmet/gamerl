"""In this file we add all the functions that will be used in Racing class"""

from common.constants import constants as common
from games.Racing.constants import constants
import random
import pygame

"""MIDDLEWARE"""


def make_possible_indexes(roads_amount):
    # To hold a list of possible indexes for a new enemy car to appear at
    possible_indexes = []
    for i in range(roads_amount):
        possible_indexes.append(i)

    return possible_indexes


def check_accuracy_input(trials):
    # Check if the trials number is integer and if it is greater than zero
    if trials <= 0 or not isinstance(trials, int):
        return "Trials number must be integer greater than 0"


def make_enemy_car_coordinates(possible_indexes):
    # Map actual x and y coordinates to cells
    road_index = random.randrange(len(possible_indexes))
    coord_x = common.MARGIN + constants.ROAD_WIDTH / 2 + constants.ROAD_WIDTH * possible_indexes.pop(road_index)
    coord_y = common.MARGIN + constants.CAR_HEIGHT / 2

    return coord_x, coord_y, possible_indexes


def map_cars_to_state(roads_amount, enemy_cars, my_car):
    # Lines will be a list of lists (ie matrix) to represent the state
    lines, my_position = make_lines(roads_amount, enemy_cars, my_car)
    return lines


def make_lines(roads_amount, enemy_cars, my_car):
    # Build up a matrix representing a full state where 0 means empty cell, 1 means my_car, 2 means enemy car
    lines = build_empty_lines(roads_amount)
    for car in enemy_cars:
        # 2 is a label representing enemy cars
        coord_x = (car.x - common.MARGIN) // constants.ROAD_WIDTH
        coord_y = (car.y - common.MARGIN) // constants.CAR_HEIGHT
        # Not to include cars that are outside of the boundaries
        if int(coord_x) < len(lines) and int(coord_y) < len(lines[0]):
            lines[int(coord_x)][int(coord_y)] = 2
    # 1 is a label representing my car
    my_coord_x = (my_car.x - common.MARGIN) // constants.ROAD_WIDTH
    my_coord_y = (my_car.y - common.MARGIN) // constants.ROAD_WIDTH
    lines[int(my_coord_x)][int(my_coord_y)] = 1

    return lines, int(my_coord_x)


def build_empty_lines(roads_amount):
    # Build up a placeholder that has all zeros representing each cell of the state
    lines = []
    for i in range(roads_amount):
        line = []
        # +1 is to hold 1 row under the screen bottom wall to remove enemy car when reaches that position
        for j in range(constants.CAR_ROWS):
            line.append(0)
        lines.append(line)

    return lines


def check_if_lost(enemy_cars, my_car):
    # For all enemy cars on the map check if x and y coordinates are equal to my_car's
    for car in enemy_cars:
        if car.x == my_car.x and car.y == my_car.y:
            return True

    return False


def move_my_car(roads_amount, direction, my_car):
    # Move player's car
    my_car.move(roads_amount, direction)


def deactivate_cars(enemy_cars):
    # Check if a car is outside of map boundaries, then deactivate it
    for car in enemy_cars:
        # If the enemy_car has reached the bottom of any road line, deactivate it
        if car.y > constants.GAME_PLAY_HEIGHT - common.MARGIN - constants.CAR_HEIGHT / 2:
            car.active = False

    # Remove all deactivated cars
    for car in enemy_cars:
        if not car.active:
            enemy_cars.remove(car)


def move_enemy_cars(enemy_cars):
    # Move enemy cars
    for car in enemy_cars:
        car.move()


def perform_action(roads_amount, direction, enemy_cars, my_car):
    # Make a given action and update the state based on it
    move_enemy_cars(enemy_cars)
    move_my_car(roads_amount, direction, my_car)
    deactivate_cars(enemy_cars)

    return check_if_lost(enemy_cars, my_car)


"""DRAWING FUNCTIONS"""


def draw_road_lines(screen, roads_amount):
    # Left line margin
    pygame.draw.rect(screen, constants.ROAD_LINE_COLOR, (0, 0, common.MARGIN, constants.ROAD_LINE_HEIGHT))
    # Right line margin
    pygame.draw.rect(screen, constants.ROAD_LINE_COLOR, (common.MARGIN + roads_amount * constants.ROAD_WIDTH, 0,
                                                         common.MARGIN, constants.ROAD_LINE_HEIGHT))
    # Middle lines that separate roads
    for i in range(roads_amount - 1):
        pygame.draw.rect(screen, constants.ROAD_LINE_COLOR,
                         (common.MARGIN + constants.ROAD_WIDTH * (i + 1) - constants.ROAD_LINE_WIDTH / 2, 0,
                          constants.ROAD_LINE_WIDTH, constants.ROAD_LINE_HEIGHT))


def draw_state(screen, enemy_cars, my_car, roads_amount):
    # Draw all lines and all cars
    draw_road_lines(screen, roads_amount)
    for car in enemy_cars:
        screen.blit(constants.ENEMY_CAR_ICON, (car.x - constants.CAR_WIDTH / 2, car.y - constants.CAR_HEIGHT / 2))

    screen.blit(constants.MY_CAR_ICON, (my_car.x - constants.CAR_WIDTH / 2, my_car.y - constants.CAR_HEIGHT / 2))
