from map import Map
from world import World
from player import Player
import config


def main():
    # Object creation
    world = World(config, config.WORLD_NAME, config.WORLD_DESCRIPTION, config.WORLD_POSITION)
    race_track = Map(config, config.MAP_NAME, config.MAP_DESCRIPTION, config.MAP_POSITION)

    # Set config
    config.PLAYER_MIN_SPEED = 0

    # Call methods
    race_track.print_config()
    world.print_config()


if __name__ == "__main__":
    main()
    # gameConfig = Config()
    # world = World()
    # myMap = Map()
    # myPlayer = Player()
