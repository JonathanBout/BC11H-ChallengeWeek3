import pygame

# GAME CONFIGURATION
# Game title
GAME_TITLE = "Wario Kart"

# Game icon
GAME_ICON = "assets/sprites/powerup_box.png"

# Whether the game is paused or not
GAME_PAUSED = False

# Window width
SCREEN_WIDTH = 1280

# Window height
SCREEN_HEIGHT = 720

# -30 to center the player horizontally
SCREEN_CENTER_X = (SCREEN_WIDTH / 2) - 30

# -30 to center the player vertically
SCREEN_CENTER_Y = (SCREEN_HEIGHT / 2) - 30

# Screen resolution
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# Center of the screen
SCREEN_CENTER = (SCREEN_CENTER_X, SCREEN_CENTER_Y)

# Maximum FPS
MAX_FPS = 120

# Current FPS
CURRENT_FPS = MAX_FPS

# Seconds per frame, to make speeds frame-independent
SECONDS_PER_FRAME = 1 / MAX_FPS

# WORLD CONFIGURATION

# World position, relative to the screen
WORLD_POSITION = [0, 0]

# World width = screen width
WORLD_WIDTH = SCREEN_WIDTH

# World height = screen height
WORLD_HEIGHT = SCREEN_HEIGHT

# PLAYER CONFIGURATION
# What's the player's name?
PLAYER_NAME = "Wario"
ENEMY_NAME = "Waluigi"

# What's the player like?
PLAYER_1_DESCRIPTION = "A fat, yellow, greedy, and smelly character."
ENEMY_DESCRIPTION = "Short-tempered, big, and bad."

# Inventory
PLAYER_INVENTORY = []

# Player position, relative to the screen
PLAYER_POSITION = [SCREEN_CENTER_X, SCREEN_CENTER_Y]

# Player respawn position, relative to the screen
PLAYER_RESPAWN_POSITION = [127, 494]

# Player current position starts at the respawn position
PLAYER_CURRENT_POSITION = PLAYER_RESPAWN_POSITION[:]

# Player sprite
PLAYER_SPRITE = None
PLAYER_SPRITE = "assets/sprites/wario.png"
ENEMY_SPRITE = "assets/sprites/waluigi.png"
PLAYER_SPRITE_WIDTH = 32
PLAYER_SPRITE_HEIGHT = 32
PLAYER_SPRITE_SCALE = 2

# Should we flip the player's sprite?
PLAYER_SPRITE_HORIZONTAL_FLIP = False
PLAYER_SPRITE_VERTICAL_FLIP = False

# Which animation frame is the player currently on?
PLAYER_CURRENT_FRAME = 0

# Player's speed
PLAYER_MAX_SPEED = 20000
PLAYER_MIN_SPEED = PLAYER_MAX_SPEED / 1.5
PLAYER_AVG_SPEED = (PLAYER_MIN_SPEED + PLAYER_MAX_SPEED) / 2
PLAYER_FRICTION = 0.2
PLAYER_CURRENT_SPEED = 1000

# MAP CONFIGURATION
# Map respawn position, relative to the screen
MAP_RESPAWN_POSITION = [5.0, -131.0]

# Map position, relative to the screen
MAP_POSITION = MAP_RESPAWN_POSITION[:]

# Map sprite - TODO: change sprite, this is just a placeholder
MAP_SPRITE = "assets/sprites/map_01.png"

# STATS CONFIGURATION
# Stats file
STATS_FILE = "stats.json"

# Stats date format
STATS_DATE_FORMAT = "%c"

# SOUND CONFIGURATION
# Respawn sound for when player dies
RESPAWN_SOUND = "assets/sounds/mk64_wario05_wahhh.wav"

# Lap sound for when player finishes a lap
LAP_SOUND = "assets/sounds/mk64_wario_im_gonna_win.wav"

# Finish sound for when player finishes the map
FINISH_SOUND = "assets/sounds/mk64_announcer11_jp_congratiolation.wav"

# Powerup sound for credits button
POWERUP_SOUND = "assets/sounds/smb3_power-up.wav"

# CAMERA CONFIGURATION
# How close the player has to be to the edge of the screen for the screen to move
SCREEN_MOVE_OFFSET = 100

# EVENT CONFIGURATION
# Player gameover event
PLAYER_GAMEOVER_EVENT = pygame.event.custom_type()

# Player won event
PLAYER_WON_EVENT = pygame.event.custom_type()
ENEMY_WON_EVENT = pygame.event.custom_type()

# Game pause changed event
GAME_PAUSE_CHANGED = pygame.event.custom_type()

# RACE TRACK CONFIGURATION
# Set laps until finish
RACE_LAPS = 3

# Keep track of the current lap
RACE_CURRENT_LAP = 0

ENEMY_COUNT = 7

# Cheats
SKIP_TRACK_CHECK = False

# Map Loading
MAP_DIRECTORY = "assets/maps"

SUPER_MARIO_FONT = "assets/fonts/SuperMario256.ttf"
