class World:
    config = "None"
    name = "name_placeholder"
    description = "description_placeholder"
    position = [0, 0]

    def __init__(self, config, name, description, position):
        """
        Constructor for the World class.
        :param config: The configuration for the world.
        :type config: any
        :param name: The name of the world.
        :type name: str
        :param description: The description of the world.
        :type description: str
        :param position: The position of the world.
        :type position: tuple
        """
        self.config = config
        self.name = name
        self.description = description
        self.position = position

    def print_config(self):
        """
        Prints the configuration values which could be of importance for the World object.
        :return: None
        """
        if self.config is None:
            print("Config is None")
            return False
        else:
            for var_name in dir(self.config):
                if var_name.isupper():  # checking if it's constant (by convention constants are upper-case)
                    if var_name.startswith("WORLD_"):
                        print(f"{var_name}: {getattr(self.config, var_name)}")
