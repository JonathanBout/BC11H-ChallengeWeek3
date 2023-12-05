import pygame
import random


class Powerup(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()

        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))  # Red color, you can change this to an image
        self.rect = self.image.get_rect()

        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(0, screen_height - self.rect.height)

    def update(self):
        # You can add any animation or movement logic here
        pass
