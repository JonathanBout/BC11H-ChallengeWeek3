import pygame
from . import config as c
from util.text import TextRenderer


class Display:
    def __init__(self):
        # Initialize pygame.display
        pygame.display.init()

        # Initialize display and clock
        self.screen = None  # Initialize display/screen
        self.clock = pygame.time.Clock()  # Initialize clock
        self.dt = 0  # add delta time

        # Initialize text renderer
        self.text_renderer = TextRenderer()

    def set_display_size(self):
        # Set display size
        self.screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))

    def draw(self):
        self.update_display_and_fps()
        self.clear_and_fill_screen()

    def update_display_and_fps(self):
        # Update the full display surface to the screen
        pygame.display.flip()

        # Set target fps
        self.clock.tick(c.MAX_FPS)

        # printing the frames per second (fps) rate
        c.CURRENT_FPS = self.clock.get_fps()

    def clear_and_fill_screen(self):
        # Clear the screen by filling it with a single color (black in this case)
        self.screen.fill((0, 0, 96))

        # Fill the screen with a custom background
        background = pygame.image.load(c.WORLD_BACKGROUND)
        background = pygame.transform.scale(background, (c.SCREEN_WIDTH * 2, c.SCREEN_HEIGHT * 2))
        self.screen.blit(background, (0, 0))
