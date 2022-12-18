"""Call test functions in all subdirectories."""

# Project imports
import app.test.test


def main():
    """Main function for the test program."""
    print("Running tests...")

    print(" Running app tests...")
    app.test.test.main()

    print("Tests complete.")


if __name__ == '__main__':
    main()
