import pygame
from pygame.constants import USEREVENT

from game import config
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
        if config.SKIP_TRACK_CHECK:
            return

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
        # Display / Render
        self.screen = screen
        self.player_position = player_position
        # Sound
        self.finish_sound = Music(finish_sound, 2)
        self.lap_sound = Music(config.LAP_SOUND, 1)
        # Flags
        self.is_finish_triggered = False
        self.is_lap_triggered = False
        self.has_started_race = False
        self.was_on_finish = False
        self.is_on_finish = False
        # Counters
        self.finish_count = 0

    def trigger(self):
        # Update the position of the finish area relative to the map
        map_pos_x, map_pos_y = config.MAP_POSITION
        finish_area_position = (map_pos_x + 60, map_pos_y + 630)
        finish_area_size = (130, 40)

        # Adjust the player position to the bottom of the player sprite
        adjusted_player_position = (
            self.player_position[0],
            self.player_position[1] + config.PLAYER_SPRITE_HEIGHT * 1.5,
        )

        # Create the player hitbox (rect)
        player_rect = pygame.Rect(
            *adjusted_player_position,
            config.PLAYER_SPRITE_WIDTH * 2,
            config.PLAYER_SPRITE_HEIGHT * 0.5,
        )

        # Create the finish area hitbox (rect)
        finish_rect = pygame.Rect(*finish_area_position, *finish_area_size)

        # Check if the player is on the finish area
        keys = pygame.key.get_pressed()
        backwards = keys[pygame.K_s]

        # If we are not on the finish rect (we started racing),
        # reset the finish trigger and race start trigger
        if finish_rect.colliderect(player_rect):
            if not self.was_on_finish:
                self.has_started_race = True
            else:
                config.RACE_CURRENT_LAP -= 1

        if finish_rect.colliderect(player_rect):
            if not backwards:
                if not self.is_on_finish:
                    self.is_on_finish = True
                    config.RACE_CURRENT_LAP += 1
                    if config.RACE_CURRENT_LAP >= config.RACE_LAPS:
                        self.handle_finish()
                    else:
                        self.handle_lap()
            else:
                if not self.is_on_finish:
                    self.is_on_finish = True
                    config.RACE_CURRENT_LAP -= 1
                    print(
                        "REVERSING OVER THE FINISH DOESN'T COUNT! NOW AT LAP",
                        config.RACE_CURRENT_LAP,
                    )
        else:
            self.is_on_finish = False

        # Draw hitboxes
        pygame.draw.rect(self.screen, (255, 0, 0), finish_rect)
        pygame.draw.rect(self.screen, (0, 255, 0), player_rect)

    # Define how handle_finish and handle_lap works, replace `camera` with your camera instance.
    def handle_finish(self):
        print("YOU FINISHED! CURRENT LAP")

        self.finish_sound.play()
        pygame.event.post(pygame.event.Event(config.PLAYER_WON_EVENT))

    def handle_lap(self):
        print("NEXT LAP! CURRENT LAP: ", config.RACE_CURRENT_LAP)
        self.lap_sound.play()


class EventManager:
    def __init__(self):
        self.events = []

    def register_event(self, event):
        self.events.append(event)

    def trigger_events(self):
        for event in self.events:
            event.trigger()
