import pygame

import config as c
from map import Map
from world import World
from player import Player


class Game:
    def __init__(self):
        # initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        # initialize game objects
        self.world = World(c, c.WORLD_NAME, c.WORLD_DESCRIPTION, c.WORLD_POSITION)
        self.race_track = Map(c, c.MAP_NAME, c.MAP_DESCRIPTION, c.MAP_POSITION)
        self.player = Player(c, c.PLAYER_NAME, c.PLAYER_DESCRIPTION, c.PLAYER_POSITION)

    def start(self):
        # Set background color
        self.screen.fill("purple")

        # Start game loop
        self.update()

    def update(self):
        while True:
            # traversing through every event
            for event in pygame.event.get():
                # if the event type is QUIT then exit the program
                if event.type == pygame.QUIT:
                    exit()
            # render everything
            self.render()

    def render(self):
        # Update the full display surface to the screen
        pygame.display.flip()

        # Set target fps
        self.clock.tick(c.MAX_FPS)

        # printing the frames per second (fps) rate
        c.CURRENT_FPS = self.clock.get_fps()

        print(c.CURRENT_FPS)

    def print_config(self):
        self.world.print_config()
        self.race_track.print_config()
        self.player.print_config()
