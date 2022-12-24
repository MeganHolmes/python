"""File that implements the entity class"""


class entity:
    """This class implements an entity."""
    def __init__(self, x, y, r, mode, color='black'):
        """Constructor for the entity class."""
        self.x = x
        self.y = y
        self.r = r
        self.angle = 0
        self.color = color
        self.id = None
        self.mode = mode
        self.maxSpeed = 10

    def __del__(self):
        """Destructor for the entity class."""

    def wallFollow(self, dT):
        """Wall follow mode."""
        pass

    def simpleMove(self, dT):
        """Simple move mode."""
        self.x += dT * self.maxSpeed

    def run(self, dT):
        """Run the entity."""
        if self.mode == 'move':
            self.simpleMove(dT)
        elif self.mode == 'wallFollow':
            self.wallFollow(dT)

    def setId(self, id):
        self.id = id
