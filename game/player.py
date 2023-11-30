import math

import pygame

import game.config as c
from util.eventHandler import EventManager, RespawnEvent
from util.text import TextRenderer
from game.world import World
from game.display import Display


class Player(World):
    def __init__(self, config, name, description, position):
        """
        Initialize the Player class object.
        :param config: The game configuration object.
        :param name: The name of the player.
        :param description: The description of the player.
        :param position: The starting position of the player.
        """
        super().__init__(config, name, description, position)

        # Initialize display
        self.display = Display()

        # sprites
        self.num_sprites = 0

    def prepare(self, frame=0):
        """
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
        sprite_path = c.PLAYER_SPRITE
        game_image = pygame.image.load(sprite_path).convert_alpha()

        sprite_width = c.PLAYER_SPRITE_WIDTH
        sprite_height = c.PLAYER_SPRITE_HEIGHT

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
                    sprite_width * c.PLAYER_SPRITE_SCALE,
                    sprite_height * c.PLAYER_SPRITE_SCALE,
                ),
            )
            sprites.append(sprite)

        # print("Player prepared")
        return sprites[frame]

    def move(self, screen):
        """
        :param screen: the screen object on which to draw the player character
        :return: None

        This method handles the movement of the player character based on keyboard inputs. It updates the player's
        position and frame, and draws the character on the screen.
        If no keys are pressed, the player character stays idle.

        Example usage:
        player = Player()
        player.move(screen)
        """
        # We can't divide by zero, so we check if the current fps is zero.
        if c.CURRENT_FPS == 0:
            print("CURRENT_FPS value is Zero! Please, check the value.")
        else:
            self.display.dt = 1.0 / c.CURRENT_FPS

        # Initialize player speed, acceleration and friction
        player_speed = c.PLAYER_CURRENT_SPEED
        player_acceleration = c.PLAYER_MAX_SPEED
        player_friction = c.PLAYER_FRICTION

        # Get the state of all keyboard buttons
        keys = pygame.key.get_pressed()

        # Get the current player position
        player_rect = pygame.Rect(
            c.PLAYER_CURRENT_POSITION, (c.PLAYER_SPRITE_WIDTH, c.PLAYER_SPRITE_HEIGHT)
        )

        # Set the frame to idle
        frame_idle = self.num_sprites // 2
        c.PLAYER_CURRENT_FRAME = frame_idle

        # Set the frame delta based on whether the player is moving horizontally
        frame_delta = 1 if keys[pygame.K_a] or keys[pygame.K_d] else 0

        # Get the initial player speed
        initial_player_speed = player_speed

        # Adjust player speed based on acceleration and friction
        if c.PLAYER_CURRENT_SPEED <= c.PLAYER_MAX_SPEED:
            player_speed = (
                initial_player_speed + player_acceleration * self.display.dt
            ) * player_friction

        # Adjust player position based on key presses and adjust frame accordingly
        if keys[pygame.K_w]:
            player_rect.y -= int(player_speed)
            c.PLAYER_CURRENT_FRAME = 0
        if keys[pygame.K_s]:
            player_rect.y += int(player_speed)
            c.PLAYER_CURRENT_FRAME = 10
        if keys[pygame.K_a]:
            player_rect.x -= int(player_speed)
            c.PLAYER_CURRENT_FRAME = min(
                c.PLAYER_CURRENT_FRAME + frame_delta, self.num_sprites - 4
            )
        if keys[pygame.K_d]:
            player_rect.x += int(player_speed)
            c.PLAYER_CURRENT_FRAME = min(
                c.PLAYER_CURRENT_FRAME + frame_delta, self.num_sprites - 4
            )

        # Boost player speed if shift is pressed
        store_speed = player_speed
        if keys[pygame.K_LSHIFT]:
            player_speed = player_speed * 2.5
        else:
            player_speed = store_speed

        # Adjust player speed if moving diagonally
        if (keys[pygame.K_w] or keys[pygame.K_s]) and (
            keys[pygame.K_a] or keys[pygame.K_d]
        ):
            player_speed = player_speed / math.sqrt(2)

        # If no keys are pressed, set the frame to idle.
        if not any(
            [keys[pygame.K_w], keys[pygame.K_s], keys[pygame.K_a], keys[pygame.K_d]]
        ):
            player_speed = 0
            c.PLAYER_CURRENT_FRAME = frame_idle

        # Save the (new) current player speed to the config
        c.PLAYER_CURRENT_SPEED = round(player_speed, 0)

        print(f"Player speed: {c.PLAYER_CURRENT_SPEED}")

        # Define the screen dimensions as a rect object
        screen_rect = pygame.Rect(
            0,
            0,
            c.SCREEN_WIDTH - c.PLAYER_SPRITE_WIDTH,
            c.SCREEN_HEIGHT - c.PLAYER_SPRITE_HEIGHT,
        )

        # Move the screen if the player is close to the edge
        if player_rect.bottom + c.SCREEN_MOVE_OFFSET >= screen_rect.bottom:
            c.MAP_POSITION[1] -= player_speed
            player_rect.top -= player_speed
        elif player_rect.top - c.SCREEN_MOVE_OFFSET <= screen_rect.top:
            c.MAP_POSITION[1] += player_speed
            player_rect.top += player_speed

        if player_rect.right + c.SCREEN_MOVE_OFFSET >= screen_rect.right:
            c.MAP_POSITION[0] -= player_speed
            player_rect.left -= player_speed
        elif player_rect.left - c.SCREEN_MOVE_OFFSET <= screen_rect.left:
            c.MAP_POSITION[0] += player_speed
            player_rect.right += player_speed

        # Update player position in the config to the possibly clamped player_rect
        c.PLAYER_CURRENT_POSITION[0], c.PLAYER_CURRENT_POSITION[1] = player_rect.topleft

        # Draw character at new position and update the display
        screen.blit(self.prepare(c.PLAYER_CURRENT_FRAME), c.PLAYER_CURRENT_POSITION)
        pygame.display.flip()

    def check_for_events(self, screen):
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
            c.PLAYER_CURRENT_POSITION,
            TextRenderer(None, 32),
            c.RESPAWN_SOUND,
            (c.SCREEN_CENTER_X, c.SCREEN_CENTER_Y),
        )

        # Register the respawn event with the event manager
        event_manager.register_event(respawn_event)

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
        if c.PLAYER_SPRITE_HORIZONTAL_FLIP or c.PLAYER_SPRITE_VERTICAL_FLIP:
            player = pygame.transform.flip(
                surface=player,
                flip_x=c.PLAYER_SPRITE_HORIZONTAL_FLIP,
                flip_y=c.PLAYER_SPRITE_VERTICAL_FLIP,
            )
        return player

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
                ):  # checking if it's constant (by convention constants are upper-case)
                    if var_name.startswith("PLAYER_"):
                        print(f"{var_name}: {getattr(self.config, var_name)}")
