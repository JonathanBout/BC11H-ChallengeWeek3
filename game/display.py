import pygame
from game import config
from game.map_manager import MapConfig
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
        logo = pygame.image.load(config.GAME_ICON)
        small_logo = pygame.transform.scale(logo, (32, 32))
        pygame.display.set_icon(small_logo)

        # Initialize display and clock
        self.screen = None  # Initialize display/screen
        self.clock = pygame.time.Clock()  # Initialize clock
        self.dt = 0  # add delta time
        self.score_font = pygame.font.Font(config.SUPER_MARIO_FONT, 30)

        # Initialize text renderer
        self.text_renderer = TextRenderer()

    def set_display_size(self):
        """
        Sets the display size for the game.
        :return: None
        """
        # Set display size
        self.screen = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )
        return self.screen

    def draw(self, map: MapConfig):
        """
        Update the display and clear the screen.
        :return: None
        """
        self.update_display_and_fps()
        self.clear_and_fill_screen(map)

    def update_display_and_fps(self):
        """
        Update the display and FPS.
        :return: None
        """
        # Update the full display surface to the screen
        pygame.display.flip()

        # Set target fps and seconds per frame (see https://www.reddit.com/r/pygame/comments/k7677j/comment/gep295w/)
        config.SECONDS_PER_FRAME = self.clock.tick(config.MAX_FPS) / 1000

        # Printing the frames per second (fps) rate
        config.CURRENT_FPS = self.clock.get_fps()

    def clear_and_fill_screen(self, map: MapConfig):
        """
        Clears the screen and fills it with a custom background.
        :return: None
        """
        # Clear the screen by filling it with a single color (black in this case)
        self.screen.fill((0, 0, 96))

        # Fill the screen with a custom background
        background = pygame.image.load(map.background_image)
        background = pygame.transform.scale(
            background, (config.SCREEN_WIDTH * 2, config.SCREEN_HEIGHT * 2)
        )
        current_lap = config.RACE_CURRENT_LAP

        text = self.score_font.render(
            f"{current_lap}/{config.RACE_LAPS}", True, "white", "gray"
        )
        self.screen.blit(background, config.MAP_POSITION)
        self.screen.blit(text, (10, 10))
