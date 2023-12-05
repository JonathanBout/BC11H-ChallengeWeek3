import pygame
import random

from game import config


class Powerup(pygame.sprite.Sprite):
    def __init__(self, id):
        super().__init__()

        # Keep track of the amount of powerups
        self.amount_powerups = id  # Give each powerup a unique id
        self.powerups = None  # Which powerups are on the map
        self.powerup_respawn_list = []  # Which powerups should be respawned
        self.picked_up_item = None  # Powerup blocks the player has picked up

        # Keep track of the powerup time
        self.POWERUP_RESPAWN_TIME = 5000  # When the powerup respawns
        self.powerup_respawn_time = None  # How long the powerup has been gone
        self.current_time = None  # The current time

        # Load the sprite
        self.image = pygame.image.load("assets/sprites/powerup_box.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))

        # Get the rectangle of the sprite
        self.rect = self.image.get_rect()

        # Properties of a powerup
        self.effects = ["Boost", "Slow"]

        # Set the position of the sprite
        if self.amount_powerups > -1:
            self.rect.x = (config.SCREEN_WIDTH - self.rect.width - 880) - (self.amount_powerups * self.rect.width) - 10
            self.rect.y = (config.SCREEN_HEIGHT - self.rect.height - 650) - (
                    self.amount_powerups * self.rect.width) - 10

    def update(self, player_rect, powerups):
        """
        :return: picked_up_item
        :rtype: list
        """
        self.powerups = powerups  # Get the list of generated powerups
        self.current_time = pygame.time.get_ticks()  # Get the current time
        self.picked_up_item = []  # List of picked up powerups

        # Check each powerup
        for powerup in self.powerups:
            # For if the player collides with the powerup
            if player_rect.colliderect(powerup):
                self.powerup_respawn_time = self.current_time  # Set the respawn time
                self.remove_powerup(powerup)  # Remove the powerup from map
                self.picked_up_item.append(random.choice(self.effects))  # Add a random effect to the list
                print("Picked up powerup")

        print(self.current_time, self.powerup_respawn_time)

        if self.powerup_respawn_time is not None:
            print("YES!", self.powerup_respawn_time)
        print(self.picked_up_item)
        return self.picked_up_item

    def respawn_powerup(self, powerup):
        self.powerup_respawn_list.remove(powerup)
        self.powerups.add(powerup)

    def remove_powerup(self, powerup):
        self.powerups.remove(powerup)
        self.powerup_respawn_list.append(powerup)
