import pygame

import config
from world import World


class Player(World):
    def __init__(self, config, name, description, position):
        super().__init__(config, name, description, position)

        # sprites
        self.num_sprites = 0

    def prepare(self, frame=0):
        sprite_path = self.config.PLAYER_SPRITE
        game_image = pygame.image.load(sprite_path).convert_alpha()

        sprite_width = self.config.PLAYER_SPRITE_WIDTH
        sprite_height = self.config.PLAYER_SPRITE_HEIGHT

        num_sprites = game_image.get_width() // sprite_width
        self.num_sprites = num_sprites

        # List to store all sprites
        sprites = []
        for i in range(num_sprites):
            sprite_x = i * sprite_width
            sprite = game_image.subsurface(pygame.Rect((sprite_x, 0, sprite_width, sprite_height)))
            sprite = pygame.transform.scale(sprite, (
                sprite_width * config.PLAYER_SPRITE_SCALE, sprite_height * config.PLAYER_SPRITE_SCALE))
            sprites.append(sprite)

        # print("Player prepared")
        return sprites[frame]

    def move(self, screen, dt):
        # Initialize player speed and acceleration
        player_speed = 0
        player_acceleration = 800  # Adjust this acceleration parameter for more gradual movement

        # Get the state of all keyboard buttons
        keys = pygame.key.get_pressed()

        player_pos = pygame.Vector2(config.SCREEN_CENTER_X, config.SCREEN_CENTER_Y)

        frame_idle = (self.num_sprites // 2)
        config.PLAYER_CURRENT_FRAME = frame_idle

        frame_delta = 1 if keys[pygame.K_a] or keys[pygame.K_d] else 0

        # Adjust player position based on key presses and adjust frame accordingly
        if keys[pygame.K_w]:
            player_speed = player_acceleration * dt
            player_pos.y -= player_speed
            config.PLAYER_CURRENT_FRAME = 0
        if keys[pygame.K_s]:
            player_speed = player_acceleration * dt
            player_pos.y += player_speed
            config.PLAYER_CURRENT_FRAME = 10
        if keys[pygame.K_a]:
            player_speed = player_acceleration * dt
            player_pos.x -= player_speed
            config.PLAYER_CURRENT_FRAME = min(config.PLAYER_CURRENT_FRAME + frame_delta, self.num_sprites - 4)
        if keys[pygame.K_d]:
            player_speed = player_acceleration * dt
            player_pos.x += player_speed
            config.PLAYER_CURRENT_FRAME = min(config.PLAYER_CURRENT_FRAME + frame_delta, self.num_sprites - 4)

        # Set idle frame if no movement keys are pressed
        if not any([keys[pygame.K_w], keys[pygame.K_s], keys[pygame.K_a], keys[pygame.K_d]]):
            config.PLAYER_CURRENT_FRAME = frame_idle

        # Update player position in the config
        config.PLAYER_CURRENT_POSITION[0] = player_pos.x
        config.PLAYER_CURRENT_POSITION[1] = player_pos.y

        # Draw character at new position and update the display
        screen.blit(self.prepare(config.PLAYER_CURRENT_FRAME), config.PLAYER_CURRENT_POSITION)
        pygame.display.flip()

    def check_flip(self, player, flip=(False, False)):
        if config.PLAYER_SPRITE_HORIZONTAL_FLIP or config.PLAYER_SPRITE_VERTICAL_FLIP:
            player = pygame.transform.flip(surface=player, flip_x=config.PLAYER_SPRITE_HORIZONTAL_FLIP,
                                           flip_y=config.PLAYER_SPRITE_VERTICAL_FLIP)  # Flip the image horizontally, not vertically
        return player

    def print_config(self):
        if self.config is None:
            print("Config is None")
            return False
        else:
            for var_name in dir(self.config):
                if var_name.isupper():  # checking if it's constant (by convention constants are upper-case)
                    if var_name.startswith("PLAYER_"):
                        print(f"{var_name}: {getattr(self.config, var_name)}")
