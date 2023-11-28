import helper
import pygame

from game import config
from game import sprites


class Menu:
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

        self.background_image.image = pygame.transform.scale(
            self.background_image.image, config.SCREEN_SIZE
        )

        self.logo = sprites.get_logo_menu_sprite(
            x_center=config.SCREEN_CENTER_X, top=config.SCREEN_HEIGHT / 10
        )

        self.button_start_game = sprites.get_button_start_sprite(
            x_center=config.SCREEN_CENTER_X,
            top=self.logo.rect.bottom + 10,
        )
        self.button_quit_image = sprites.get_button_quit_sprite(
            x_center=config.SCREEN_CENTER_X,
            top=self.button_start_game.rect.bottom + 10,
        )
        self.button_stats = sprites.get_button_stats_sprite(
            x_center=config.SCREEN_CENTER_X, top=self.button_quit_image.rect.bottom + 10
        )

    def show(self):
        pygame.display.flip()
        while (x := self.__show_menu()) == 0:
            helper.exit_if_user_wants()
            pygame.display.flip()
        return x

    def __show_menu(self) -> int:
        self.screen.blits(
            [
                (self.background_image.image, self.background_image.rect),
                (self.logo.image, self.logo.rect),
                (self.button_quit_image.image, self.button_quit_image.rect),
                (self.button_start_game.image, self.button_start_game.rect),
                (self.button_stats.image, self.button_stats.rect),
            ]
        )

        if self.button_start_game.is_clicked():
            return 1
        elif self.button_quit_image.is_clicked():
            return 2
        elif self.button_stats.is_clicked():
            return 3
        return 0
