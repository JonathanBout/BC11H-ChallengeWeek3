from game.map_manager import MapManager, MapConfig
from pygame.font import Font
import pygame
from game import config, sprites, helper
from util.sprite_overrides import SurfaceSprite, create as create_sprite


class MapChooser:
    def __init__(self, font: Font, map_manager: MapManager) -> None:
        self.map_manager = map_manager
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
        text, (width, height) = self.__render_text("Choose Your Map")
        self.to_blit.append((text, pygame.Rect(0, 10, width, height)))
        self.maps_starting_point = height + 20

    def show(self):
        helper.exit_if_user_wants()

        visible_maps: dict[SurfaceSprite, MapConfig] = {}
        y_pos = self.maps_starting_point
        for map in self.map_manager.loaded_maps:
            pygame.draw.circle(
                self.screen,
                "red",
                (
                    100,
                    self.maps_starting_point,
                ),
                10,
                10,
            )
            map_text = f"{map.name}:\n{map.description}\n--------------------"
            surface, (width, height) = self.__render_text(map_text)
            sprite = create_sprite(surface, x_center=width / 2, top=y_pos)
            visible_maps[sprite] = map
            y_pos += height + 10

        while not self.button_back.is_clicked():
            maps_to_blit = [
                (sprite.image, sprite.rect) for sprite in visible_maps.keys()
            ]
            self.screen.blits([*self.to_blit, *maps_to_blit])
            helper.exit_if_user_wants()
            pygame.display.flip()

            for sprite, map_config in visible_maps.items():
                if sprite.is_clicked():
                    return map_config

            self.clock.tick(config.MAX_FPS)

    def __render_text(self, text: str):
        destination_surface: pygame.Surface = None
        for line in text.split("\n"):
            text_to_blit = self.font.render(line, True, "white")
            if destination_surface:
                dest_width = destination_surface.get_width()
                dest_height = destination_surface.get_height()
                text_width = text_to_blit.get_width()
                new_width = max(dest_width, text_width)
                half_new_width = new_width / 2
                new_height = (
                    destination_surface.get_height() + text_to_blit.get_height() + 10
                )
                new_surface = pygame.Surface(
                    (new_width, new_height), pygame.SRCALPHA, 32
                )
                new_surface.blit(
                    destination_surface, (half_new_width - dest_width / 2, 0)
                )
                new_surface.blit(
                    text_to_blit, (half_new_width - text_width / 2, dest_height + 10)
                )
                destination_surface = new_surface
            else:
                destination_surface = text_to_blit
        return destination_surface, destination_surface.get_size()
