import pygame
import game.config as c
from util.text import TextRenderer


class Display:
    def __init__(self):
        """
        This method initializes the Display object.
        :param None:
        :return: None
        """
        # Initialize pygame.display
        pygame.display.init()

        # Set logo
        logo = pygame.image.load(c.GAME_ICON)
        small_logo = pygame.transform.scale(logo, (32, 32))
        pygame.display.set_icon(small_logo)

        # Initialize display and clock
        self.screen = None  # Initialize display/screen
        self.clock = pygame.time.Clock()  # Initialize clock
        self.dt = 0  # add delta time

        # Initialize text renderer
        self.text_renderer = TextRenderer()

    def set_display_size(self):
        """
        Sets the display size for the game.
        :return: None
        """
        # Set display size
        self.screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        return self.screen

    def draw(self):
        """
        Update the display and clear the screen.
        :return: None
        """
        self.update_display_and_fps()
        self.clear_and_fill_screen()

    def update_display_and_fps(self):
        """
        Update the display and FPS.
        :return: None
        """
        # Update the full display surface to the screen
        pygame.display.flip()

        # Set target fps
        self.clock.tick(c.MAX_FPS)

        # Printing the frames per second (fps) rate
        c.CURRENT_FPS = self.clock.get_fps()

    def clear_and_fill_screen(self):
        """
        Clears the screen and fills it with a custom background.
        :return: None
        """
        # Clear the screen by filling it with a single color (black in this case)
        self.screen.fill((0, 0, 96))

        # Fill the screen with a custom background
        background = pygame.image.load(c.WORLD_BACKGROUND)
        background = pygame.transform.scale(
            background, (c.SCREEN_WIDTH * 2, c.SCREEN_HEIGHT * 2)
        )
        self.screen.blit(background, c.MAP_POSITION)
