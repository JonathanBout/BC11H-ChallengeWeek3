import math
import time

import pygame
from pygame.surface import Surface
from game.camera import Camera
from game import config
from game import powerup
from util.eventHandler import EventManager, RespawnEvent, FinishEvent
from game.display import Display


class PlayerBase:
    def __init__(
        self, config: config, player_number, name, description, position, player_sprite
    ):
        self.config = config
        self.name = name
        self.description = description
        self.position = position
        self.display = Display()
        self.player_number = player_number
        self.player_sprite = player_sprite
        self.num_sprites = 0
        self.finish_event = FinishEvent(
            None, config.PLAYER_1_POSITION, config.FINISH_SOUND
        )
        self.POWERUP_RESPAWN_TIME = 5000
        self.powerup_respawn_time = None
        self.item_inventory = []

    def prepare(self, frame=0):
        game_image = pygame.image.load(self.player_sprite).convert_alpha()
        sprite_width = config.PLAYER_SPRITE_WIDTH
        sprite_height = config.PLAYER_SPRITE_HEIGHT
        num_sprites = game_image.get_width() // sprite_width
        self.num_sprites = num_sprites
        sprites = []
        for i in range(num_sprites):
            sprite_x = i * sprite_width
            sprite = game_image.subsurface(
                pygame.Rect((sprite_x, 0, sprite_width, sprite_height))
            )
            sprite = pygame.transform.scale(
                sprite,
                (
                    sprite_width * config.PLAYER_SPRITE_SCALE,
                    sprite_height * config.PLAYER_SPRITE_SCALE,
                ),
            )
            sprites.append(sprite)
        return self.check_flip(sprites[frame])

    def move(
        self,
        screen: Surface,
        camera: Camera,
        controls: dict,
        current_position: list[int],
        powerup_list: pygame.sprite.Group,
    ):
        left = controls[pygame.K_a]
        right = controls[pygame.K_d]
        up = controls[pygame.K_w]
        down = controls[pygame.K_s]
        boost = controls[pygame.K_LSHIFT] or controls[pygame.K_RSHIFT]

        player_cnt = str(self.player_number)
        if config.CURRENT_FPS == 0:
            print("CURRENT_FPS value is Zero! Please, check the value.")
        else:
            self.display.dt = 1.0 / config.CURRENT_FPS

        player_rect = pygame.Rect(
            current_position,
            (config.PLAYER_SPRITE_WIDTH, config.PLAYER_SPRITE_HEIGHT),
        )

        player_speed = 0
        if player_cnt == "1":
            player_speed = config.PLAYER_1_CURRENT_SPEED
        if player_cnt == "2":
            player_speed = config.PLAYER_2_CURRENT_SPEED

        player_acceleration = config.PLAYER_MAX_SPEED
        player_friction = config.PLAYER_FRICTION

        frame_idle = self.num_sprites // 2
        current_frame = frame_idle
        frame_delta = 1 if left or right else 0

        initial_player_speed = player_speed

        # Check if player is on a powerup and update accordingly
        items = powerup.Powerup(-1).update(player_rect, powerup_list)
        if items:
            self.item_inventory.extend(items)
        print("Inventory: ", self.item_inventory)

        if initial_player_speed <= config.PLAYER_MAX_SPEED:
            player_speed = (
                initial_player_speed + player_acceleration * self.display.dt
            ) * player_friction

        if up:
            player_rect.y -= int(player_speed)
            current_frame = 0
        if down:
            player_rect.y += int(player_speed)
            current_frame = 10
        if left:
            config.PLAYER_SPRITE_HORIZONTAL_FLIP = True
            player_rect.x -= int(player_speed)
            current_frame = min(current_frame + frame_delta, self.num_sprites - 4)
        if right:
            config.PLAYER_SPRITE_HORIZONTAL_FLIP = False
            player_rect.x += int(player_speed)
            current_frame = min(current_frame + frame_delta, self.num_sprites - 4)

        store_speed = player_speed

        if boost and self.item_inventory is not None:
            if "Boost" in self.item_inventory:
                player_speed = player_speed * 3
            if "Slow" in self.item_inventory:
                player_speed = player_speed / 5

        else:
            for event in pygame.event.get(pygame.KEYUP):
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        if "Boost" in self.item_inventory:
                            self.item_inventory.remove("Boost")
                        elif "Slow" in self.item_inventory:
                            self.item_inventory.remove("Slow")
            player_speed = store_speed

        if (up or down) and (left or right):
            player_speed = player_speed / math.sqrt(2)

        any_keys = up or down or left or right

        if not any_keys:
            player_speed = 0
            config.PLAYER_CURRENT_FRAME = frame_idle

        if player_cnt == "1":
            config.PLAYER_1_CURRENT_SPEED = round(player_speed, 0)
            config.PLAYER_1_CURRENT_FRAME = current_frame
        if player_cnt == "2":
            config.PLAYER_2_CURRENT_SPEED = round(player_speed, 0)
            config.PLAYER_2_CURRENT_FRAME = current_frame

        screen_rect = pygame.Rect(
            0,
            0,
            config.SCREEN_WIDTH - config.PLAYER_SPRITE_WIDTH,
            config.SCREEN_HEIGHT - config.PLAYER_SPRITE_HEIGHT,
        )

        player_rect, screen_rect = camera.do_movement(
            player_rect, screen_rect, powerup_list
        )

        (
            current_position[0],
            current_position[1],
        ) = player_rect.topleft

        screen.blit(self.prepare(current_frame), current_position)

    def check_for_events(
        self, screen: Surface, map_rects: list[pygame.Rect], current_position
    ):
        # Create event manager
        event_manager = EventManager()

        # Create respawn event
        respawn_event = RespawnEvent(
            map_rects,
            current_position,
            config.RESPAWN_SOUND,
        )

        # Create finish event
        self.finish_event.player_position = current_position
        self.finish_event.screen = screen

        # Register events
        event_manager.register_event(respawn_event)
        event_manager.register_event(self.finish_event)

        # Trigger events, if any pass
        event_manager.trigger_events()

    def check_flip(self, player):
        if config.PLAYER_SPRITE_HORIZONTAL_FLIP or config.PLAYER_SPRITE_VERTICAL_FLIP:
            player = pygame.transform.flip(
                surface=player,
                flip_x=config.PLAYER_SPRITE_HORIZONTAL_FLIP,
                flip_y=config.PLAYER_SPRITE_VERTICAL_FLIP,
            )
        return player

    def reset(self):
        config.PLAYER_CURRENT_POSITION = config.PLAYER_RESPAWN_POSITION[:]
        config.PLAYER_POSITION = config.PLAYER_CURRENT_POSITION[:]
        config.PLAYER_CURRENT_SPEED = 0
        config.RACE_CURRENT_LAP = 0

    def print_config(self):
        if self.config is None:
            print("Config is None")
            return False
        else:
            for var_name in dir(self.config):
                if var_name.isupper():
                    if var_name.startswith("PLAYER_"):
                        print(f"{var_name}: {getattr(self.config, var_name)}")


class Player(PlayerBase):
    def __init__(self, config: config, name, description, position, player_sprite):
        super().__init__(config, 1, name, description, position, player_sprite)
