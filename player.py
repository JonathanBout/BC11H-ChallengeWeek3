import pygame

import config
from world import World


class Player(World):
    def __init__(self, config, name, description, position):
        super().__init__(config, name, description, position)

    def prepare(self, frame=0):
        sprite_path = self.config.PLAYER_SPRITE
        game_image = pygame.image.load(sprite_path).convert_alpha()

        sprite_width = self.config.PLAYER_SPRITE_WIDTH
        sprite_height = self.config.PLAYER_SPRITE_HEIGHT

        num_sprites = game_image.get_width() // sprite_width

        # List to store all sprites
        sprites = []
        for i in range(num_sprites):
            sprite_x = i * sprite_width
            sprite = game_image.subsurface(pygame.Rect((sprite_x, 0, sprite_width, sprite_height)))
            sprite = pygame.transform.scale(sprite, (sprite_width * config.PLAYER_SPRITE_SCALE, sprite_height * config.PLAYER_SPRITE_SCALE))
            sprites.append(sprite)

        # print("Player prepared")
        return sprites[frame]

    def move(self, frame=0):
        pass


    def print_config(self):
        if self.config is None:
            print("Config is None")
            return False
        else:
            for var_name in dir(self.config):
                if var_name.isupper():  # checking if it's constant (by convention constants are upper-case)
                    if var_name.startswith("PLAYER_"):
                        print(f"{var_name}: {getattr(self.config, var_name)}")
