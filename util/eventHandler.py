import pygame
from pygame.constants import USEREVENT

from game import config, camera
from util.music import Music


class CustomEvent:
    def __init__(self, delay=3000):
        self.EVENT_TYPE = USEREVENT + 1
        pygame.time.set_timer(self.EVENT_TYPE, delay)

    def trigger(self):
        raise NotImplementedError


class RespawnEvent(CustomEvent):
    def __init__(self, screen, player_position, respawn_sound):
        super().__init__()
        self.screen = screen
        self.player_position = player_position
        self.respawn_sound = Music(respawn_sound, 1)
        self.is_respawn_triggered = False

    def trigger(self):
        # Get the color of the pixel at the player's position
        color = self.screen.get_at(
            (
                int(self.player_position[0] + config.PLAYER_SPRITE_HEIGHT * 2),
                int(self.player_position[1] + config.PLAYER_SPRITE_WIDTH * 2),
            )
        )

        # The color of the respawn area
        respawn_color = (0, 0, 96, 255)

        # If the player is on the road, reset the respawn trigger
        if color != respawn_color:
            self.is_respawn_triggered = False

        # If the player is not on the road, trigger the respawn event
        if color == respawn_color:
            if not self.is_respawn_triggered:
                self.is_respawn_triggered = True
                self.handle_respawn()

    def handle_respawn(self):
        print("C: ", config.PLAYER_CURRENT_POSITION)
        print("R: ", config.PLAYER_RESPAWN_POSITION)
        print("You are no longer on the road!")
        self.respawn_sound.play()
        config.MAP_POSITION = [0, 0]
        config.PLAYER_CURRENT_POSITION = config.PLAYER_RESPAWN_POSITION[:]

        pygame.event.post(pygame.event.Event(config.PLAYER_GAMEOVER_EVENT))


class FinishEvent(CustomEvent):
    def __init__(self, screen, player_position, finish_sound):
        super().__init__()
        self.screen = screen
        self.player_position = player_position
        self.finish_sound = Music(finish_sound, 2)
        self.lap_sound = Music(config.LAP_SOUND, 1)
        self.is_finish_triggered = False
        self.is_lap_triggered = False
        self.finish_count = 0
        self.previous_color = None
        self.was_on_finish_color = True
        self.has_started_race = False

    def handle_finish(self):
        # You need to define the implementation of handle_finish
        pass

    def handle_lap(self):
        # You need to define the implementation of handle_lap
        pass

    def trigger(self):
        player_rect = pygame.Rect(*self.player_position, config.PLAYER_SPRITE_WIDTH * 2,
                                  config.PLAYER_SPRITE_HEIGHT * 2)

        camera_inst = camera
        map_pos_x, map_pos_y = config.MAP_POSITION
        finish_area_position = (map_pos_x + 60, map_pos_y + 630)
        finish_area_size = (130, 40)

        finish_rect = pygame.Rect(*finish_area_position, *finish_area_size)

        keys = pygame.key.get_pressed()
        backwards = keys[pygame.K_s]

        # If we are not on the finish rect (we started racing),
        # reset the finish trigger and race start trigger
        if not finish_rect.colliderect(player_rect):
            if not self.was_on_finish_color:
                self.was_on_finish_color = True
            if not self.has_started_race:
                self.has_started_race = True

        if finish_rect.colliderect(player_rect):
            if self.was_on_finish_color:
                if self.has_started_race:
                    self.finish_count += 1
                    self.finish_sound.play()

        print(f"Finish count: {self.finish_count}\n" * 100)

        # if self.was_on_finish_color:
        #     if self.has_started_race:
        #         if not backwards:
        #             self.is_finish_triggered = True
        #         else:
        #             self.is_lap_triggered = True
        #         print(f"Finish triggered: {self.is_finish_triggered}\n"
        #               f"Lap triggered: {self.is_lap_triggered}\n"
        #               f"Finish count: {self.finish_count}\n" * 100)

        # if self.is_finish_triggered:
        #     self.finish_count += 1
        #     self.is_finish_triggered = False
        #     self.handle_finish()
        #
        # if self.is_lap_triggered:
        #     self.is_lap_triggered = False
        #     self.handle_lap()

        pygame.draw.rect(self.screen, (255, 0, 0), finish_rect)

    # Define how handle_finish and handle_lap works, replace `camera` with your camera instance.
    def handle_finish(self):
        print("Handle finish")
        self.finish_sound.play()

    def handle_lap(self):
        print("Handle lap")
        self.lap_sound.play()


class EventManager:
    def __init__(self):
        self.events = []

    def register_event(self, event):
        self.events.append(event)

    def trigger_events(self):
        for event in self.events:
            event.trigger()
