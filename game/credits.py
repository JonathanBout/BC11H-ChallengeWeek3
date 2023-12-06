from pygame.font import Font
import pygame
from game import config, helper, sprites
from game.display import Display
from util.music import Music
from time import sleep

PIXELS_PER_SECOND = 65


class Credits:
    def __init__(self, font: Font) -> None:
        self.clock = Display().clock
        self.screen = Display().set_display_size()
        self.font = font

        self.background_image = sprites.get_menu_background_sprite(
            left=0,
            top=0,
            target_size=(config.SCREEN_SIZE[0], config.SCREEN_SIZE[1]),
        )

        self.logo = sprites.logo_menu

    def show(self):
        Music(config.POWERUP_SOUND).play()
        sleep(1)
        y_pos = config.SCREEN_HEIGHT / 10
        current_speed = 0
        while self.__write_to_screen(
            """\n\n\n\n\n\n\n\n\n\n\n
programming
----------------------------------
Ruben Flinterman
Jonathan Bout
\n\n\n\n
project management
----------------------------------
Ruben Flinterman
Jonathan Bout
\n\n\n\n
planning
----------------------------------
Ruben Flinterman
Jonathan Bout
\n\n\n\n
sounds
----------------------------------
FROM
themushroomkingdom.net
\n\n\n\n
sprites
----------------------------------
FROM
pygame.org/project/3596
spriters-resource.com
\n
MODIFIED BY
Ruben Flinterman
Jonathan Bout
\n\n\n\n
Thank you for playing!""",
            y_pos,
        ):
            dt = self.clock.tick(120) / 1000
            if current_speed < PIXELS_PER_SECOND:
                current_speed += dt * 10
            y_pos -= dt * current_speed
            pygame.display.flip()
            helper.exit_if_user_wants()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                break

    def __write_to_screen(self, text: str, distance_from_top: int) -> bool:
        last_y = distance_from_top
        lines_to_blit = [
            (self.logo, (config.UI_SCREEN_CENTER_X - self.logo.get_width() / 2, last_y))
        ]
        last_y += self.logo.get_height()
        for line in text.split("\n"):
            text_to_blit = self.font.render(line, True, "white")
            lines_to_blit.append(
                (
                    text_to_blit,
                    (config.UI_SCREEN_CENTER_X - text_to_blit.get_width() / 2, last_y),
                )
            )
            last_y += text_to_blit.get_height() + 10

        self.screen.blits(
            [(self.background_image.image, self.background_image.rect), *lines_to_blit]
        )

        return last_y > 0
