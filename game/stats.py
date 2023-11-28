import pygame
from game import config, sprites
import helper


class Stats:
    def __init__(self) -> None:
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )

        self.background_image = sprites.get_menu_background_sprite(
            x_center=config.SCREEN_CENTER_X,
            y_center=config.SCREEN_CENTER_Y,
            target_size=config.SCREEN_SIZE,
        )

        self.button_back = sprites.get_button_back_sprite(
            x_center=config.SCREEN_CENTER_X,
            top=config.SCREEN_HEIGHT / 10 * 9
        )

        self.to_blit = [(x.image, x.rect) for x in [self.background_image, self.button_back]]

    def show(self):
        while not self.button_back.is_clicked():
            helper.exit_if_user_wants()
            self.screen.fill("black")
            self.screen.blits(self.to_blit)
            pygame.display.flip()
            self.clock.tick(config.MAX_FPS)
