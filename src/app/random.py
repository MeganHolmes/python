"""Module handles randomization operations"""

import random

def randomizeList(list):
    """Randomizes a list"""
    random.shuffle(list)
    return list

def checkLogisticRemoval(value):
    """Function has a 1/value chance of returning True, 0 always returns False"""
    if value <= 0:
        return False
    else:
        return (random.random() > 1/value)
