"""This file implements the map class."""

# System imports
import matplotlib.pyplot

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

        self.lines = []
        self.circles = []
        self.rectangles = []
        self.semiCircles = []
        self.entities = []

    def __del__(self):
        """Destructor for the map class."""
        matplotlib.pyplot.close(self._figure)

    def addLine(self, x1, y1, x2, y2, color='black'):
        """Add a line to the map."""
        line = (x1, y1, x2, y2, color)  # Create a tuple representing the line
        self.lines.append(line)  # Add the line to the list

    def addCircle(self, x, y, r, color='black'):
        """Add a Circle to the map."""
        circle = (x, y, r, color)  # Create a tuple representing the circle
        self.circles.append(circle)  # Add the circle to the list

    def addRectangle(self, x, y, w, h, color='black'):
        """Add a Rectangle to the map."""
        rectangle = (x, y, w, h, color)  # Create a tuple representing the rectangle
        self.rectangles.append(rectangle)  # Add the rectangle to the list

    def addSemiCircle(self, x, y, r, theta1, theta2, color='black'):
        """Add a SemiCircle to the map."""
        semiCircle = (x, y, r, theta1, theta2, color)  # Create a tuple representing the semi-circle
        self.semiCircles.append(semiCircle)  # Add the semi-circle to the list

    def addEntity(self, entity):
        """Add an entity to the map."""
        id = len(self.entities)  # Get the id of the entity
        newEntity = (entity.x, entity.y, entity.r, entity.color, entity.angle)  # Create a tuple representing the entity
        self.entities.append(newEntity)
        return id

    def entityUpdate(self, id, x, y, angle):
        """Update the position and angle of an entity."""
        self.entities[id] = (x, y, self.entities[id][2], self.entities[id][3], angle)

    def update(self):
        """Update the map."""
        # Clear the map
        self._axes.clear()

        # Add all of the lines to the map
        for line in self.lines:
            x1, y1, x2, y2, color = line
            self._axes.plot([x1, x2], [y1, y2], color=color)

        # Add all of the circles to the map
        for circle in self.circles:
            x, y, r, color = circle
            self._axes.plot(x, y, 'o', color=color, markersize=r)

        # Add all of the rectangles to the map
        for rectangle in self.rectangles:
            x, y, w, h, color = rectangle
            self._axes.plot([x, x+w, x+w, x, x], [y, y, y+h, y+h, y], color=color)

        # Add all of the semi-circles to the map
        for semiCircle in self.semiCircles:
            x, y, r, theta1, theta2, color = semiCircle
            self._axes.add_patch(matplotlib.patches.Arc((x, y), 2*r, 2*r, theta1=theta1, theta2=theta2, color=color))

        # Add all of the entities to the map
        for entity in self.entities:
            x, y, r, color, angle = entity
            self._axes.add_patch(matplotlib.patches.Circle((x, y), r, color=color, fill=False))
            self._axes.plot([x, x+r], [y, y], color=color)

        # Redraw the map
        self._figure.canvas.draw()
