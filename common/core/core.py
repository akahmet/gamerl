"""In this file we add all the classes that are common for all games of the library"""


from common.constants import constants as common
from common.helpers import helpers
import random


class Model:
    """Creates an example of a deep learning model instance"""
    def __init__(self, game_name):
        self.possible_actions = common.POSSIBLE_ACTIONS[game_name]

    def predict(self, state):
        action_index = random.randrange(len(self.possible_actions))
        action = self.possible_actions[action_index]
        return action


class Game:
    """Creates a game instance with common properties, the rest of the fields are presented by exact game class"""
    def __init__(self, mode=common.GAME_MODE, speed=common.GAME_SPEED):
        # Check if user inputs are correct
        __error = helpers.check_input(mode, speed)
        if __error:
            raise ValueError(__error)

        self.__mode = mode
        self.__speed = speed
