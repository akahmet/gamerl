"""
This is where we hold the variables that are fixed for all games and can not be changed at any time throughout
all interactions with the game
"""

"""COMMON FIXED VARIABLES"""
MODE = ["player", "ai"]  # Can also be ai
SPEED = [1, 2, 3, 5, 6, 10, 15, 30]  # Possible speed choices
MARGIN = 20
FPS = 30
GAME_BACKGROUND = (0, 0, 0)  # RGB representation of black screen for pygame
MARGIN_BACKGROUND = (150, 0, 0)
SCOREBOARD_HEIGHT = 100
SCOREBOARD_BACKGROUND = (50, 50, 50)
SCOREBOARD_SEPARATOR_WIDTH = 2
SCOREBOARD_SEPARATOR_COLOR = (150, 150, 150)

POSSIBLE_ACTIONS = {
    "racing": [0, 1, 2],
    "snake": [0, 1, 2]
}

"""COMMON TUNABLE VARIABLES"""
GAME_SPEED = 1  # Amount of actions per second
GAME_MODE = "player"  # Can be "ai" or "player"
