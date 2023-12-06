from datetime import datetime
import pygame
from pygame.font import Font
from game import config, sprites, helper
import json
from os.path import isfile, getsize

from game.map_chooser import MapChooser
from game.map_manager import MapManager


class Stat:
    def __init__(self, score: int, map: str, date: datetime) -> None:
        self.score = score
        self.date = date
        self.map = map

    def get_json_dict(self):
        return {
            "score": self.score,
            "date": self.date.strftime(config.STATS_DATE_FORMAT),
            "map": self.map,
        }

    @staticmethod
    def from_json_dict(json_dict: dict):
        map_name = "unknown"
        if "map" in json_dict:
            map_name = json_dict["map"]
        return Stat(
            json_dict["score"],
            map_name,
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
            target_size=(config.SCREEN_SIZE[0], config.SCREEN_SIZE[1]),
        )

        self.button_back = sprites.get_button_back_sprite(
            x_center=config.SCREEN_CENTER_X, top=config.SCREEN_HEIGHT / 10 * 9
        )

        self.font = font

        self.to_blit = [
            (x.image, x.rect) for x in [self.background_image, self.button_back]
        ]

        self.map_chooser = MapChooser(self.font, MapManager())

    def show(self):
        if map_config := self.map_chooser.show():
            while not self.button_back.is_clicked():
                helper.exit_if_user_wants()
                text_to_show = ""
                place = 1
                for stat in self.get_stats(top=10, map_name=map_config.name):
                    text_to_show += f"{str(place).rjust(2)}. {stat.date.strftime('%b %d %Y, %H:%M')}: {stat.score} points\n"
                    place += 1

                if text_to_show == "":
                    text_to_show = "No scores yet!"

                self.__write_to_screen(text_to_show)
                pygame.display.flip()
                self.clock.tick(config.MAX_FPS)

    def __write_to_screen(self, text: str):
        lines_to_blit = []
        last_y = 10
        if text == "No scores yet!":
            center_x = config.SCREEN_CENTER_X - 182
        else:
            center_x = config.SCREEN_CENTER_X / 2 - 75
        for line in text.split("\n"):
            text_to_blit = self.font.render(line, True, "white")
            lines_to_blit.append((text_to_blit, (center_x, last_y)))
            last_y += text_to_blit.get_height() + 10

        self.screen.blits([*self.to_blit, *lines_to_blit])

    def get_stats(self, top=-1, map_name="") -> list[Stat]:
        if not isfile(config.STATS_FILE) or getsize(config.STATS_FILE) == 0:
            return []

        with open(config.STATS_FILE, "r") as stats_file:
            stored_scores = json.load(stats_file)
            scores = [Stat.from_json_dict(score) for score in stored_scores]
            if map_name != "":
                scores = [
                    score for score in scores if score.map.lower() == map_name.lower() or score.map.lower() == "unknown"
                ]
            scores.sort(key=lambda i: i.get_order(), reverse=True)
            if top > 0:
                scores = scores[:top]
            return scores

    def add_stat(self, score: int, map: str):
        current_stats = self.get_stats()
        current_stats.append(Stat(score, map, datetime.now()))

        current_stats = [stat.get_json_dict() for stat in current_stats]

        with open(config.STATS_FILE, "w") as stats_file:
            json.dump(current_stats, stats_file)
