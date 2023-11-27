from world import World


class Map(World):
    def __init__(self, config, name, description, position):
        super().__init__(config, name, description, position)

    def print_config(self):
        print(World.config)
