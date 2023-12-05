import pygame
from pygame.sprite import Sprite
from pygame import Surface


def create(
    image: str | Surface,
    x_center: int = 0,
    y_center: int = 0,
    top: int = None,
    left: int = None,
    target_size: tuple[int | None, int | None] = None,
):
    if not isinstance(image, Surface):
        image = pygame.image.load(f"{image}")

    if target_size:
        if not target_size[0]:
            target_size = (image.get_width(), target_size[1])
        if not target_size[1]:
            target_size = (target_size[0], image.get_height())

        image = pygame.transform.scale(image, target_size)

    if top is None:
        top = y_center - image.get_height() // 2

    if left is None:
        left = x_center - image.get_width() // 2

    return SurfaceSprite(
        image, pygame.Rect(left, top, image.get_width(), image.get_height())
    )


class SurfaceSprite(Sprite):
    def __init__(self, sprite: pygame.Surface, rect: pygame.Rect):
        self.rect = rect
        self.image = sprite

    def is_clicked(self):
        return pygame.mouse.get_pressed()[0] and self.is_hovering()

    def is_hovering(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
