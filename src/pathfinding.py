"""This is the main file for the pathfinding project."""

# System imports
import matplotlib.pyplot

# Project imports
import display.map

def main():
    """Main function for the pathfinding program."""
    map = display.map.map(1800,900)
    map.addLine(500,500,100,800, 'red')
    map.addLine(700,530,800,10, 'green')
    map.addLine(100,100,500,500, 'blue')
    map.addCircle(1400,500,50, 'magenta')
    map.addRectangle(100,100,100,100, 'cyan')
    map.addSemiCircle(1000,800,50,0,320, 'orange')

    matplotlib.pyplot.pause(10)

if __name__ == '__main__':
    main()
