from world import World


class Map(World):
    def __init__(self, config, name, description, position):
        super().__init__(config)

    def print_config(self):
        World.print_config(self)

