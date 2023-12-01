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
CURRENT_FPS = 0

# WORLD CONFIGURATION
# World name
WORLD_NAME = "Rainbow Road"

# World description
WORLD_DESCRIPTION = "A colorful track in the sky."

# World position, relative to the screen
WORLD_POSITION = [0, 0]

# World background
WORLD_BACKGROUND = "assets/sprites/rainbow_road_map.png"

# World width = screen width
WORLD_WIDTH = SCREEN_WIDTH

# World height = screen height
WORLD_HEIGHT = SCREEN_HEIGHT

# PLAYER CONFIGURATION
# What's the player's name?
PLAYER_NAME = "Wario"

# What's the player like?
PLAYER_DESCRIPTION = "A fat, yellow, greedy, and smelly character."

# Player position, relative to the screen
PLAYER_POSITION = [SCREEN_CENTER_X, SCREEN_CENTER_Y]

# Player respawn position, relative to the screen
PLAYER_RESPAWN_POSITION = [127, 494]

# Player current position starts at the respawn position
PLAYER_CURRENT_POSITION = PLAYER_RESPAWN_POSITION[:]

# Player sprite
PLAYER_SPRITE = "assets/sprites/wario.png"

# Player sprite width
PLAYER_SPRITE_WIDTH = 32

# Player sprite height
PLAYER_SPRITE_HEIGHT = 32

# Player sprite scale
PLAYER_SPRITE_SCALE = 2

# Whether the player sprite should be horizontally flipped
PLAYER_SPRITE_HORIZONTAL_FLIP = False

# Whether the player sprite should be vertically flipped
PLAYER_SPRITE_VERTICAL_FLIP = False

# Player's current sprite frame
PLAYER_CURRENT_FRAME = 0

# Player's frame update interval
PLAYER_FRAME_UPDATE_INTERVAL = 5

# Player's max speed
PLAYER_MAX_SPEED = 500

# Player's min speed
PLAYER_MIN_SPEED = PLAYER_MAX_SPEED / 1.5

# Player's average speed
PLAYER_AVG_SPEED = (PLAYER_MIN_SPEED + PLAYER_MAX_SPEED) / 2

# Player's friction
PLAYER_FRICTION = 0.2

# Player's current speed
PLAYER_CURRENT_SPEED = 100

# MAP CONFIGURATION
# Map name is the same as the world name
MAP_NAME = WORLD_NAME

# Map description is the same as the world description
MAP_DESCRIPTION = WORLD_DESCRIPTION

# Map position, relative to the screen
MAP_POSITION = [5.0, -131.0]

# Map respawn position, relative to the screen
MAP_RESPAWN_POSITION = MAP_POSITION[:]

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

# Rainbow Road music for the map
MUSIC_RAINBOW_ROAD = "assets/sounds/music/Mario_Kart_64_Rainbow_Road.mp3"

# CAMERA CONFIGURATION
# How close the player has to be to the edge of the screen for the screen to move
SCREEN_MOVE_OFFSET = 100

# EVENT CONFIGURATION
# Player gameover event
PLAYER_GAMEOVER_EVENT = pygame.event.custom_type()

# Player won event
PLAYER_WON_EVENT = pygame.event.custom_type()

# Game pause changed event
GAME_PAUSE_CHANGED = pygame.event.custom_type()

# RACE TRACK CONFIGURATION
# Set laps until finish
RACE_LAPS = 2

# Keep track of the current lap
RACE_CURRENT_LAP = 0
