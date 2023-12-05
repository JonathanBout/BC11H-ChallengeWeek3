from game import config, helper, sprites
from util.sprite_overrides import create

import pygame
from pygame.font import Font


class EndOfGame:
    def __init__(self, font: Font, title: str) -> None:
        self.title = title
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )
        self.font = font

        self.background_image = sprites.get_menu_background_sprite(
            left=0,
            top=0,
            target_size=(config.SCREEN_SIZE[0], config.SCREEN_SIZE[1]),
        )

        self.game_over_text = create(
            self.font.render(title, True, "black"),
            x_center=config.SCREEN_CENTER_X,
            top=config.SCREEN_HEIGHT / 10,
        )

        # self.to_menu_button = sprites
        self.play_again_button = sprites.get_button_playagain_sprite(
            config.SCREEN_CENTER_X, top=self.game_over_text.rect.bottom + 20
        )

        self.to_menu_button = sprites.get_button_back_to_menu_sprite(
            config.SCREEN_CENTER_X, top=self.play_again_button.rect.bottom + 20
        )

        self.to_blit = [
            (sprite.image, sprite.rect)
            for sprite in [
                self.background_image,
                self.game_over_text,
                self.play_again_button,
                self.to_menu_button,
            ]
        ]

    def show(self):
        pygame.display.set_caption(self.title)
        while True:
            self.screen.blits([*self.to_blit])
            if self.play_again_button.is_clicked():
                return 1  # 1=play again
            elif self.to_menu_button.is_clicked():
                return 0  # 0=to menu
            helper.exit_if_user_wants()
            pygame.display.flip()