"""This file implements the map class."""

# System imports
import matplotlib.pyplot

# Project imports

class map:
    """This class implements a map."""
    def __init__(self, width, height):
        """Constructor for the map class."""
        dpi = matplotlib.rcParams['figure.dpi']
        self._figure = matplotlib.pyplot.figure(figsize=(width/dpi, height/dpi))
        self._axes = self._figure.add_subplot(111)
        self._axes.set_xlim(0, width)
        self._axes.set_ylim(0, height)
        self._figure.subplots_adjust(left=0.05, right=0.98, bottom=0.04, top=0.99)
        self._figure.show()

    def __del__(self):
        """Destructor for the map class."""
        matplotlib.pyplot.close(self._figure)

    def addLine(self, x1, y1, x2, y2, color='black'):
        """Add a line to the map."""
        self._axes.plot([x1, x2], [y1, y2], color=color)

    def addCircle(self, x, y, r, color='black'):
        """Add a Circle to the map."""
        self._axes.plot(x, y, 'o', color=color, markersize=r)

    def addRectangle(self, x, y, w, h, color='black'):
        """Add a Rectangle to the map."""
        self._axes.plot([x, x+w, x+w, x, x], [y, y, y+h, y+h, y], color=color)

    def addSemiCircle(self, x, y, r, theta1, theta2, color='black'):
        """Add a SemiCircle to the map."""
        self._axes.add_patch(matplotlib.patches.Arc((x, y), 2*r, 2*r, theta1=theta1, theta2=theta2, color=color))
