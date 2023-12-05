import pygame
from game import config, helper, sprites
from game.score_manager import ScoreManager
from game.stats import Stats
from util.sprite_overrides import create
from pygame.font import Font


class GameWon:
    def __init__(self, font: Font) -> None:
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )
        self.font = font

        self.background_image = sprites.get_menu_background_sprite(
            left=0,
            top=0,
            target_size=(config.SCREEN_SIZE[0] * 1.3, config.SCREEN_SIZE[1] * 1.4),
        )

        self.game_over_text = create(
            self.font.render("You won!", True, "white"),
            x_center=config.SCREEN_CENTER_X,
            top=config.SCREEN_HEIGHT / 10,
        )

        # self.to_menu_button = sprites
        self.play_again_button = sprites.get_button_playagain_sprite(
            config.SCREEN_CENTER_X, top=self.game_over_text.rect.bottom + 20
        )

        self.to_menu_button = sprites.get_button_back_sprite(
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

    def show(self, score_manager: ScoreManager, stats: Stats):
        pygame.display.set_caption("You Won!")
        score = score_manager.get_score()

        stats.add_stat(score)

        while True:
            self.screen.blits([*self.to_blit])
            if self.play_again_button.is_clicked():
                return 1  # 1=play again
            elif self.to_menu_button.is_clicked():
                return 0  # 0=to menu
            helper.exit_if_user_wants()
            pygame.display.flip()
