"""In this file we add all the functions that will be used in Game class that are common for all games"""


from common.constants import constants as common


"""MIDDLEWARE FUNCTIONS"""

def check_input(mode, speed):
    """Checking user input and returning the corresponding errors if any"""
    if mode not in common.MODE:
        return ("Mode name is incorrect. Please choose one of the following: {}".format(
            ', '.join(str(x) for x in common.MODE)))
    if speed not in common.SPEED:
        return ("Speed value is incorrect. Please choose one of the following: {}".format(
            ', '.join(str(x) for x in common.SPEED)))
    return None
