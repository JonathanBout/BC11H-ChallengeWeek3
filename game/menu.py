import pygame

import game.config as c
from game import config, helper
from game import sprites


class Menu:
    def __init__(self) -> None:
        pygame.display.set_caption(f"{c.GAME_TITLE}")

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )

        self.background_image = sprites.get_menu_background_sprite(
            left=0,
            top=0,
            target_size=(config.SCREEN_SIZE[0] * 1.3, config.SCREEN_SIZE[1] * 1.4),
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
        self.button_credits = sprites.get_powerup_box_sprite(
            left=10,
            top=config.SCREEN_HEIGHT
            - 60,  # subtract 60, as height=50 and offset from bottom 10
            target_size=(50, 50),
        )

        self.to_blit = [
            (image.image, image.rect)
            for image in [
                self.background_image,
                self.logo,
                self.button_start_game,
                self.button_quit_image,
                self.button_stats,
                self.button_credits,
            ]
        ]

    def show(self):
        pygame.display.flip()
        self.screen.fill("black")
        while (x := self.__show_menu()) == 0:
            helper.exit_if_user_wants()
            pygame.display.flip()
        return x

    def __show_menu(self) -> int:
        self.screen.blits(self.to_blit)

        if self.button_start_game.is_clicked():
            return 1
        elif self.button_quit_image.is_clicked():
            return 2
        elif self.button_stats.is_clicked():
            return 3
        elif self.button_credits.is_clicked():
            return 4
        return 0
