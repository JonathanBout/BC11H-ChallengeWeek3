import math
import pygame
from pygame.surface import Surface
from game.camera import Camera
from game import config
from util.eventHandler import EventManager, RespawnEvent, FinishEvent
from game.world import World
from game.display import Display


class Player(World):
    def __init__(self, config: config, name, description, position, player_sprite):
        """
        Initialize the Player class object.
        :param config: The game configuration object.
        :param name: The name of the player.
        :param description: The description of the player.
        :param position: The starting position of the player.
        :param player_sprite: The sprite of the player.
        """
        super().__init__(config, name, description, position)

        # Initialize display
        self.display = Display()

        # sprites
        self.player_sprite = player_sprite
        self.num_sprites = 0
        self.finish_event = FinishEvent(None, config.PLAYER_1_POSITION, config.FINISH_SOUND)

    def prepare(self, frame=0):
        """
        :param player: an integer representing the player number
        :param frame: an integer representing the index of the desired sprite frame
        :return: the sprite image at the specified frame index
        This method prepares the player character sprite by loading the sprite image file
        and extracting individual frames. It returns the sprite image at the specified frame index.
        Example usage:
            player = Player()
            frame = 0
            sprite = player.prepare(frame)
        Note: This method does not handle error checking for invalid frame indices.
        """
        # Load the sprite image
        game_image = pygame.image.load(self.player_sprite).convert_alpha()

        # Set the sprite width and height
        sprite_width = config.PLAYER_SPRITE_WIDTH
        sprite_height = config.PLAYER_SPRITE_HEIGHT

        # Calculate the number of sprites in the sprite image
        num_sprites = game_image.get_width() // sprite_width
        self.num_sprites = num_sprites

        # List to store all sprites
        sprites = []
        for i in range(num_sprites):
            sprite_x = i * sprite_width
            sprite = game_image.subsurface(
                pygame.Rect((sprite_x, 0, sprite_width, sprite_height))
            )
            sprite = pygame.transform.scale(
                sprite,
                (
                    sprite_width * config.PLAYER_SPRITE_SCALE,
                    sprite_height * config.PLAYER_SPRITE_SCALE,
                ),
            )
            sprites.append(sprite)

        # Return the sprite at the specified frame index
        return sprites[frame]

    def move(self, screen: Surface, camera: Camera, controls: list):
        """
        :param screen: the screen object on which to draw the player character
        :param camera: the camera object to use for movement
        :param controls: a list containing the controls for the player character
        :return: None

        This method handles the movement of the player character based on keyboard inputs. It updates the player's
        position and frame, and draws the character on the screen.
        If no keys are pressed, the player character stays idle.

        Example usage:
        player = Player()
        player.move(screen)
        """
        # We can't divide by zero, so we check if the current fps is zero.
        if config.CURRENT_FPS == 0:
            print("CURRENT_FPS value is Zero! Please, check the value.")
        else:
            self.display.dt = 1.0 / config.CURRENT_FPS

        # Initialize player speed, acceleration and friction
        player_speed = config.PLAYER_CURRENT_SPEED
        player_acceleration = config.PLAYER_MAX_SPEED
        player_friction = config.PLAYER_FRICTION

        # Get the state of all keyboard buttons
        # keys = pygame.key.get_pressed()
        key = dict()
        key["w"] = controls[0]
        key["s"] = controls[1]
        key["a"] = controls[2]
        key["d"] = controls[3]
        key["shift"] = controls[4]

        # Get the current player position
        player_rect = pygame.Rect(
            config.PLAYER_CURRENT_POSITION,
            (config.PLAYER_SPRITE_WIDTH, config.PLAYER_SPRITE_HEIGHT),
        )

        # Set the frame to idle
        frame_idle = self.num_sprites // 2
        config.PLAYER_CURRENT_FRAME = frame_idle

        # Set the frame delta based on whether the player is moving horizontally
        frame_delta = 1 if key["a"] or key["d"] else 0

        # Get the initial player speed
        initial_player_speed = player_speed

        # Adjust player speed based on acceleration and friction
        if config.PLAYER_CURRENT_SPEED <= config.PLAYER_MAX_SPEED:
            player_speed = (
                initial_player_speed + player_acceleration * self.display.dt
            ) * player_friction

        # Adjust player position based on key presses and adjust frame accordingly
        if key["w"]:
            player_rect.y -= int(player_speed)
            config.PLAYER_CURRENT_FRAME = 0
        if key["s"]:
            player_rect.y += int(player_speed)
            config.PLAYER_CURRENT_FRAME = 10
        if key["a"]:
            player_rect.x -= int(player_speed)
            config.PLAYER_CURRENT_FRAME = min(
                config.PLAYER_CURRENT_FRAME + frame_delta, self.num_sprites - 4
            )
        if key["d"]:
            player_rect.x += int(player_speed)
            config.PLAYER_CURRENT_FRAME = min(
                config.PLAYER_CURRENT_FRAME + frame_delta, self.num_sprites - 4
            )

        # Boost player speed if shift is pressed
        store_speed = player_speed
        if key["shift"]:
            player_speed = player_speed * 2.5
        else:
            player_speed = store_speed

        # Adjust player speed if moving diagonally
        if (key["w"] or key["s"]) and (key["a"] or key["d"]):
            player_speed = player_speed / math.sqrt(2)

        # If no keys are pressed, set the frame to idle.
        any_keys = [key["w"], key["s"], key["a"], key["d"]]

        if not any(any_keys):
            player_speed = 0
            config.PLAYER_CURRENT_FRAME = frame_idle

        # Save the (new) current player speed to the config
        config.PLAYER_CURRENT_SPEED = round(player_speed, 0)

        # Define the screen dimensions as a rect object
        screen_rect = pygame.Rect(
            0,
            0,
            config.SCREEN_WIDTH - config.PLAYER_SPRITE_WIDTH,
            config.SCREEN_HEIGHT - config.PLAYER_SPRITE_HEIGHT,
        )

        # Clamp the player position to the screen dimensions
        player_rect, screen_rect = camera.do_movement(player_rect, screen_rect)

        # Update player position in the config to the possibly clamped player_rect
        (
            config.PLAYER_CURRENT_POSITION[0],
            config.PLAYER_CURRENT_POSITION[1],
        ) = player_rect.topleft

        # Print player speed and player and map position
        print(f"Player speed: {config.PLAYER_CURRENT_SPEED}")
        print(f"Player position: {player_rect.topleft}")
        print(f"Map position: {config.MAP_POSITION}")

        # Draw character at new position and update the display
        screen.blit(
            self.prepare(config.PLAYER_CURRENT_FRAME), config.PLAYER_CURRENT_POSITION
        )
        pygame.display.flip()

    def check_for_events(self, screen: Surface):
        """
        Check for registered player events.
        :param screen: The pygame screen object.
        :return: None
        """
        # Event manager
        event_manager = EventManager()

        # Create respawn event
        respawn_event = RespawnEvent(
            screen,
            config.PLAYER_CURRENT_POSITION,
            config.RESPAWN_SOUND,
        )

        self.finish_event.player_position = config.PLAYER_CURRENT_POSITION
        self.finish_event.screen = screen
        # Register the events with the event manager
        event_manager.register_event(respawn_event)
        event_manager.register_event(self.finish_event)

        # Trigger the respawn event
        event_manager.trigger_events()

    def check_flip(self, player, flip=(False, False)):
        """
        :param player: The current player sprite.
        :param flip: A tuple representing the flip state. The first element indicates whether the sprite should be
        horizontally flipped, and the second element indicates whether it should be vertically flipped. Defaults to
        (False, False).
        :return: The player sprite with the requested flip applied.
        """
        if config.PLAYER_SPRITE_HORIZONTAL_FLIP or config.PLAYER_SPRITE_VERTICAL_FLIP:
            player = pygame.transform.flip(
                surface=player,
                flip_x=config.PLAYER_SPRITE_HORIZONTAL_FLIP,
                flip_y=config.PLAYER_SPRITE_VERTICAL_FLIP,
            )
        return player

    def reset(self):
        """
        Resets the player's position and speed.
        :param self: The Player object.
        :return: None.
        """
        config.PLAYER_CURRENT_POSITION = config.PLAYER_RESPAWN_POSITION[:]
        config.PLAYER_POSITION = config.PLAYER_CURRENT_POSITION[:]
        config.PLAYER_CURRENT_SPEED = 0
        config.RACE_CURRENT_LAP = 0
        

    def print_config(self):
        """
        Prints the configuration values which could be of importance for the Player object.
        :return: None
        """
        if self.config is None:
            print("Config is None")
            return False
        else:
            for var_name in dir(self.config):
                if (
                    var_name.isupper()
                ):  # Checking if it's constant (by convention constants are upper-case)
                    if var_name.startswith("PLAYER_"):
                        print(f"{var_name}: {getattr(self.config, var_name)}")
