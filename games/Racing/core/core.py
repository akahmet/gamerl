"""In this file we present all the classes that are used in Race game"""


from common.constants import constants as common
from games.Racing.constants import constants
from common.core import core
from games.Racing.helpers import helpers
import pygame
import numpy as np


class MyCar:
    """Instance of this class becomes player's car on the game start"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, roads_amount, direction):
        """Direction can be 0, 1, 2, where 0 means go-left,
                1 means stay where you are, 2 means go-right"""
        if direction == 0 and self.x > common.MARGIN + constants.ROAD_WIDTH / 2:
            # Want to go-left and there is a road to the left of the player
            self.x -= constants.ROAD_WIDTH
        elif direction == 2 and self.x < roads_amount * constants.ROAD_WIDTH + common.MARGIN - constants.ROAD_WIDTH / 2:
            # Want to go-right and there is a road to the right of the player
            self.x += constants.ROAD_WIDTH


class EnemyCar:
    """Instances of this class appear every other step"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.active = True

    def move(self):
        """Moves enemy car one car height down every step"""
        self.y += constants.CAR_HEIGHT

    def deactivate(self):
        """All cars that have active=False will be removed from game"""
        self.active = False


class Racing(core.Game):
    """Creates an instance of Car Racing game"""
    def __init__(self, mode=common.GAME_MODE, speed=common.GAME_SPEED, roads=constants.ROADS_AMOUNT):
        super().__init__(mode, speed)
        print("Initializing a Race Environment...")
        self.__step_counter = 0
        self.__roads_amount = roads
        self.__action_size = common.POSSIBLE_ACTIONS["racing"]
        self.__state_size = self.__roads_amount * constants.CAR_ROWS

        self.__enemy_cars = []
        self.__my_car = MyCar(constants.MY_CAR_X, constants.MY_CAR_Y)

        self.__action_frequency = common.FPS / speed
        self.__new_car_frequency = self.__action_frequency * 2
        self.__SCREEN_WIDTH = self.__roads_amount * constants.ROAD_WIDTH + common.MARGIN * 2
        self.__SCREEN_HEIGHT = constants.CAR_HEIGHT * constants.CAR_ROWS + common.MARGIN * 2 + common.SCOREBOARD_HEIGHT

        self.__state = helpers.map_cars_to_state(self.__roads_amount, self.__enemy_cars, self.__my_car)
        self.model = core.Model("racing")

    def __test_model(self):
        # Building up a fake state based on amount of roads and checking the model to return proper action
        # TODO: Make better error raise messages with examples, steps to debug and links to videos and blog
        test_state = constants.TEST_STATES[:self.__roads_amount]

        # Check if model exists
        if not self.model:
            raise ValueError("Model does not exist!")
        # Check if model has predict function
        if not self.model.predict:
            raise ValueError("Model does not have a method predict!")

        action = self.model.predict(test_state)
        if action not in constants.ACTIONS:
            raise ValueError("Model does not predict a proper action")

        return print("Model has passed required tests!")

    def get_state(self):
        return self.__state

    def describe(self):
        print("State size: {}. Action size: {}".format(self.__state_size, self.__action_size))
        return self.__state_size, self.__action_size

    def reset(self):
        self.__enemy_cars = []
        self.__step_counter = 0
        self.model = core.Model("racing")
        self.__my_car = MyCar(constants.MY_CAR_X, constants.MY_CAR_Y)
        self.__state = helpers.map_cars_to_state(self.__roads_amount, self.__enemy_cars, self.__my_car)
        return self.__state

    def __add_enemy_car(self):
        possible_indexes = helpers.make_possible_indexes(self.__roads_amount)
        coord_x, coord_y, possible_indexes = helpers.make_enemy_car_coordinates(possible_indexes)
        enemy_car = EnemyCar(coord_x, coord_y)
        self.__enemy_cars.append(enemy_car)

    def __add_multiple_enemy_cars(self):
        max_cars = 2
        possible_indexes = helpers.make_possible_indexes(self.__roads_amount)
        while max_cars > 0:
            coord_x, coord_y, possible_indexes = helpers.make_enemy_car_coordinates(possible_indexes)
            enemy_car = EnemyCar(coord_x, coord_y)
            self.__enemy_cars.append(enemy_car)
            max_cars -= 1

    def step(self, direction):
        self.__step_counter += 1

        if self.__step_counter % 2 == 0:
            if self.__roads_amount > 3:
                self.__add_multiple_enemy_cars()
            else:
                self.__add_enemy_car()

        self.__state = helpers.map_cars_to_state(self.__roads_amount, self.__enemy_cars, self.__my_car)
        done = helpers.perform_action(self.__roads_amount, direction, self.__enemy_cars, self.__my_car)
        self.__state = helpers.map_cars_to_state(self.__roads_amount, self.__enemy_cars, self.__my_car)

        return self.__state, done

    def play(self):
        if self.__mode == "ai":
            self.__test_model()
        self.__initialize_game()

    def check_accuracy(self, trials):
        __error = helpers.check_accuracy_input(trials)
        if __error:
            raise ValueError(__error)

        if self.__mode == "ai":
            print("checking accuracy of ai model")
            __crash_counter = 0
            __i = 0
            while __i < trials:
                # Reshaping next state to save as neural network input
                reshaped_state = np.reshape(self.__state, [1, self.__state_size])
                direction = self.model.predict(reshaped_state)
                _, done = self.step(direction)
                if done:
                    __crash_counter += 1
                __i += 1

            # Since new cars appear every 2 actions, random accuracy means 1 mistake every roads_amount * 2 actions
            print("Your Accuracy: {}%, Random Accuracy: {}%".format(100 - (100 * __crash_counter) / trials,
                                                                    100 - 100 / (2 * self.__roads_amount)))

            return 100 - __crash_counter * 100 / trials

    def __initialize_game(self):
        pygame.init()
        pygame.display.set_caption("Car Racing game by {}".format(self.__mode))

        size = self.__SCREEN_WIDTH, self.__SCREEN_HEIGHT
        screen = pygame.display.set_mode(size)
        # Clock is set to keep track of frames
        clock = pygame.time.Clock()
        pygame.display.flip()

        frame = 1
        action_taken = False  # To restrict input actions with game step actions
        while True:
            clock.tick(common.FPS)
            pygame.event.pump()
            for event in pygame.event.get():
                if self.__mode == "player" and not action_taken:
                    # Look for any button press action
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            action_taken = True
                            action = 0  # 0 means go left
                            helpers.move_my_car(self.__roads_amount, action, self.__my_car)

                        elif event.key == pygame.K_RIGHT:
                            action_taken = True
                            action = 2  # 2 means go right
                            helpers.move_my_car(self.__roads_amount, action, self.__my_car)

                # Quit the game if the X symbol is clicked
                if event.type == pygame.QUIT:
                    print("pressing escape")
                    pygame.quit()
                    raise SystemExit

            # Build up a black screen as a game background
            screen.fill(common.GAME_BACKGROUND)

            if frame % self.__action_frequency == 0:
                if self.__mode == "ai":
                    self.__state = helpers.map_cars_to_state(self.__roads_amount, self.__enemy_cars, self.__my_car)
                    # Reshaping next state to save as neural network input
                    reshaped_state = np.reshape(self.__state, [1, self.__state_size])
                    action = self.model.predict(reshaped_state)
                    done = helpers.perform_action(self.__roads_amount, action, self.__enemy_cars, self.__my_car)
                    self.__state = helpers.map_cars_to_state(self.__roads_amount, self.__enemy_cars, self.__my_car)

                    action_taken = False
                    if done:
                        print("Lost")

            if frame % (self.__action_frequency * 2) == 0:
                if self.__roads_amount > 3:
                    self.__add_multiple_enemy_cars()
                else:
                    self.__add_enemy_car()

            helpers.draw_state(screen, self.__enemy_cars, self.__my_car, self.__roads_amount)

            # update display
            pygame.display.flip()
            frame += 1
