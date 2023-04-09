"""This file contains misc math functions."""


# System imports
import math

def pointLineDistance(x, y, x1, y1, x2, y2):
    """Calculate the distance between a point and a line."""
    # Check if the line is vertical
    if x1 == x2:
        return abs(x - x1)
    else:
        # Calculate the slope and y-intercept of the line
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1

        # Calculate the distance between the point and the line
        return abs(m * x - y + b) / math.sqrt(m**2 + 1)
