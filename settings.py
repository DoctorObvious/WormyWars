import pygame
from pygame.locals import *

NUM_LIVES = 3
FPS = 8
GROW_BY = 4
DOUBLE_CLICK_TIME = 0.3         # in seconds
DYING_TIME_IN_SECS = 1.0                # in seconds

GRAPE_APPEAR_TIME = 20.         # in seconds
GRAPE_POINTS = 17
NUM_SECS_IN_INVISIBLE = 5.0     # in seconds (how long does it last)

BANANA_APPEAR_TIME = 10.        # in seconds
BANANA_POINTS = 10

NUM_SECS_IN_TURBO = 1.75        # how long does it last
NUM_TURBOS = 1

GOLDEN_APPEAR_TIME = 60.        # in seconds
GOLDEN_DISAPPEAR_TIME = 5.      # in seconds

BLUEBERRY_APPEAR_TIME = 18.     # in seconds
BLUEBERRY_DISAPPEAR_TIME = 5    # in seconds
BLUEBERRY_POINTS = 2
NUM_SECS_IN_FREEZE = 3.

LIME_APPEAR_TIME = 35.          # in seconds
LIME_DISAPPEAR_TIME = 10.       # in seconds
LIME_POINTS = 10
SWITCH_PAUSE_TIME = 1.5         # in seconds

BAD_APPLE_TIME = 16.            # how long before apple goes rotten. For 1 player
SHRINK_SEG_TIME = 1.            # number of seconds for a segment to disappear

WINDOWWIDTH = 900   # 640
WINDOWHEIGHT = 700  # 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

# Where to start plotting scores and such
INFO_POSITION = [{'x': WINDOWWIDTH - 110, 'y': 10},
                 {'x': 20,                'y': 10},
                 {'x': 20,                'y': WINDOWHEIGHT - 70},
                 {'x': WINDOWWIDTH - 120, 'y': WINDOWHEIGHT - 70}]

PORTAL_LENGTH = 3        # Must be odd
PORTALS_PER_SIDE = 2
LEFT_PORTAL_X = 2
RIGHT_PORTAL_X = CELLWIDTH-3
UP_PORTAL_Y = 2
DOWN_PORTAL_Y = CELLHEIGHT-3

SOUND_DIE = 'Taps_silly.wav'
SOUND_HAPPY = 'happy.wav'
SOUND_BEEP = 'quick_beep.wav'
SOUND_REVERSE = 'reverse.wav'
SOUND_LIFE = 'angelic.wav'
SOUND_PORTAL = 'port.wav'

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
BLUE      = (  0,   0, 255)
BLUE2     = ( 10,   0, 215)
LIGHTBLUE = (180, 180, 255)
DARKGREEN = (  0, 155,   0)
LIMEGREEN = ( 50, 205,  50)
DARKGRAY  = ( 40,  40,  40)
LIGHTGRAY = ( 80,  80,  80)
PURPLE    = (127,   0, 255)
YELLOW    = (255, 255,   0)
GOLD      = (255, 215,   0)
BGCOLOR = BLACK

TITLE_COLORS = [DARKGREEN, BLACK, RED, BLACK, LIGHTGRAY, BLACK, BLUE, BLACK]

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

DIRECTIONS  = [LEFT,  RIGHT, UP,    DOWN]
D_OPPOSITE  = [RIGHT, LEFT,  DOWN,  UP]
D_ALTERNATE = [DOWN,  UP,    LEFT,  RIGHT]
D_ALT_ALT   = [UP,    DOWN,  RIGHT, LEFT]

IX_L = DIRECTIONS.index(LEFT)
IX_R = DIRECTIONS.index(RIGHT)
IX_U = DIRECTIONS.index(UP)
IX_D = DIRECTIONS.index(DOWN)

# Worm controls
ALL_LEFTS = [K_LEFT, K_a, K_j, K_KP4]
ALL_RIGHTS = [K_RIGHT, K_d, K_l, K_KP6]
ALL_UPS = [K_UP, K_w, K_i, K_KP8]
ALL_DOWNS = [K_DOWN, K_s, K_k, K_KP5]
WORM_COLORS = [GREEN, BLUE, RED, LIGHTGRAY]

HEAD = 0  # syntactic sugar: index of the worm's head