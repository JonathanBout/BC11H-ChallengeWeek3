import pygame

import game.config
from game.camera import Camera  # noqa: E402

import game.config as c
from game.display import Display
from game.game_over import GameOver
from game.menu import Menu
from game.score_manager import ScoreManager
from game.stats import Stats
from game.world import World
from game.map import Map
from game.player import Player
from game.credits import Credits
from util.music import Music


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
        self.game_over_font = self.stats_menu_font
        # setup menu and stats
        self.menu = Menu()
        self.stats = Stats(self.stats_menu_font)
        self.credits = Credits(self.credits_font)
        self.game_over = GameOver(self.game_over_font)
        self.score_manager = ScoreManager()
        # initialize game objects
        self.world = World(c, c.WORLD_NAME, c.WORLD_DESCRIPTION, c.WORLD_POSITION)
        self.race_track = Map(c, c.MAP_NAME, c.MAP_DESCRIPTION, c.MAP_POSITION)
        self.player = Player(c, c.PLAYER_NAME, c.PLAYER_DESCRIPTION, c.PLAYER_POSITION)
        self.camera = Camera()
        # Player properties
        self.player1 = self.player.prepare(c.PLAYER_CURRENT_FRAME)
        # Music
        self.rainbow_road_music = Music(c.MUSIC_RAINBOW_ROAD, 0)

    def start(self):
        """
        Starts the game and displays the menu options.
        :return: None
        """
        # show the menu over and over again
        self.show_menu(False)

    def update(self):
        self.score_manager.start()
        """
        This method updates the game state and display.
        This is needed to run and play the game.
        :return: None
        """
        # Start game loop

        run_game = True
        did_win = False
        should_show_main_menu = False
        if run_game:
            self.rainbow_road_music.set_volume(0.1)
            self.rainbow_road_music.play(-1)

        while run_game:
            # Set the current window caption
            pygame.display.set_caption(f"{c.WORLD_NAME} - {c.CURRENT_FPS:.2f}")

            # Check for events
            for event in pygame.event.get():
                # if the event type is QUIT then exit the program
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        c.GAME_PAUSED = True
                        self.pause()
                        if not self.show_menu(True):
                            run_game = False
                            should_show_main_menu = True
                            break
                        self.resume()
                        c.GAME_PAUSED = False
                if event.type == c.GAME_PAUSE_CHANGED:
                    if c.GAME_PAUSED:
                        self.pause()
                    else:
                        self.resume()
                if event.type == c.PLAYER_GAMEOVER_EVENT:
                    self.camera.reset()
                    run_game = False
                    did_win = False
                    break
                if event.type == c.PLAYER_WON_EVENT:
                    run_game = False
                    did_win = True
                    break

            if not run_game:
                break

            # Move the player
            self.player1 = self.player.move(self.display.screen, self.camera)

            # Check if player is on the road

            # Update both the display and fps
            self.display.draw()

            self.player1 = self.player.check_for_events(self.display.screen)

        self.camera.reset()
        self.player.reset()
        self.rainbow_road_music.stop_on_channel(0)
        if did_win:
            # show win screen
            ...
        else:
            # show gameover screen
            if not should_show_main_menu and self.game_over.show() == 1:
                return self.update()
            # (not) temporary solution for a weird bug
            pygame.mouse.set_pos(c.SCREEN_CENTER)

    def show_menu(self, is_pause_menu: bool):
        while True:
            match self.menu.show(is_pause_menu):
                case 1:  # 1=start game
                    if is_pause_menu:
                        c.GAME_PAUSED = False
                        return True
                    else:
                        self.update()
                case 2:  # 2=quit
                    return False
                case 3:  # 3=stats
                    self.stats.show()
                    continue
                case 4:  # 4=credits
                    self.credits.show()
                    continue

    def print_config(self):
        """
        Prints game configuration details.
        This includes the world, racetrack, and player configurations.
        :return: None
        """
        self.world.print_config()
        self.race_track.print_config()
        self.player.print_config()

    def pause(self):
        self.rainbow_road_music.pause()
        self.score_manager.pause()

    def resume(self):
        self.rainbow_road_music.unpause()
        self.score_manager.resume()
