"""This is the main file for the pathfinding project."""

# System imports
import matplotlib.pyplot
import time

# Project imports
import display.map
import app.entity

def generateMap(map):
    map.addLine(500,500,100,800, 'red')
    map.addLine(700,530,800,10, 'green')
    map.addLine(100,100,500,500, 'blue')
    map.addCircle(1400,500,50, 'magenta')
    map.addRectangle(100,100,100,100, 'cyan')
    map.addSemiCircle(1000,800,50,0,320, 'orange')
    map.update()

def init():
    """Initialize the pathfinding program."""
    map = display.map.map(1800,900)
    generateMap(map)
    en1 = app.entity.entity(600,500,20, 'move', 'blue')
    en1.id = map.addEntity(en1)

    return map, en1

def run(map, en1):
    """Run the pathfinding program."""
    maxTime = 30
    currentTime = 0
    FPS = 15
    framePeriod = 1/FPS
    dt = 1/FPS
    lastDisplayTime = 0

    # assert(dt < 1/FPS)

    while currentTime < maxTime:
        # Simulation actions
        startTime = time.perf_counter()
        en1.run(dt)
        currentTime += dt

        # Display actions
        newDisplayTime = time.perf_counter()

        if (newDisplayTime - lastDisplayTime) >= framePeriod:
            lastDisplayTime = newDisplayTime
            map.entityUpdate(en1.id, en1.x, en1.y, en1.angle)
            map.update()

            # Prevent program from returning immediately
            matplotlib.pyplot.pause(0.01)

        # Check performance
        timeDiff = time.perf_counter() - startTime
        if timeDiff > dt*1.1:
            print("Loops taking too long "+ str(timeDiff))


def main():
    """Main function for the pathfinding program."""
    map, en1 = init()
    run(map, en1)

if __name__ == '__main__':
    main()
