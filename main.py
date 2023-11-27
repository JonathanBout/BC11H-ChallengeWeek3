from map import Map
from world import World
from player import Player
import config as c


def main():
    # Object creation
    world = World(c, c.WORLD_NAME, c.WORLD_DESCRIPTION, c.WORLD_POSITION)
    race_track = Map(c, c.MAP_NAME, c.MAP_DESCRIPTION, c.MAP_POSITION)
    player = Player(c, c.PLAYER_NAME, c.PLAYER_DESCRIPTION, c.PLAYER_POSITION)

    # Call methods
    world.print_config()
    race_track.print_config()
    player.print_config()


if __name__ == "__main__":
    main()
    # gameConfig = Config()
    # world = World()
    # myMap = Map()
    # myPlayer = Player()
