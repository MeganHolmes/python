"""App test file that calls all tests in the app directory."""

from . import testRandom

def main():
    """Main function for the app test program."""

    print("  Running app.random tests...")
    testRandom.main()
