from game.world import World


class Map(World):
    def __init__(self, config, name, description, position):
        super().__init__(config ,name, description, position)

    def print_config(self):
        if self.config is None:
            print("Config is None")
            return False
        else:
            for var_name in dir(self.config):
                if var_name.isupper():  # checking if it's constant (by convention constants are upper-case)
                    if var_name.startswith("MAP_"):
                        print(f"{var_name}: {getattr(self.config, var_name)}")
