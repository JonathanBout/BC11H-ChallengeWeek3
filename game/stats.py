from datetime import datetime
import pygame
from pygame.font import Font
from game import config, sprites, helper
import json
from os.path import isfile


class Stat:
    def __init__(self, score: str, date: datetime) -> None:
        self.score = score
        self.date = date


class Stats:
    def __init__(self, font: Font) -> None:
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
            x_center=config.SCREEN_CENTER_X, top=config.SCREEN_HEIGHT / 10 * 9
        )

        self.font = font

        self.to_blit = [
            (x.image, x.rect) for x in [self.background_image, self.button_back]
        ]

    def show(self):
        while not self.button_back.is_clicked():
            helper.exit_if_user_wants()
            self.screen.fill("black")
            text_to_show = ""
            for stat in self.get_stats():
                text_to_show += f"{stat.date.strftime()}: {stat.score}"

            if text_to_show == "":
                text_to_show = "No scores yet!"

            text = self.font.render(text_to_show, True, "black")
            self.screen.blits(
                [
                    *self.to_blit,
                    (
                        text,
                        (
                            config.SCREEN_CENTER_X - text.get_width() / 2,
                            config.SCREEN_HEIGHT / 10,
                        ),
                    ),
                ]
            )
            pygame.display.flip()
            self.clock.tick(config.MAX_FPS)

    def get_stats(self) -> list[Stat]:
        if not isfile(config.STATS_FILE):
            return []

        with open(config.STATS_FILE, "r") as stats_file:
            stored_scores = json.load(stats_file)
            return [Stat(score["score"], score["date"]) for score in stored_scores]

    def add_stat(self, score):
        current_stats = self.get_stats()
        current_stats.append(Stat(str(score), datetime.now()))
        with open(config.STATS_FILE, "w") as stats_file:
            json.dump(current_stats, stats_file)
