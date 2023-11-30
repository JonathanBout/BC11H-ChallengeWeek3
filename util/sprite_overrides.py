import pygame
from pygame.sprite import Sprite
from pygame import Surface


class ImageSprite(Sprite):
    def __init__(
        self,
        image: str | Surface,
        x_center: int = 0,
        y_center: int = 0,
        top: int = None,
        left: int = None,
        target_size: tuple[int | None, int | None] = None,
    ) -> None:
        if not isinstance(image, Surface):
            image = pygame.image.load(f"{image}")

        self.image = image

        if target_size:
            if not target_size[0]:
                target_size = (self.image.get_width(), target_size[1])
            if not target_size[1]:
                target_size = (target_size[0], self.image.get_height())
            image = pygame.transform.scale(self.image, target_size)

        if not top:
            top = y_center - self.image.get_height() // 2

        if not left:
            left = x_center - self.image.get_width() // 2

        self.rect = pygame.Rect(left, top, image.get_width(), image.get_height())
        self.image = image

    def is_clicked(self):
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(
            pygame.mouse.get_pos()
        )
