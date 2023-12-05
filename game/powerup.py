import pygame
import random

from game import config


class Powerup(pygame.sprite.Sprite):

    def __init__(self, id):
        super().__init__()

        # Keep track of the amount of powerups
        self.POWERUP_RESPAWN_EVENT = pygame.USEREVENT + 1  # Event for when the powerup respawns
        self.amount_powerups = id  # Give each powerup a unique id
        self.powerups = None  # Which powerups are on the map
        self.powerup_respawn_list = []  # Which powerups should be respawned
        self.picked_up_item = []  # Powerup blocks the player has picked up

        # Keep track of the powerup time
        self.POWERUP_RESPAWN_TIME = 5000  # When the powerup respawns
        self.powerup_respawn_time = None  # How long the powerup has been gone
        self.current_time = None  # The current time
        pygame.time.set_timer(self.POWERUP_RESPAWN_EVENT, self.POWERUP_RESPAWN_TIME)

        # Load the sprite
        self.image = pygame.image.load("assets/sprites/powerup_box.png").convert_alpha()  # Load the sprite
        self.image = pygame.transform.scale(self.image, (30, 30))  # Scale the sprite

        # Get the rectangle of the sprite
        self.rect = self.image.get_rect()  # Create a rectangle around the sprite

        # Properties of a powerup
        self.effects = ["Boost", "Slow"]  # The possible effects of a powerup

        # Set the X and Y position of the sprite
        if self.amount_powerups > -1:
            self.rect.x = (config.SCREEN_WIDTH - self.rect.width - 880) - (self.amount_powerups * self.rect.width) - 10
            self.rect.y = (config.SCREEN_HEIGHT - self.rect.height - 650) - (
                    self.amount_powerups * self.rect.width) - 10

    def update(self, player_rect, powerups):
        """
        :return: picked_up_item
        :rtype: list
        """
        self.powerups = powerups

        for event in pygame.event.get(
                self.POWERUP_RESPAWN_EVENT
        ):
            if event.type == self.POWERUP_RESPAWN_EVENT:
                print("Powerup respawned - TRIGGERED")
                self.respawn_powerups()
                pygame.display.flip()

        for powerup in self.powerups:
            if player_rect.colliderect(powerup):
                self.on_pick_up(powerup)

        return self.picked_up_item

    def respawn_powerups(self):
        for p in self.powerup_respawn_list:
            self.powerups.add(Powerup(p))
        self.powerup_respawn_list.clear()

    def on_pick_up(self, powerup):
        event = pygame.event.Event(self.POWERUP_RESPAWN_EVENT)
        pygame.event.post(event)

        self.powerups.remove(powerup)
        self.picked_up_item.append(random.choice(self.effects))
        self.powerup_respawn_list.append(powerup)
