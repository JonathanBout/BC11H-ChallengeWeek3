from map import Map
from world import World
from player import Player
import config


def main():
    config.PLAYER_MIN_SPEED = 0
    world = World(config, config.WORLD_NAME, config.WORLD_DESCRIPTION, config.WORLD_POSITION)
    raceTrack = Map()
    raceTrack.print_config()


if __name__ == "__main__":
    main()
    # gameConfig = Config()
    # world = World()
    # myMap = Map()
    # myPlayer = Player()
