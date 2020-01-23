"""
This is where we hold the variables that are fixed for Race game and can not be changed at any time throughout
all interactions with the game

STATE REPRESENTATION
0    0    0    0    0

1    0    0    0    1

0    0    0    0    0

0    0    1    1    0

0    0    0    0    0

0    1    0    1    0

0    0    2    0    0

"""

import pygame
from common.constants import constants as common

"""RACING FIXED VARIABLES"""
TEST_STATES = [
    [0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 2],
    [0, 0, 0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0]
]
ACTIONS = common.POSSIBLE_ACTIONS["racing"]  # 0 - go left, 1 - idle, 2 - go right
ROADS = [2, 3, 4, 5]  # Possible road choices
CAR_ROWS = 7  # Cars can fit vertically on map
ROAD_WIDTH = 80
CAR_WIDTH = 40
CAR_HEIGHT = 80

MY_CAR_X = common.MARGIN + CAR_WIDTH / 2
MY_CAR_Y = common.MARGIN + CAR_HEIGHT * CAR_ROWS - CAR_HEIGHT / 2

GAME_PLAY_HEIGHT = CAR_ROWS * CAR_HEIGHT
MY_CAR_ICON = pygame.image.load('./img/my_car.png')
ENEMY_CAR_ICON = pygame.image.load('./img/enemy_car.png')
# Line represents a separator between roads
ROAD_LINE_WIDTH = 4
ROAD_LINE_COLOR = (100, 100, 100)
ROAD_LINE_HEIGHT = GAME_PLAY_HEIGHT

"""RACING TUNABLE VARIABLES"""
ROADS_AMOUNT = 2  # Amount of car columns on map
