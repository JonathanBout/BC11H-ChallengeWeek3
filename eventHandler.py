import pygame
from pygame.constants import USEREVENT

import config as c
from music import Music


class CustomEvent:
    def __init__(self, delay=3000):
        self.EVENT_TYPE = USEREVENT + 1
        pygame.time.set_timer(self.EVENT_TYPE, delay)

    def trigger(self):
        raise NotImplementedError


class RespawnEvent(CustomEvent):
    def __init__(self, screen, player_position, text_renderer, respawn_sound, screen_center):
        super().__init__()
        self.screen = screen
        self.player_position = player_position
        self.text_renderer = text_renderer
        self.respawn_sound = Music(respawn_sound, 1)
        self.screen_center = screen_center
        self.is_respawn_triggered = False

    def trigger(self):
        # Get the color of the pixel at the player's position
        color = self.screen.get_at(
            (
                int(self.player_position[0] + 60),
                int(self.player_position[1] + 60)
            )
        )

        # If the player is not on the road, trigger the respawn event
        if color == (0, 0, 96, 255) and not self.is_respawn_triggered:
            self.is_respawn_triggered = True
            self.handle_respawn()
        else:
            self.is_respawn_triggered = False

    def handle_respawn(self):
        print("C: ", c.PLAYER_CURRENT_POSITION)
        print("R: ", c.PLAYER_RESPAWN_POSITION)
        print("You are no longer on the road!")
        self.respawn_sound.play()
        c.PLAYER_CURRENT_POSITION = c.PLAYER_RESPAWN_POSITION[:]
        self.text_renderer.render_text(
            self.screen,
            "You are no longer on the road!",
            (255, 255, 255),
            (self.screen_center[0] - 200, self.screen_center[1] - 100)
        )


class EventManager:
    def __init__(self):
        self.events = []

    def register_event(self, event):
        self.events.append(event)

    def trigger_events(self):
        for event in self.events:
            event.trigger()
