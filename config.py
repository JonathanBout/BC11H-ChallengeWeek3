import pygame

# Game
MAX_FPS = 120
CURRENT_FPS = 0
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_CENTER_X = (SCREEN_WIDTH / 2)-30
SCREEN_CENTER_Y = (SCREEN_HEIGHT / 2)-30
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN_BACKGROUND = "sprites/win_background.png"

# World
WORLD_NAME = "Rainbow Road"
WORLD_DESCRIPTION = "A colorful track in the sky."
WORLD_POSITION = [0, 0]
WORLD_BACKGROUND = "sprites/background.png"
WORLD_WIDTH = SCREEN_WIDTH
WORLD_HEIGHT = SCREEN_HEIGHT

# Player
PLAYER_NAME = "Wario"
PLAYER_DESCRIPTION = "A fat, yellow, greedy, and smelly character."
PLAYER_POSITION = [SCREEN_CENTER_X, SCREEN_CENTER_Y]
PLAYER_CURRENT_POSITION = [0, 0]
PLAYER_SPRITE = "sprites/bowser.png"
PLAYER_SPRITE_WIDTH = 32
PLAYER_SPRITE_HEIGHT = 32
PLAYER_SPRITE_SCALE = 2
PLAYER_SPRITE_HORIZONTAL_FLIP = False
PLAYER_SPRITE_VERTICAL_FLIP = False
PLAYER_CURRENT_FRAME = 0
PLAYER_FRAME_UPDATE_INTERVAL = 5
PLAYER_MAX_SPEED = 300
PLAYER_MIN_SPEED = PLAYER_MAX_SPEED/2
PLAYER_AVG_SPEED = (PLAYER_MIN_SPEED + PLAYER_MAX_SPEED) / 2
PLAYER_CURRENT_SPEED = 10

# Map
MAP_NAME = WORLD_NAME
MAP_DESCRIPTION = WORLD_DESCRIPTION
MAP_POSITION = [0, 0]
MAP_SPRITE = "sprites/map_01.png"
MAP_WIDTH = 1280
MAP_HEIGHT = 720
