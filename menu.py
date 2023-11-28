import pygame

import config
import sprites
from game import Game


class Menu:
    def __init__(self) -> None:
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )

        self.background_image = sprites.menu_background(
            x_center=config.SCREEN_CENTER_X,
            y_center=config.SCREEN_CENTER_Y,
        )
        self.logo = sprites.logo(x_center=config.SCREEN_CENTER_X, top=10)

        self.button_start_game = sprites.button_start(
            x_center=config.SCREEN_CENTER_X,
            top=self.logo.rect.bottom + 10,
        )
        self.button_quit_image = sprites.button_quit(
            x_center=config.SCREEN_CENTER_X,
            top=self.button_start_game.rect.bottom + 10,
        )

    def show(self, game: Game):
        pygame.display.flip()
        while (x := self.__show_menu()) == 0:
            pygame.event.pump()
            game.render()
        return x

    def __show_menu(self) -> int:
        self.screen.blits(
            [
                (self.background_image.image, self.background_image.rect),
                (self.logo.image, self.logo.rect),
                (self.button_quit_image.image, self.button_quit_image.rect),
                (self.button_start_game.image, self.button_start_game.rect),
            ]
        )

        if self.button_start_game.is_clicked():
            print("Start Game")
            return 1
        elif self.button_quit_image.is_clicked():
            print("Quit Game")
            return 2
        return 0
