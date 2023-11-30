import pygame  # noqa: E402

import game.config as c
from game.display import Display
from game.menu import Menu
from game.stats import Stats
from game.world import World
from game.map import Map
from game.player import Player
from game.credits import Credits

class Game:
    def __init__(self):
        """
        Initialize the Game class.
        Initialization includes:
        - Initializing pygame, the display and the clock
        - Setting up the menu and its stats page
        - Initializing game objects (world, race_track, player)
        - Setting up player properties
        :return: None
        """
        # initialize pygame
        pygame.init()

        # initialize screen and clock
        self.display = Display()
        self.display.set_display_size()

        # Initialize frame_update_interval using config variable
        self.frame_update_interval = c.PLAYER_FRAME_UPDATE_INTERVAL

        # set up font for text rendering - TODO: use text.py instead
        self.stats_menu_font = pygame.font.Font("assets/fonts/SuperMario256.ttf", 40)
        self.credits_font = self.stats_menu_font
        # setup menu and stats
        self.menu = Menu()
        self.stats = Stats(self.stats_menu_font)
        self.credits = Credits(self.credits_font)
        # initialize game objects
        self.world = World(c, c.WORLD_NAME, c.WORLD_DESCRIPTION, c.WORLD_POSITION)
        self.race_track = Map(c, c.MAP_NAME, c.MAP_DESCRIPTION, c.MAP_POSITION)
        self.player = Player(c, c.PLAYER_NAME, c.PLAYER_DESCRIPTION, c.PLAYER_POSITION)

        # Player properties
        self.player1 = self.player.prepare(c.PLAYER_CURRENT_FRAME)

    def start(self):
        """
        Starts the game and displays the menu options.
        :return: None
        """
        # show the menu over and over again
        while True:
            match self.menu.show():
                case 1:  # 1=start game
                    self.update()
                case 2:  # 2=quit
                    return
                case 3:  # 3=stats
                    self.stats.show()
                    continue
                case 4:  # 4=credits
                    self.credits.show()
                    continue
                # more cases e.g. for a leader board

    def update(self):
        """
        This method updates the game state and display.
        This is needed to run and play the game.
        :return: None
        """
        # Start game loop
        while True:
            # Set the current window caption
            pygame.display.set_caption(f"{c.WORLD_NAME} - {c.CURRENT_FPS}")

            # Check for events
            for event in pygame.event.get():
                # if the event type is QUIT then exit the program
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menu.show()

            # Give the game some time to process events
            pygame.time.wait(10)

            # Move the player
            self.player1 = self.player.move(self.display.screen)

            # Check if player is on the road
            self.player1 = self.player.check_for_events(self.display.screen)

            # Update both the display and fps
            self.display.draw()

    def print_config(self):
        """
        Prints game configuration details.
        This includes the world, racetrack, and player configurations.
        :return: None
        """
        self.world.print_config()
        self.race_track.print_config()
        self.player.print_config()
