from datetime import datetime
import pygame
from pygame.font import Font
from game import config, sprites, helper
import json
from os.path import isfile, getsize


class Stat:
    def __init__(self, score: int, date: datetime) -> None:
        self.score = score
        self.date = date

    def get_json_dict(self):
        return {
            "score": self.score,
            "date": self.date.strftime(config.STATS_DATE_FORMAT),
        }

    @staticmethod
    def from_json_dict(json_dict):
        return Stat(
            json_dict["score"],
            datetime.strptime(json_dict["date"], config.STATS_DATE_FORMAT),
        )

    def get_order(self):
        return int(self.score)


class Stats:
    def __init__(self, font: Font) -> None:
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )

        self.background_image = sprites.get_menu_background_sprite(
            left=0,
            top=0,
            target_size=(config.SCREEN_SIZE[0] * 1.3, config.SCREEN_SIZE[1] * 1.4),
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
            text_to_show = ""
            place = 1
            for stat in self.get_stats(top=10):
                text_to_show += f"{str(place).rjust(2)}. {stat.date.strftime('%b %d %Y, %H:%M')}: {stat.score} points\r\n"
                place += 1

            if text_to_show == "":
                text_to_show = "No scores yet!"

            self.__write_to_screen(text_to_show)
            pygame.display.flip()
            self.clock.tick(config.MAX_FPS)

    def __write_to_screen(self, text: str):
        lines_to_blit = []
        last_y = 10
        for line in text.split("\n"):
            text_to_blit = self.font.render(line, True, "white")
            lines_to_blit.append((text_to_blit, (config.SCREEN_CENTER_X/2-80, last_y)))
            last_y += text_to_blit.get_height() + 10

        self.screen.blits([*self.to_blit, *lines_to_blit])

    def get_stats(self, top=-1) -> list[Stat]:
        if not isfile(config.STATS_FILE) or getsize(config.STATS_FILE) == 0:
            return []

        with open(config.STATS_FILE, "r") as stats_file:
            stored_scores = json.load(stats_file)
            scores = [Stat.from_json_dict(score) for score in stored_scores]
            scores.sort(key=lambda i: i.get_order())
            if top > 0:
                scores = scores[:top]
            return scores

    def add_stat(self, score: int):
        current_stats = self.get_stats()
        current_stats.append(Stat(score, datetime.now()))

        current_stats = [stat.get_json_dict() for stat in current_stats]

        with open(config.STATS_FILE, "w") as stats_file:
            json.dump(current_stats, stats_file)
