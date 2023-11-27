from world import World


class Player(World):
    def __init__(self, config, name, description, position):
        super().__init__(config, name, description, position)
