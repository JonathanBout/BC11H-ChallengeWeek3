from game.world import World


class Map(World):
    def __init__(self, config, name, description, position):
        """
        Initialize a Map object.
        :param config: The configuration for the map.
        :param name: The name of the map.
        :param description: The description of the map.
        :param position: The position of the map.
        """
        super().__init__(config, name, description, position)

    def print_config(self):
        """
        Prints the configuration values which could be of importance for the Map object.
        :return: None
        """
        if self.config is None:
            print("Config is None")
            return False
        else:
            for var_name in dir(self.config):
                if var_name.isupper():  # Checking if it's constant (by convention constants are upper-case)
                    if var_name.startswith("MAP_"):
                        print(f"{var_name}: {getattr(self.config, var_name)}")
