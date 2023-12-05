from game.map_manager import MapManager, MapConfig
from pygame.font import Font
import pygame
from game import config, sprites, helper
from util.sprite_overrides import SurfaceSprite


class MapChooser:
    def __init__(self, font: Font, map_manager: MapManager) -> None:
        self.map_manager = map_manager
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )

        self.background_image = sprites.get_menu_background_sprite(
            x_center=0,
            y_center=0,
            target_size=(config.SCREEN_SIZE[0] * 1.3, config.SCREEN_SIZE[1] * 1.4),
        )

        self.button_back = sprites.get_button_back_sprite(
            x_center=config.SCREEN_CENTER_X, top=config.SCREEN_HEIGHT / 10 * 9
        )

        self.font = font

        self.to_blit = [
            (x.image, x.rect) for x in [self.background_image, self.button_back]
        ]
        rendered = self.__render_text("Choose Your Map", config.SCREEN_WIDTH, 10)
        image_rect_tuple = (rendered, pygame.Rect(0, 0, *rendered.get_size()))
        self.to_blit.append(image_rect_tuple)
        self.maps_starting_point = image_rect_tuple[-1].bottom + 10

    def show(self):
        helper.exit_if_user_wants()

        visible_maps: dict[SurfaceSprite, MapConfig] = {}
        line_start_position = self.maps_starting_point
        for map in self.map_manager.loaded_maps:
            map_text = f"{map.name}:\n{map.description}\n--------------------"
            rendered = self.__render_text(
                map_text, config.SCREEN_WIDTH, line_start_position
            )
            visible_maps[
                SurfaceSprite(
                    rendered, pygame.Rect(0, line_start_position, *rendered.get_size())
                )
            ] = map
            line_start_position += rendered.get_height() + 10

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

    def __render_text(self, text: str, width: int, starting_point=0):
        full_surface = pygame.Surface((width, 0), masks=(0, 0, 0, 0))
        for line in text.split("\n"):
            rendered = self.font.render(line, True, "white")
            new_surface = pygame.Surface(
                (width, full_surface.get_height() + rendered.get_height()),
                masks=(0, 0, 0, 0),
            )
            new_surface.blit(full_surface, (0, 0))
            new_surface.blit(rendered, (0, full_surface.get_height() + 10))
        return full_surface
