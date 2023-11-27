import pygame
from pygame.sprite import Sprite


class ImageSprite(Sprite):
    def __init__(
        self,
        image_path: str,
        x_center: int = 0,
        y_center: int = 0,
        top: int = None,
        left: int = None,
    ) -> None:
        self.image = pygame.image.load(image_path)

        width = self.image.get_width()
        height = self.image.get_height()

        if not top:
            top = y_center - self.image.get_height() / 2

        if not left:
            left = x_center - self.image.get_width() / 2

        self.rect = pygame.Rect(left, top, width, height)

        def is_clicked(self):
            return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(
                pygame.mouse.get_pos()
            )
