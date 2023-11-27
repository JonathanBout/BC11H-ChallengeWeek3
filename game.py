import config as c
from map import Map
from world import World
from player import Player


class Game:
    def __init__(self):
        self.world = World(c, c.WORLD_NAME, c.WORLD_DESCRIPTION, c.WORLD_POSITION)
        self.race_track = Map(c, c.MAP_NAME, c.MAP_DESCRIPTION, c.MAP_POSITION)
        self.player = Player(c, c.PLAYER_NAME, c.PLAYER_DESCRIPTION, c.PLAYER_POSITION)

    def start(self):
        pass

    def print_config(self):
        self.world.print_config()
        self.race_track.print_config()
        self.player.print_config()