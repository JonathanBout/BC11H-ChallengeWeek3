import pygame

import game.config as c
from game.camera import Camera
from game.display import Display
from game.game_over import GameOver
from game.game_won import GameWon
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
        # Initialize pygame
        pygame.init()

        # Initialize screen and clock
        self.display = Display()
        self.display.set_display_size()

        # Initialize frame_update_interval using config variable
        self.frame_update_interval = c.PLAYER_FRAME_UPDATE_INTERVAL

        # Set up font for text rendering - TODO: use text.py instead
        self.stats_menu_font = pygame.font.Font("assets/fonts/SuperMario256.ttf", 40)
        self.credits_font = self.stats_menu_font
        self.game_over_font = self.stats_menu_font
        self.game_won_font = self.stats_menu_font

        # Setup menu and stats
        self.menu = Menu()
        self.stats = Stats(self.stats_menu_font)
        self.credits = Credits(self.credits_font)
        self.game_over = GameOver(self.game_over_font)
        self.game_won = GameWon(self.game_won_font)
        self.score_manager = ScoreManager()

        # Initialize game objects
        self.world = World(c, c.WORLD_NAME, c.WORLD_DESCRIPTION, c.WORLD_POSITION)
        self.race_track = Map(c, c.MAP_NAME, c.MAP_DESCRIPTION, c.MAP_POSITION)
        self.player = Player(c, c.PLAYER_NAME, c.PLAYER_DESCRIPTION, c.PLAYER_POSITION)
        self.camera = Camera()

        # Player properties
        self.player.prepare(c.PLAYER_CURRENT_FRAME)

        # Music
        self.rainbow_road_music = Music(c.MUSIC_RAINBOW_ROAD, 0)

    # Actions to perform when the game starts
    def start(self):
        """
        Starts the game and displays the menu options.
        :return: None
        """
        # Show the menu over and over again
        self.show_menu(False)

    # Actions to perform when the game updates
    def update(self):
        """
        This method updates the game state and display.
        This is needed to run and play the game.
        :return: None
        """
        # Start the score manager
        self.score_manager.start()

        # Setup game variables
        run_game, did_win, should_show_main_menu = self.init_game()

        # Play the music
        self.rainbow_road_music.set_volume(0.1)
        self.rainbow_road_music.play(-1)
        self.player.reset()
        self.camera.reset()
        # Main game loop
        while run_game:
            # Set the current window caption
            pygame.display.set_caption(f"{c.WORLD_NAME} - {c.CURRENT_FPS:.2f}")

            # Check for events and only get the events we want
            for event in pygame.event.get(
                (
                    pygame.KEYDOWN,
                    c.GAME_PAUSE_CHANGED,
                    c.PLAYER_GAMEOVER_EVENT,
                    c.PLAYER_WON_EVENT,
                    pygame.QUIT,
                )
            ):
                # If player presses a button
                if event.type == pygame.KEYDOWN:
                    # And if the button is escape
                    if event.key == pygame.K_ESCAPE:
                        # Pause the game
                        c.GAME_PAUSED = True
                        self.pause()
                        # And show the menu
                        if not self.show_menu(True):
                            run_game = False
                            should_show_main_menu = True
                            break
                        # And if the menu is closed, resume the game
                        self.resume()
                        c.GAME_PAUSED = False
                # If the pause state is changed
                elif event.type == c.GAME_PAUSE_CHANGED:
                    # And it is now paused
                    if c.GAME_PAUSED:
                        # Pause the game
                        self.pause()
                    else:
                        # Otherwise, resume the game
                        self.resume()
                # If the player died
                elif event.type == c.PLAYER_GAMEOVER_EVENT:
                    # Reset the camera and player
                    self.camera.reset()
                    self.player.reset()
                    # Stop the game and set the win state to false
                    run_game = False
                    did_win = False
                    break
                # If the player won
                elif event.type == c.PLAYER_WON_EVENT:
                    # Reset the camera and player
                    self.camera.reset()
                    self.player.reset()
                    # Stop the game and set the win state to true
                    run_game = False
                    did_win = True
                    break
                elif event.type == pygame.QUIT:
                    exit()

            # Check if the player died or won
            if not run_game:
                break

            print(c.RACE_CURRENT_LAP)

            # Move player 1
            self.player.move(self.display.screen, self.camera)

            # Refresh the display and frame rate
            self.display.draw()

            # Check for events related to the player, such as collisions with the respawn area
            self.player.check_for_events(self.display.screen)

        # Set game state to game over, regardless of whether the player won or lost
        self.game_over_state(did_win, should_show_main_menu)

    # Show the main menu
    def show_menu(self, is_pause_menu: bool):
        # Show the menu
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

    # Print the world, map and player configuration for debugging purposes
    def print_config(self):
        """
        Prints game configuration details.
        This includes the world, racetrack, and player configurations.
        :return: None
        """
        self.world.print_config()
        self.race_track.print_config()
        self.player.print_config()

    # Initialize game variables
    def init_game(self):
        """
        Initializes the game by setting up the necessary variables and objects.
        :return: A tuple containing the following values:
            - run_game (bool): Indicates whether the game should continue running.
            - did_win (bool): Indicates whether the player won the game.
            - should_show_main_menu (bool): Indicates whether the main menu should be displayed.
        """
        run_game = True
        did_win = False
        should_show_main_menu = False
        return run_game, did_win, should_show_main_menu

    def game_over_state(self, did_win, should_show_main_menu):
        # If the game is over, reset the camera and player and stop the music.
        self.camera.reset()
        self.player.reset()
        self.rainbow_road_music.stop_on_channel(0)

        # If the player won, show the win screen, otherwise show the game over screen.
        if did_win:
            # Show win screen
            if self.game_won.show(self.score_manager, self.stats) == 1:
                return self.update()
        else:
            # Show gameover screen
            if not should_show_main_menu and self.game_over.show() == 1:
                return self.update()

        # (Not so) temporary solution for a weird bug
        pygame.mouse.set_pos(c.SCREEN_CENTER)

    # Pause the music and score manager if the game is paused
    def pause(self):
        """
        Pauses the game by pausing the music and score manager.
        :return: None
        """
        self.rainbow_road_music.pause()
        self.score_manager.pause()

    # Resume the music and score manager if the game is resumed
    def resume(self):
        """
        Resumes the game by unpausing the music and resuming the score manager.
        :return: None
        """
        self.rainbow_road_music.unpause()
        self.score_manager.resume()
