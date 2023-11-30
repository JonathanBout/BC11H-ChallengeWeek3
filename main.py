from game import Game, helper
import atexit


def main():
    atexit.register(__at_exit)
    game = Game()  # Initialize game
    game.print_config()  # Print game config
    game.start()  # Start the game


def __at_exit():
    helper.why_quit_if_you_can_stay()


if __name__ == "__main__":
    main()
