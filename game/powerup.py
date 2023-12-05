import pygame
import random

from game import sprites, config


class Powerup(pygame.sprite.Sprite):
    def __init__(self, id, screen_width, screen_height):
        super().__init__()

        # Keep track of the amount of powerups
        self.amount_powerups = id

        # self.image = pygame.Surface((30, 30))
        # self.image.fill((0, 0, 255))  # Blue color, you can change this to an image

        # Load the sprite
        self.image = pygame.image.load("assets/sprites/powerup_box.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))

        # Get the rectangle of the sprite
        self.rect = self.image.get_rect()

        # Set the position of the sprite
        self.rect.x = (config.SCREEN_WIDTH - self.rect.width - 880) - (self.amount_powerups * self.rect.width) - 10
        self.rect.y = (config.SCREEN_HEIGHT - self.rect.height - 650) - (self.amount_powerups * self.rect.width) - 10

    def update(self):
        # You can add any animation or movement logic here
        pass
