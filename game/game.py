import pygame

from game import config, helper
from game.camera import Camera
from game.display import Display
from game.enemy import Enemy
from game.game_over import GameOver
from game.game_won import GameWon
from game.map_chooser import MapChooser
from game.map_manager import MapConfig, MapManager
from game.menu import Menu
from game.powerup import Powerup
from game.score_manager import ScoreManager
from game.stats import Stats
from game.player import Player1, Player2
from game.credits import Credits
from util.music import Music
from util import rect_from_image

import importlib


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
        self.joystick_count = pygame.joystick.get_count()
        self.joystick_keys = [False, False, False, False, False]
        if self.joystick_count > 0:
            self.joystick = pygame.joystick.Joystick(0)
        # Initialize screen and clock
        self.display = Display()
        self.display.set_display_size()

        # Set up font for text rendering - TODO: use text.py instead
        self.stats_menu_font = pygame.font.Font("assets/fonts/SuperMario256.ttf", 40)
        self.credits_font = self.stats_menu_font
        self.game_over_font = self.stats_menu_font
        self.game_won_font = self.stats_menu_font
        self.map_chooser_font = self.stats_menu_font

        # Setup menu and stats
        self.menu = Menu()
        self.stats = Stats(self.stats_menu_font)
        self.credits = Credits(self.credits_font)
        self.game_over = GameOver(self.game_over_font)
        self.game_won = GameWon(self.game_won_font)
        self.score_manager = ScoreManager()
        self.map_manager = MapManager()
        self.map_chooser = MapChooser(self.map_chooser_font, self.map_manager)

        # Player objects and properties
        self.camera = Camera()
        self.keys = None

        # Music
        self.music: Music = None

        # Map rects
        self.powerup_group = pygame.sprite.Group()
        self.create_powerups(3)

    def init_players(self):
        # Player 1
        self.player1 = Player1(
            config,
            config.PLAYER_1_NAME,
            config.PLAYER_1_DESCRIPTION,
            config.PLAYER_1_POSITION,
            config.PLAYER_1_SPRITE,
        )

        # Player 2
        self.player2 = Player2(
            config,
            config.PLAYER_2_NAME,
            config.PLAYER_2_DESCRIPTION,
            config.PLAYER_2_POSITION,
            config.PLAYER_2_SPRITE,
        )

        # Prepare the player sprites
        self.player_one = self.player1.prepare(config.PLAYER_1_CURRENT_FRAME)
        self.player_two = self.player2.prepare(config.PLAYER_2_CURRENT_FRAME)

        # Print player configuration
        self.player1.print_config()
        self.player2.print_config()

    # Actions to perform when the game starts
    def start(self):
        """
        Starts the game and displays the menu options.
        :return: None
        """
        # Show the menu over and over again
        self.show_menu(False)

    # Actions to perform when the game updates
    def update(self, map: MapConfig):
        """
        This method updates the game state and display.
        This is needed to run and play the game.
        :return: None
        """
        # Start the score manager
        self.score_manager.start()
        self.load_map_rects(map)

        # Setup game variables
        run_game, did_win, should_show_main_menu = self.init_game()
        self.init_players()

        # Play the music
        self.music = Music(map.music_file, 0)
        self.enemy = Enemy(map, config.PLAYER_2_SPRITE, self.display.screen)
        self.music.set_volume(1)
        self.music.play(-1)

        # Reset the camera and player
        self.player1.reset()
        self.player2.reset()
        self.camera.reset()

        # Main game loop
        while run_game:
            self.powerup_group.draw(self.display.screen)

            map_relative_position = (
                -config.MAP_POSITION[0] + config.PLAYER_1_CURRENT_POSITION[0],
                -config.MAP_POSITION[1] + config.PLAYER_1_CURRENT_POSITION[1],
            )

            # Set the current window caption
            pygame.display.set_caption(
                f"{map.name} - {map_relative_position} - {config.CURRENT_FPS}"
            )

            # Check for events and only get the events we want
            for event in pygame.event.get(
                    (
                            pygame.KEYDOWN,
                            config.GAME_PAUSE_CHANGED,
                            config.PLAYER_GAMEOVER_EVENT,
                            config.PLAYER_WON_EVENT,
                            pygame.QUIT,
                            pygame.JOYAXISMOTION,
                    )
            ):
                # If player presses a button
                if event.type == pygame.KEYDOWN:
                    # And if the button is escape
                    if event.key == pygame.K_ESCAPE:
                        # Pause the game
                        config.GAME_PAUSED = True
                        self.pause()
                        # And show the menu
                        if not self.show_menu(True):
                            run_game = False
                            should_show_main_menu = True
                            break
                        # And if the menu is closed, resume the game
                        self.resume()
                        config.GAME_PAUSED = False
                elif event.type == pygame.JOYAXISMOTION:
                    if self.joystick.get_axis(0) >= 0.5:
                        print("Right")
                        self.joystick_keys[0] = True
                    elif self.joystick.get_axis(0) <= -0.5:
                        print("Left")
                        self.joystick_keys[1] = True
                    elif self.joystick.get_axis(1) >= 0.5:
                        print("Down")
                        self.joystick_keys[2] = True
                    elif self.joystick.get_axis(1) <= -0.5:
                        print("Up")
                        self.joystick_keys[3] = True
                    elif self.joystick.get_axis(5) >= 0.5:
                        print("Right Trigger")
                        self.joystick_keys[4] = True
                    else:
                        self.joystick_keys = [False, False, False, False, False]

                # If the pause state is changed
                elif event.type == config.GAME_PAUSE_CHANGED:
                    # And it is now paused
                    if config.GAME_PAUSED:
                        # Pause the game
                        self.pause()
                    else:
                        # Otherwise, resume the game
                        self.resume()
                # If the player died
                elif event.type == config.PLAYER_GAMEOVER_EVENT:
                    # Reset the camera and player
                    self.camera.reset()
                    self.player1.reset()
                    self.player2.reset()
                    # Stop the game and set the win state to false
                    run_game = False
                    did_win = False
                    break
                # If the player won
                elif event.type == config.PLAYER_WON_EVENT:
                    # Reset the camera and player
                    self.camera.reset()
                    self.player1.reset()
                    self.player2.reset()
                    # Stop the game and set the win state to true
                    run_game = False
                    did_win = True
                    break
                elif event.type == pygame.QUIT:
                    exit()

            # Check if the player died or won
            if not run_game:
                break

            # print("current lap:", config.RACE_CURRENT_LAP)

            # Update key states
            self.keys = pygame.key.get_pressed()

            # Position the collision map correctly
            map_rects = [
                pygame.Rect(
                    rect.left + config.MAP_POSITION[0],
                    rect.top + config.MAP_POSITION[1],
                    *rect.size,
                )
                for rect in self.map_rects
            ]

            [
                pygame.draw.circle(
                    self.display.screen,
                    "red",
                    (x[0] + config.MAP_POSITION[0], x[1] + config.MAP_POSITION[1]),
                    50,
                    50,
                )
                for x in map.waypoints
            ]

            self.enemy.update()

            # Move player 1
            if self.joystick_count == 0:
                self.player1.move(
                    screen=self.display.screen,
                    camera=self.camera,
                    controls=self.keys,
                    current_position=config.PLAYER_1_CURRENT_POSITION,
                    powerup_list=self.powerup_group,
                )
            else:
                self.player1.move(
                    screen=self.display.screen,
                    camera=self.camera,
                    controls=self.joystick_keys,
                    current_position=config.PLAYER_1_CURRENT_POSITION,
                    powerup_list=self.powerup_group,
                )

            # Refresh the display and frame rate
            self.display.draw(map)

            # Check for events related to the player, such as collisions with the respawn area
            self.player1.check_for_events(
                self.display.screen, map_rects, config.PLAYER_1_CURRENT_POSITION
            )
            # self.player2.check_for_events(
            #     self.display.screen, map_rects, config.PLAYER_2_CURRENT_POSITION
            # )

        # Set game state to game over, regardless of whether the player won or lost
        self.game_over_state(did_win, should_show_main_menu, map)

    # Show the main menu
    def show_menu(self, is_pause_menu: bool):
        # Show the menu
        while True:
            match self.menu.show(is_pause_menu):
                case 1:  # 1=start game
                    if is_pause_menu:
                        config.GAME_PAUSED = False
                        return True
                    else:
                        self.show_map_choice_menu()
                case 2:  # 2=quit
                    return False
                case 3:  # 3=stats
                    self.stats.show()
                    continue
                case 4:  # 4=credits
                    self.credits.show()
                    continue

    def show_map_choice_menu(self):
        helper.wait_for_mouse_up()  # wait for mouse up to prevent multiple button clicks
        if map := self.map_chooser.show():
            self.update(map)

    # Initialize game variables
    def init_game(self):
        """
        Initializes the game by setting up the necessary variables and objects.
        :return: A tuple containing the following values:
            - run_game (bool): Indicates whether the game should continue running.
            - did_win (bool): Indicates whether the player won the game.
            - should_show_main_menu (bool): Indicates whether the main menu should be displayed.
        """
        global config

        config = importlib.reload(config)

        run_game = True
        did_win = False
        should_show_main_menu = False
        return run_game, did_win, should_show_main_menu

    def game_over_state(self, did_win: bool, should_show_main_menu: bool, map: MapConfig):
        # If the game is over, reset the camera and player and stop the music.
        self.camera.reset()
        self.player1.reset()
        self.music.stop_on_channel(0)
        self.powerup_group.empty()
        self.create_powerups(3)

        # If the player won, show the win screen, otherwise show the game over screen.
        if did_win:
            self.score_manager.pause()
            score = self.score_manager.get_score()
            self.stats.add_stat(score, map.name)
            # Show win screen
            if self.game_won.show() == 1:
                return self.show_map_choice_menu()
        else:
            # Show gameover screen
            if not should_show_main_menu and self.game_over.show() == 1:
                return self.show_map_choice_menu()

    # Pause the music and score manager if the game is paused
    def pause(self):
        """
        Pauses the game by pausing the music and score manager.
        :return: None
        """
        self.music.pause()
        self.score_manager.pause()

    # Resume the music and score manager if the game is resumed
    def resume(self):
        """
        Resumes the game by unpausing the music and resuming the score manager.
        :return: None
        """
        self.music.unpause()
        self.score_manager.resume()

    def load_map_rects(self, map: MapConfig):
        self.map_rects = rect_from_image.load_rect(
            map.background_image, map.collider_scale
        )

    def create_powerups(self, num_powerups):
        for _ in range(num_powerups):
            powerup = Powerup(_)
            self.powerup_group.add(powerup)
