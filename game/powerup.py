import pygame
import random

from game import config


class Powerup(pygame.sprite.Sprite):
    def __init__(self, id):
        super().__init__()

        # Keep track of the amount of powerups
        self.amount_powerups = id
        self.powerups = None
        self.powerup_respawn_list = []

        # Keep track of the powerup time
        self.POWERUP_RESPAWN_TIME = 5000  # When the powerup respawns
        self.powerup_respawn_time = None  # How long the powerup has been gone
        self.current_time = None  # The current time

        # Load the sprite
        self.image = pygame.image.load("assets/sprites/powerup_box.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))

        # Get the rectangle of the sprite
        self.rect = self.image.get_rect()

        # Set the position of the sprite
        if self.amount_powerups > -1:
            self.rect.x = (config.SCREEN_WIDTH - self.rect.width - 880) - (self.amount_powerups * self.rect.width) - 10
            self.rect.y = (config.SCREEN_HEIGHT - self.rect.height - 650) - (
                    self.amount_powerups * self.rect.width) - 10

    def update(self, player_rect, powerups):
        self.powerups = powerups
        self.current_time = pygame.time.get_ticks()
        print(self.powerup_respawn_time)

        for powerup in self.powerups:
            if player_rect.colliderect(powerup):
                self.powerup_respawn_time = self.current_time
                self.remove_powerup(powerup)

            if self.powerup_respawn_time is not None:
                if self.current_time - self.powerup_respawn_time > self.POWERUP_RESPAWN_TIME:
                    self.powerup_respawn_time = None
                    self.respawn_powerup(powerup)
        print(self.current_time, self.powerup_respawn_time)

    def respawn_powerup(self, powerup):
        self.powerup_respawn_list.remove(powerup)
        self.powerups.add(powerup)

    def remove_powerup(self, powerup):
        self.powerups.remove(powerup)
        self.powerup_respawn_list.append(powerup)
