from game import Game, helper
import atexit


def main():
    # This is the main function
    atexit.register(__at_exit)  # Register the at_exit function
    game = Game()  # Initialize game
    game.start()  # Start the game


# This function is called when the program exits
def __at_exit():
    helper.why_quit_if_you_can_stay()


# This is the main entry point of the program
if __name__ == "__main__":
    main()
