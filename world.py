class World:
    config = None
    name = "name_placeholder"
    description = "description_placeholder"
    position = [0, 0]

    def __init__(self, config, name, description, position):
        self.config = config
        self.name = name
        self.description = description
        self.position = position
