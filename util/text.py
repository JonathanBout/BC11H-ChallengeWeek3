import pygame

class TextObject:
    def __init__(self, surface, position, creation_time, delay):
        self.surface = surface
        self.position = position
        self.creation_time = creation_time
        self.delay = delay


class TextRenderer:
    def __init__(self, font_name=None, font_size=32):
        pygame.font.init()
        self.font = pygame.font.Font(font_name, font_size)
        self.text_objects = []  # Temporary storage for text objects

    def render_text(self, surface, text, color, position, delay=3000):
        text_surface = self.font.render(text, True, color)
        text_object = TextObject(text_surface, position, pygame.time.get_ticks(), delay)
        self.text_objects.append(text_object)
        self.update(surface)

    def update(self, surface):
        current_time = pygame.time.get_ticks()
        self.text_objects = [text_object for text_object in self.text_objects if
                             current_time - text_object.creation_time < text_object.delay]
        for text_object in self.text_objects:
            surface.blit(text_object.surface, text_object.position)