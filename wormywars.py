# Wormy Wars! (a Nibbles clone)
# Originally by Al Sweigart al@inventwithpython.com
# Modified and expanded by Mark and Lincoln Phillips
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random
import pygame
import sys
import time
from pygame.locals import *

NUM_LIVES = 3
FPS = 8
GROW_BY = 4
DOUBLE_CLICK_TIME = 0.3     # in seconds
DEATH_TIME = 1.0            # in seconds

GRAPE_APPEAR_TIME = 20      # in seconds
GRAPE_POINTS = 17
NUM_TICKS_IN_GRAPE = 25     # in ticks (how long does it last)

BANANA_APPEAR_TIME = 10     # in seconds
BANANA_POINTS = 10

NUM_TICKS_IN_TURBO = 14     # how long (in ticks) does it last
NUM_TURBOS = 1

GOLDEN_APPEAR_TIME = 30     # in seconds
GOLDEN_DISAPPEAR_TIME = 5   # in seconds

BLUEBERRY_APPEAR_TIME = 25     # in seconds
BLUEBERRY_DISAPPEAR_TIME = 5   # in seconds
BLUEBERRY_POINTS = 2
NUM_SECS_IN_FREEZE = 3
NUM_TICKS_IN_FREEZE = NUM_SECS_IN_FREEZE*FPS

LIME_APPEAR_TIME = 42       # in seconds
LIME_DISAPPEAR_TIME = 10    # in seconds
LIME_POINTS = 10

BAD_APPLE_TIME = 16         # how long before apple goes rotten. For 1 player
SHRINK_TIME    = 1          # number of seconds for a segment to disappear

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
DARKGREEN = (  0, 155,   0)
LIMEGREEN = ( 50, 205,  50)
DARKGRAY  = ( 40,  40,  40)
LIGHTGRAY = ( 80,  80,  80)
PURPLE    = (127,   0, 255)
YELLOW    = (255, 255,   0)
GOLD      = (255, 215,   0)
BGCOLOR = BLACK

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

GLOBAL_TIME = 0.0

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    pygame.mixer.init(frequency=44100, channels=2)
    s = pygame.mixer.Sound(SOUND_HAPPY)
    s.play()
    
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy Wars!')

    key = showStartScreen()
            
    while True:
        num_players = 1
        num_robots = 0
        if (key == K_1):
            num_players = 1
        elif (key == K_2):
            num_players = 2
        elif (key == K_3):
            num_players = 3
        elif (key == K_4):
            num_players = 4
        elif (key == K_F1):
            num_players = 1
            num_robots = 1
        elif (key == K_F2):
            num_players = 2
            num_robots = 1
        elif (key == K_F3):
            num_players = 3
            num_robots = 1
        elif (key == K_F4):
            num_players = 4
            num_robots = 1
        elif (key == K_F6):
            num_players = 4
            num_robots = 2
        elif (key == K_r):
            num_players = 4
            num_robots = 4
        winning_player = runGame(num_players, num_robots)
        key = showGameOverScreen(winning_player, WORM_COLORS[winning_player[0]-1])

def wormBirth(player_number, existCoords=[]):
   
    startx = 5
    # starty = 5 + 7*player_number
    for y_try in range(4, 26):
        starty = y_try + 7*player_number
        starty = ((starty-4) % 22) + 4
        wormCoords = wormStartingCoords(startx, starty)
        if coordsSafe(wormCoords, existCoords):
            break
        
    direction = RIGHT

    is_alive = True
    num_to_grow = 0
    num_turbos = NUM_TURBOS
    turbo_ticks = 0
    freeze_ticks = 0
    invisible_ticks = 0
    is_shrinking = False
    
    return wormCoords, direction, is_alive, num_to_grow, num_turbos, turbo_ticks, invisible_ticks, freeze_ticks, is_shrinking

def wormStartingCoords(startx, starty):
    return [{'x': startx,     'y': starty},
            {'x': startx - 1, 'y': starty},
            {'x': startx - 2, 'y': starty}]

    
def getPortalCoords():
    # Do sides
    leftPortalCoords = [0] * PORTALS_PER_SIDE
    leftPortalNames = ['left'] * PORTALS_PER_SIDE
    rightPortalCoords =  [0] * PORTALS_PER_SIDE
    rightPortalNames = ['right'] * PORTALS_PER_SIDE
    
    portalIncr = int(CELLHEIGHT/(PORTALS_PER_SIDE+1))
    portalOffset = (PORTAL_LENGTH-1)/2
    for hh in range(PORTALS_PER_SIDE):
        leftPortalCoords[hh] = [0] * PORTAL_LENGTH
        rightPortalCoords[hh] = [0] * PORTAL_LENGTH

        for xx in range(PORTAL_LENGTH):
            leftPortalCoords[hh][xx] = {'x': LEFT_PORTAL_X, 'y': (hh+1)*portalIncr-portalOffset+xx}
            rightPortalCoords[hh][xx] = {'x': RIGHT_PORTAL_X, 'y': (hh+1)*portalIncr-portalOffset+xx}
    
    upPortalCoords = [0] * PORTALS_PER_SIDE
    upPortalNames = ['up'] * PORTALS_PER_SIDE
    downPortalCoords =  [0] * PORTALS_PER_SIDE
    downPortalNames = ['down'] * PORTALS_PER_SIDE
    
    portalIncr = int(CELLWIDTH/(PORTALS_PER_SIDE+1))
    portalOffset = (PORTAL_LENGTH-1)/2
    for hh in range(PORTALS_PER_SIDE):
        upPortalCoords[hh] = [0] * PORTAL_LENGTH
        downPortalCoords[hh] = [0] * PORTAL_LENGTH

        for xx in range(PORTAL_LENGTH):
            upPortalCoords[hh][xx] = {'y': UP_PORTAL_Y, 'x': (hh+1)*portalIncr-portalOffset+xx}
            downPortalCoords[hh][xx] = {'y': DOWN_PORTAL_Y, 'x': (hh+1)*portalIncr-portalOffset+xx}

    portalCoords = leftPortalCoords + rightPortalCoords + upPortalCoords + downPortalCoords
    portalNames = leftPortalNames + rightPortalNames + upPortalNames + downPortalNames
    return portalCoords, portalNames
    

def runGame(num_players, num_robots=0):
    # Create worms
    allWormsCoords = []
    allStartX = []
    allStartY = []
    directions =[]
    sound_happy = pygame.mixer.Sound(SOUND_HAPPY)
    sound_happy.set_volume(0.5)
    sound_die = pygame.mixer.Sound(SOUND_DIE)
    sound_beep = pygame.mixer.Sound(SOUND_BEEP)
    sound_portal = pygame.mixer.Sound(SOUND_PORTAL)
    sound_life = pygame.mixer.Sound(SOUND_LIFE)
    sound_reverse = pygame.mixer.Sound(SOUND_REVERSE)

    do_switcheroo = False
    is_alive = [True] * num_players
    is_visible = [True] * num_players
    is_shrinking = [False] * num_players
    is_robot = [False] * num_players
    num_to_grow = [0] * num_players
    num_turbos = [NUM_TURBOS] * num_players
    invisible_ticks = [0] * num_players
    turbo_ticks = [0] * num_players
    freeze_ticks = [0] * num_players
    num_lives = [NUM_LIVES] * num_players
    scores = [0] * num_players
    
    for ii in range(num_players):
        wormCoords, direction, is_alive[ii], num_to_grow[ii], num_turbos[ii], \
                    turbo_ticks[ii], invisible_ticks[ii], freeze_ticks[ii], is_shrinking[ii] =\
                    wormBirth(ii)
        
        allWormsCoords.insert(0, wormCoords)
        directions.insert(0, direction)

        if (ii >= num_players-num_robots):
            is_robot[ii] = True
        
    # Get the portal coordinates
    portalCoords, portalNames = getPortalCoords()

    existingCoords = makeCoordsList(portalCoords) + makeCoordsList(allWormsCoords)
    
    # Start the apple in a random place.    
    apple = getSafeFruitLocation(existingCoords)
    apple_is_bad = False
    grape = []
    banana = []
    golden_apple = []
    blueberry = []
    lime = []

    frame_count = 0.0

    # How long since the LAST appearance of a fruit
    last_grape_time = 0
    last_banana_time = 0
    last_golden_time = 0
    last_blueberry_time = 0
    last_lime_time = 0
    last_shrink_time = [0]*num_players
    
    last_press_time = [0]*num_players
    last_key_press = [0]*num_players
    
    # Initialize time since a fruit has appeared
    apple_time = 0
    golden_time = -1000
    blueberry_time = -1000
    lime_time = -1000


    while True: # main game loop
        frame_count += 1.0
        global GLOBAL_TIME
        GLOBAL_TIME = float(frame_count)/FPS
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()

        keys_processed = [0] * num_players
        worm_died = [False] * num_players

        # Handle Robots
        for ii in range(num_players):
            if is_robot[ii] and is_alive[ii]:
                #visibleWormCoords = allVisibleWormCoords(allWormsCoords, is_alive, is_visible)
                #visibleCoords = makeCoordsList(portalCoords) + visibleWormCoords

                visibleWorms = allVisibleWormNumbers(is_alive, is_visible)
                otherWormCoords = []
                otherWormDirections = []
                # TODO: Cleanup!
                for mm in visibleWorms:
                    otherWormCoords.append(allWormsCoords[mm])
                    otherWormDirections.append(directions[mm])

                visibleCoords = makeCoordsList(portalCoords) + makeCoordsList(otherWormCoords)
                fruits = [banana, grape, lime, blueberry, golden_apple]

                if ii%2 == 0:
                    directions[ii] = robot_link(ii, allWormsCoords, directions, apple, visibleCoords, is_alive, fruits)
                else:
                    directions[ii] = robot_daddy(ii, allWormsCoords, directions, apple, visibleCoords, is_alive, fruits)
               
        for event in pygame.event.get(): # event handling loop

            if event.type == QUIT:
                 terminate()

            # See how keypresses affect direction for each worm!
            for ii in range(num_players):
                 direction = directions[ii]
                 new_direction = direction

                 if event.type == KEYDOWN:
                     key_press = None
                     if (event.key == ALL_LEFTS[ii]):
                         key_press = LEFT
                         if direction != RIGHT:
                             new_direction = LEFT
                     elif (event.key == ALL_RIGHTS[ii]):
                         key_press = RIGHT
                         if direction != LEFT:
                             new_direction = RIGHT
                     elif (event.key == ALL_UPS[ii]):
                         key_press = UP
                         if direction != DOWN:
                             new_direction = UP
                     elif (event.key == ALL_DOWNS[ii]):
                         key_press = DOWN
                         if direction != UP:
                             new_direction = DOWN
                     elif event.key == K_ESCAPE:
                         terminate()
                     elif event.key == K_F5:
                         is_alive = [False] * num_players

                     if key_press == last_key_press[ii] and GLOBAL_TIME - last_press_time[ii] < DOUBLE_CLICK_TIME:
                         # Double click in same direction for turbo
                         if num_turbos[ii] > 0:
                             turbo_ticks[ii] += NUM_TICKS_IN_TURBO
                             num_turbos[ii] -= 1

                     # Only process one direction key per worm per drawing cycle.
                     # Save others for next time.
                     if key_press is not None:
                         if new_direction != direction:
                             if keys_processed[ii] > 0:
                                 pygame.event.post(event)
                             else:
                                 keys_processed[ii] += 1
                                 direction = new_direction
                                 # sound_beep.play()
                                 last_key_press[ii] = key_press
                                 last_press_time[ii] = GLOBAL_TIME
                         else:
                             last_key_press[ii] = key_press
                             last_press_time[ii] = GLOBAL_TIME
                         
                     directions[ii]=direction

        # Do for each worm!
        for ii in range(num_players):
            wormCoords = allWormsCoords[ii]
            direction = directions[ii]
            
            if is_alive[ii]:

                num_moves = 1
                if turbo_ticks[ii] > 0:
                    num_moves = 2
                    turbo_ticks[ii] -= 1

                if invisible_ticks[ii] > 0:
                    invisible_ticks[ii] -= 1

                if freeze_ticks[ii] > 0:
                    freeze_ticks[ii] -= 1
                    continue

                for kk in range(num_moves):
                    if worm_died[ii]:  # In case worm died in previous (turbo) move.
                        continue
                    
                    # move the worm by adding a segment in the direction it is moving
                    newHead = getNewHead(direction, wormCoords)
            
                    # Grow new head
                    wormCoords.insert(0, newHead)

                    # check if the worm has hit the edge
                    if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
                        worm_died[ii] = True

                    # check if the worm has hit its body
                    for wormBody in wormCoords[1:]:
                        if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                            worm_died[ii] = True

                    # check if the worm has hit a portal
                    hit_portal = False
                    for portalCoord in portalCoords:
                        for coord in portalCoord:
                            if wormCoords[HEAD]['x'] == coord['x'] and wormCoords[HEAD]['y'] == coord['y']:
                                sound_portal.play()
                                hit_portal = True
                                
                    # teleport logic:  Should update to use x AND y checks and/or use the portal "name".
                    if hit_portal == True:
                        if wormCoords[HEAD]['x'] == LEFT_PORTAL_X:
                            if direction == UP or direction == DOWN:
                                # worm_died[ii] = True
                                wormCoords[HEAD] = moveWormSameSidePortal(wormCoords[HEAD], portalCoords, direction)
                            elif direction == LEFT:
                                wormCoords[HEAD]['x'] = RIGHT_PORTAL_X - 1
                            else:
                                wormCoords[HEAD]['x'] = RIGHT_PORTAL_X + 1
                                
                        elif wormCoords[HEAD]['x'] == RIGHT_PORTAL_X:
                            if direction == UP or direction == DOWN:
                                # worm_died[ii] = True
                                wormCoords[HEAD] = moveWormSameSidePortal(wormCoords[HEAD], portalCoords, direction)
                            elif direction == LEFT:
                                wormCoords[HEAD]['x'] = LEFT_PORTAL_X - 1
                            else:
                                wormCoords[HEAD]['x'] = LEFT_PORTAL_X + 1
                                
                        elif wormCoords[HEAD]['y'] == UP_PORTAL_Y:
                            if direction == LEFT or direction == RIGHT:
                                # worm_died[ii] = True
                                wormCoords[HEAD] = moveWormSameSidePortal(wormCoords[HEAD], portalCoords, direction)                                
                            elif direction == DOWN:
                                wormCoords[HEAD]['y'] = DOWN_PORTAL_Y + 1
                            else:
                                wormCoords[HEAD]['y'] = DOWN_PORTAL_Y - 1
                                
                        elif wormCoords[HEAD]['y'] == DOWN_PORTAL_Y:
                            if direction == LEFT or direction == RIGHT:
                                #worm_died[ii] = True
                                wormCoords[HEAD] = moveWormSameSidePortal(wormCoords[HEAD], portalCoords, direction)                                
                            elif direction == DOWN:
                                wormCoords[HEAD]['y'] = UP_PORTAL_Y + 1
                            else:
                                wormCoords[HEAD]['y'] = UP_PORTAL_Y - 1                           

                    # check if the worm has hit another worm
                    for jj in range(num_players):
                        # make sure it is not the same worm
                        if jj == ii:
                            continue
                        
                        # make sure the worm isn't dead
                        if not is_alive[jj] or worm_died[jj]:
                            continue

                        # Actual checking for collision
                        kk = 0
                        for wormBlock in allWormsCoords[jj]:
                            if wormBlock['x'] == wormCoords[HEAD]['x'] and wormBlock['y'] == wormCoords[HEAD]['y']:
                                worm_died[ii] = True      # This worm dies
                                drawWorm(allWormsCoords[ii], WORM_COLORS[ii], is_robot[ii], is_shrinking[ii], turbo_ticks[ii]>0)
                                if kk == 0:               # This is the other head block 
                                    worm_died[jj] = True  # The other worm dies
                            kk += 1

                    allWormsCoords[ii] = wormCoords
                    existingCoords = makeCoordsList(portalCoords) + makeCoordsList(allWormsCoords)

                    # check if worm has eaten an apple
                    if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
                        apple = getSafeFruitLocation(existingCoords) # set a new apple somewhere
                        apple_time = frame_count/FPS
                        sound_happy.play()
                        if apple_is_bad:
                            num_to_grow[ii] += 0
                            scores[ii] += GROW_BY
                            is_shrinking[ii] = True
                            last_shrink_time[ii] = GLOBAL_TIME
                        else:
                            num_to_grow[ii] += GROW_BY
                            num_turbos[ii] += 1
                            scores[ii] += GROW_BY
                            is_shrinking[ii] = False

                    if len(golden_apple)>0:
                        # check if a worm has eaten a golden_apple
                        if wormCoords[HEAD]['x'] == golden_apple['x'] and wormCoords[HEAD]['y'] == golden_apple['y']:
                            last_golden_time = GLOBAL_TIME
                            sound_life.play()
                            golden_apple = []
                            num_lives[ii] += 1

                    if len(blueberry)>0:
                        # check if a worm has eaten a blueberry
                        if wormCoords[HEAD]['x'] == blueberry['x'] and wormCoords[HEAD]['y'] == blueberry['y']:
                            last_blueberry_time = GLOBAL_TIME
                            sound_happy.play()
                            blueberry = []
                            for kk in range(num_players):
                                if kk != ii:
                                    freeze_ticks[kk] += NUM_TICKS_IN_FREEZE
                                    
                    if len(grape)>0:
                        # check if a worm has eaten a grape
                        if wormCoords[HEAD]['x'] == grape['x'] and wormCoords[HEAD]['y'] == grape['y']:
                            last_grape_time = GLOBAL_TIME
                            sound_happy.play()
                            invisible_ticks[ii] += NUM_TICKS_IN_GRAPE
                            scores[ii] += GRAPE_POINTS
                            grape = []

                    if len(banana)>0:
                        # check if a worm has eaten a banana, and flip the coordinates
                        if wormCoords[HEAD]['x'] == banana['x'] and wormCoords[HEAD]['y'] == banana['y']:
                            last_banana_time = GLOBAL_TIME
                            sound_reverse.play()
                            scores[ii] += BANANA_POINTS
                            banana = []

                            tail_direction = getTailDirection(wormCoords)
                            directions[ii] = D_OPPOSITE[DIRECTIONS.index(tail_direction)]
                            direction = directions[ii]
                            wormCoords.reverse()
                            
                    if num_to_grow[ii] > 0:
                        # Don't delete the tail, grow instead!
                        num_to_grow[ii] -= 1
                    else:
                        del wormCoords[-1] # remove worm's tail segment

                    if is_shrinking[ii] and (GLOBAL_TIME - last_shrink_time[ii] > SHRINK_TIME):
                        last_shrink_time[ii] = GLOBAL_TIME
                        if len(wormCoords) == 1:
                            worm_died[ii] = True
                            is_shrinking[ii] = False
                            turbo_ticks[ii] = 0

                        del wormCoords[-1] # remove worm's tail segment
                            
                    # Do lime switch after length is adjusted
                    if len(lime) > 0 and not worm_died[ii]:
                        # check if a worm has eaten a lime
                        if wormCoords[HEAD]['x'] == lime['x'] and wormCoords[HEAD]['y'] == lime['y']:
                            last_lime_time = frame_count/FPS
                            sound_happy.play()
                            scores[ii] += LIME_POINTS
                            lime = []
                            do_switcheroo = True
                            wormCoords = allWormsCoords[ii]
                            direction = directions[ii]
                            for jj in range(num_players):
                                removeWormEvents(jj)

                allWormsCoords[ii] = wormCoords

        # Was a switcheroo triggered?
        if do_switcheroo:
            allWormsCoords, directions = switcheroo(allWormsCoords, directions, is_alive)
            do_switcheroo = False

        # ------------- Time check ----------------

        # Has the apple gone bad?
        bad_apple_time = max(7, BAD_APPLE_TIME - sum(is_alive)*2)
        if (GLOBAL_TIME - apple_time > bad_apple_time):
            apple_is_bad = True
        else:
            apple_is_bad = False    

        # Is it time to make a golden_apple?
        if len(golden_apple)==0 and (GLOBAL_TIME - last_golden_time > GOLDEN_APPEAR_TIME):
            # Make a golden_apple!
            golden_apple = getSafeFruitLocation(existingCoords)
            golden_time = GLOBAL_TIME
            last_golden_time = golden_time
        elif len(golden_apple)>0 and (GLOBAL_TIME - golden_time > GOLDEN_DISAPPEAR_TIME):
            # It is time for the golden_apple to disappear
            golden_apple = []

        # Is it time to make a blueberry?
        if len(blueberry)==0 and (GLOBAL_TIME - last_blueberry_time > BLUEBERRY_APPEAR_TIME):
            # Make a blueberry!
            blueberry = getSafeFruitLocation(existingCoords)
            blueberry_time = GLOBAL_TIME
            last_blueberry_time = blueberry_time
        elif len(blueberry)>0 and (GLOBAL_TIME - blueberry_time > BLUEBERRY_DISAPPEAR_TIME):
            # It is time for the blueberry to disappear
            blueberry = []

        # Is it time to make a lime?
        if len(lime)==0 and (GLOBAL_TIME - last_lime_time > LIME_APPEAR_TIME) and sum(is_alive)>1:
            # Make a lime!
            lime = getSafeFruitLocation(existingCoords)
            lime_time = GLOBAL_TIME
            last_lime_time = lime_time
        elif (len(lime)>0 and (GLOBAL_TIME - lime_time > LIME_DISAPPEAR_TIME)) or sum(is_alive)<2:
            # It is time for the lime to disappear
            lime = []
            
        # Is it time to make a grape?
        GLOBAL_TIME = frame_count/FPS
        if len(grape)==0 and (GLOBAL_TIME-last_grape_time > GRAPE_APPEAR_TIME):
            # Make a grape!
            grape = getSafeFruitLocation(existingCoords)

        # Is it time to make a banana?
        if len(banana)==0 and (GLOBAL_TIME-last_banana_time > BANANA_APPEAR_TIME):
            # Make a banana!
            banana = getSafeFruitLocation(existingCoords)

        existingCoords = makeCoordsList(portalCoords) + makeCoordsList(allWormsCoords)        

        # ----------------  Draw everything! ---------------------------
        for ii in range(num_players):
            drawScore(ii, scores[ii], WORM_COLORS[ii])
            drawTurbos(ii, num_turbos[ii], WORM_COLORS[ii])
            drawLives(ii, num_lives[ii], WORM_COLORS[ii])

            # If alive and visible...
            if is_alive[ii] and invisible_ticks[ii]==0:
                drawWorm(allWormsCoords[ii], WORM_COLORS[ii], is_robot[ii], is_shrinking[ii], turbo_ticks[ii]>0)

        drawPortals(portalCoords)

        drawFruit(apple, RED, is_bad=apple_is_bad)
        drawFruit(golden_apple, GOLD, is_shiny=True)
        drawFruit(grape, PURPLE)
        drawFruit(banana, YELLOW)
        drawFruit(blueberry, BLUE2)
        drawFruit(lime, LIMEGREEN)
        
        if any(worm_died):
            start_time = time.time()
            while (time.time() - start_time < DEATH_TIME):
                for ii in range(num_players):
                    if worm_died[ii]:
                        drawWorm(allWormsCoords[ii], BLACK, is_robot[ii], is_shrinking[ii], turbo_ticks[ii]>0)
                pygame.display.update()
                FPSCLOCK.tick(100)
                for ii in range(num_players):
                    if worm_died[ii]:
                        drawWorm(allWormsCoords[ii], WORM_COLORS[ii], is_robot[ii], is_shrinking[ii], turbo_ticks[ii]>0)
                pygame.display.update()
                FPSCLOCK.tick(100)

        for ii in range(num_players):
            if worm_died[ii]:
                if num_lives[ii]>1:
                    allWormsCoords[ii], directions[ii], is_alive[ii], num_to_grow[ii], num_turbos[ii], turbo_ticks[ii], \
                                        invisible_ticks[ii], freeze_ticks[ii], is_shrinking[ii] = \
                                wormBirth(ii, existingCoords)
                else:
                    is_alive[ii] = False
                    drawWorm(allWormsCoords[ii], WORM_COLORS[ii], is_robot[ii], is_shrinking[ii], turbo_ticks[ii]>0)
                    sound_die.play()
                    allWormsCoords[ii] = []
                num_lives[ii] -= 1
                removeWormEvents(ii)

        # Update coordinates where things are
        existingCoords = makeCoordsList(portalCoords) + makeCoordsList(allWormsCoords)        

        
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        # sound_beep.play()

        # Check to see if the game is over
        if not any(is_alive):
            max_score = max(scores)
            winning_player = []
            for ii in range(num_players):
                if scores[ii] == max_score:
                    winning_player.append(ii+1)
            
            return winning_player  # game over

def robot_link(worm_num, allWormCoords, current_directions, apple, existingCoords, is_alive, fruits):

    wormCoords = allWormCoords[worm_num]
    current_direction = current_directions[worm_num]
    x_dist = apple['x'] - wormCoords[0]['x']
    y_dist = apple['y'] - wormCoords[0]['y']

    # Give points to the best directions [LEFT, RIGHT, UP, DOWN]
    goodness = [0, 0, 0, 0]

    # Give a very slight preference to the current direction, all else being equal
    goodness[DIRECTIONS.index(current_direction)] += 4

    # Prefer the routes to the apple
    goodness = preferDirectionToFruit(wormCoords, apple, goodness)

    # Can't go the opposite of the current direction
    # print "Current direction: {}".format(current_direction)
    # print "DIRECTIONS.index(current_direction): {}".format(DIRECTIONS.index(current_direction))
    goodness[D_OPPOSITE.index(current_direction)] = -1000  # Impossible choice

    # Check each direction for collision with other objects
    for jj in range(4):
        newHead = getNewHead(DIRECTIONS[jj], wormCoords)
        found_hit = False
        
        # check if the worm will hit its body, other worm bodies, or portals
        for coords in existingCoords:
            if coords['x'] == newHead['x'] and coords['y'] == newHead['y']:
                found_hit = True
                goodness[jj] -= 90   # A hit is not a good choice.

        # check if the worm will hit the edge
        if not found_hit:
            if newHead['x'] == -1 or newHead['x'] == CELLWIDTH or newHead['y'] == -1 or newHead['y'] == CELLHEIGHT:
                found_hit = True
                goodness[jj] -= 90   # A hit is not a good choice.

        # check if the worm is going to hit where it looks like the other worm is going
        if not found_hit:
            for kk in range(len(allWormCoords)):
                if kk == worm_num:
                    continue   # Don't check against the same worm
                if not is_alive[kk]:
                    continue   # Ignore dead worms
                otherNewHead = getNewHead(current_directions[kk], allWormCoords[kk])
                if newHead['x'] == otherNewHead['x'] and newHead['y'] == otherNewHead['y']:
                    found_hit = True
                    goodness[jj] -= 10   # Avoid were other worm is headed

    # Find the "most goodness" direction
    new_direction = DIRECTIONS[goodness.index(max(goodness))]    
    # print "new_direction: {}".format(new_direction)
    return new_direction

def robot_daddy(worm_num, allWormCoords, current_directions, apple, existingCoords, is_alive, fruits):

    wormCoords = allWormCoords[worm_num]
    current_direction = current_directions[worm_num]

    # Give points to the best directions [LEFT, RIGHT, UP, DOWN]
    goodness = [0, 0, 0, 0]

    # Give a very slight preference to the current direction, all else being equal
    goodness[DIRECTIONS.index(current_direction)] += 4

    # Find the closest fruit.
    appleDistance = totalDistanceToFruit(wormCoords, apple)
    existingFruits = findExistingFruits(fruits)
    if len(existingFruits) > 0:
        closeFruit, fruitDistance = closestFruit(wormCoords, existingFruits)
        
    if len(existingFruits) > 0 and fruitDistance < (appleDistance - 4):
        goodness = preferDirectionToFruit(wormCoords, closeFruit, goodness, 1.0)
    else:
        goodness = preferDirectionToFruit(wormCoords, apple, goodness, 1.0)

    # Can't go the opposite of the current direction
    # print "Current direction: {}".format(current_direction)
    # print "DIRECTIONS.index(current_direction): {}".format(DIRECTIONS.index(current_direction))
    goodness[D_OPPOSITE.index(current_direction)] = -1000.0  # Impossible choice

    # Check each direction for collision with other objects
    for jj in range(4):
        newHead = getNewHead(DIRECTIONS[jj], wormCoords)
        found_hit = False

##        if isFruitInThisDirection(d[jj], wormCoords, fruits):
##            goodness[jj] += 100.0
        
        # check if the worm will hit its body, other worm bodies, or portals
        for coords in existingCoords:
            if coords['x'] == newHead['x'] and coords['y'] == newHead['y']:
                found_hit = True
                goodness[jj] -= 90.0   # A hit is not a good choice.

        # check if the worm will hit the edge
        if not found_hit:
            if newHead['x'] == -1 or newHead['x'] == CELLWIDTH or newHead['y'] == -1 or newHead['y'] == CELLHEIGHT:
                found_hit = True
                goodness[jj] -= 90.0   # A hit is not a good choice.

        # check if the worm is going to hit where it looks like the other worm is going
        if not found_hit:
            for kk in range(len(allWormCoords)):
                if kk == worm_num:
                    continue   # Don't check against the same worm          
                
                if not is_alive[kk]:
                    continue   # Ignore dead worms
                
                otherNewHead = getNewHead(current_directions[kk], allWormCoords[kk])
                if newHead['x'] == otherNewHead['x'] and newHead['y'] == otherNewHead['y']:
                    found_hit = True
                    goodness[jj] -= 10.0   # Avoid were other worm is headed

                # And check where other worm MIGHT go
                if totalDistance(newHead, allWormCoords[kk][HEAD]) == 1:
                    goodness[jj] -= 5.0   # Avoid where other worm is might be headed

        # Check if it is a single lane road
        if not found_hit:
            # See if something is occupying the "sides" of the new direction
            # That would be the alternate direction from the new head and the opposite of the alternate
            sideCheck1 = getNewHead(D_ALTERNATE[jj], [newHead])
            sideCheck2 = getNewHead(D_ALT_ALT[jj], [newHead])
            if sideCheck1 in existingCoords and sideCheck2 in existingCoords:
                # print "tunnel warning"
                goodness[jj] -= 20.0
                

    # Find the "most goodness" direction
    new_direction = DIRECTIONS[goodness.index(max(goodness))]    

    return new_direction


def preferDirectionToFruit(wormCoords, fruit, goodness, scale=1.0):
    x_dist, y_dist = xyDistanceToFruit(wormCoords, fruit)
    preferred_x_ix = None
    preferred_y_ix = None
    if x_dist > 0:
        goodness[IX_R] += 5.0 * scale
        preferred_x_ix = IX_R
    elif x_dist < 0:
        goodness[IX_L] += 5.0 * scale
        preferred_x_ix = IX_L
        
    if y_dist > 0:
        goodness[IX_D] += 5.0 * scale
        preferred_y_ix = IX_D
    elif y_dist < 0:
        goodness[IX_U] += 5.0 * scale
        preferred_y_ix = IX_U

    # Add some goodness to the direction most in the direction of the target.
    # Add a little goodness to the alternate directions in case the preferred direction isn't allowed
    if abs(x_dist) > abs(y_dist):
        # Some diagonal
        # goodness[preferred_x_ix] += 10 * (1 - int(y_dist/x_dist))
        # More straight
        goodness[preferred_x_ix] += 5.0 * scale
        goodness[DIRECTIONS.index(D_ALTERNATE[preferred_x_ix])] += 4.0 * scale

    else:
        # Some diagonal
        # goodness[preferred_y_ix] += 10 * (1 - int(x_dist/y_dist))
        # More straight
        goodness[preferred_y_ix] += 5.0 * scale
        goodness[DIRECTIONS.index(D_ALTERNATE[preferred_y_ix])] += 4.0 * scale

    return goodness

def findExistingFruits(fruits):
    existingFruits = []
    for fruit in fruits:
        if len(fruit) > 0:
            existingFruits.append(fruit)

    return existingFruits


def closestFruit(wormCoords, fruits):
    distances = [totalDistanceToFruit(wormCoords, fruit) for fruit in fruits]
    min_index = distances.index(min(distances))
    return (fruits[min_index], distances[min_index])


def xyDistanceToFruit(wormCoords, fruit):
    x_dist = fruit['x'] - wormCoords[0]['x']
    y_dist = fruit['y'] - wormCoords[0]['y']
    return (x_dist, y_dist)


def totalDistanceToFruit(wormCoords, fruit):
    x_dist, y_dist = xyDistanceToFruit(wormCoords, fruit)
    total_dist = abs(x_dist) + abs(y_dist)
    return total_dist


def totalDistance(coord1, coord2):
    x_dist = coord1['x'] - coord2['x']
    y_dist = coord1['y'] - coord2['y']
    total_dist = abs(x_dist) + abs(y_dist)
    return total_dist


def getNewHead(direction, wormCoords):
    
    if direction == UP:
        newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
    elif direction == DOWN:
        newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
    elif direction == LEFT:
        newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
    elif direction == RIGHT:
        newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}

    return newHead


def moveWormSameSidePortal(wormHead, portalCoords, direction):
    # Find which portal we're in
    for portal in portalCoords:
        if wormHead in portal:
            foundPortal = portal

    # Is it a vertical or horizontal portal?
    if foundPortal[0]['x'] == foundPortal[1]['x']:
        use_key = 'x'
        other_key = 'y'
    else:
        use_key = 'y'
        other_key = 'x'
        
    # Are we going in the min or max end?
    min_of_found = findMinCoord(foundPortal, other_key)
    if wormHead[other_key] == min_of_found:
        entered_min = True
    else:
        entered_min = False

    # Find the other one on the same side
    for portal in portalCoords:
        if portal[0][use_key] == foundPortal[0][use_key] and portal[0][other_key] != foundPortal[0][other_key]:
            otherPortal = portal
    
    # Figure out the correct end of the portal to exit
    if entered_min:
        useVal = findMaxCoord(otherPortal, other_key)
        useVal += 1   # Go beyond end of portal
    else:
        useVal = findMinCoord(otherPortal, other_key)
        useVal -= 1   # Go beyond end of portal

    newHead = dict()
    newHead[use_key] = foundPortal[0][use_key]
    newHead[other_key] = useVal

    return newHead


def findMinCoord(coords, key):
    useVal = max(WINDOWWIDTH, WINDOWHEIGHT)
    for coord in coords:
        if coord[key] < useVal:
            useVal = coord[key]

    return useVal

def findMaxCoord(coords, key):
    useVal = 0
    for coord in coords:
        if coord[key] > useVal:
            useVal = coord[key]

    return useVal

def isFruitInThisDirection(direction, wormCoords, fruits):
    newHead = getNewHead(direction, wormCoords)
    for fruit in fruits:
        if len(fruit)>0:
            if newHead['x'] == fruit['x'] and newHead['y'] == fruit['y']:
                return True

    return False

def coordsSafe(newCoords, existingCoords):
    for newCoord in newCoords:
        for existingCoord in existingCoords:
            if newCoord['x'] == existingCoord['x'] and newCoord['y'] == existingCoord['y']:
                return False
    
    return True


def getSafeFruitLocation(existingCoords):
    fruit = getRandomLocation() # set a new apple somewhere
    while (not coordsSafe([fruit], existingCoords)):
        fruit = getRandomLocation() # set a new apple somewhere
        
    return fruit

def getTailDirection(wormCoords):
    last = len(wormCoords)-1
    last_m1 = last - 1

    if wormCoords[last]['y'] == wormCoords[last_m1]['y']:
        if wormCoords[last]['x'] > wormCoords[last_m1]['x']:
            direction = LEFT
        else:
            direction = RIGHT
    else:
        if wormCoords[last]['y'] > wormCoords[last_m1]['y']:
            direction = UP
        else:
            direction = DOWN

    return direction            

def removeWormEvents(wormNumber):
    for event in pygame.event.get(): # event handling loop
        if event.type == KEYDOWN:
            if (event.key == ALL_LEFTS[wormNumber]):
                continue
            elif (event.key == ALL_RIGHTS[wormNumber]):
                continue
            elif (event.key == ALL_UPS[wormNumber]):
                continue
            elif (event.key == ALL_DOWNS[wormNumber]):
                continue
        
        pygame.event.post(event)

def switcheroo(allWormsCoords, directions, is_alive):
    num_players = len(directions)
    newWormsCoords = list(allWormsCoords)
    newDirections = list(directions)
    
    for ii in range(num_players):           
        for jj in range(1, num_players):
            new_index = (ii+jj) % num_players
            if is_alive[new_index]:
                break
        
        newWormsCoords[ii] = allWormsCoords[new_index]
        newDirections[ii] = directions[new_index]

    return newWormsCoords, newDirections

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press # of players (1-4) to play.', True, LIGHTGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 300, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

def makeCoordsList(coords):
    coordList = []
    for coord in coords:
        coordList = coordList + coord
    return coordList

def allVisibleWormCoords(allWormsCoords, is_alive, is_visible):
    coordList = []
    for ii in range(len(is_alive)):
        if is_alive[ii] and is_visible[ii]:
            coord = allWormsCoords[ii]      
            coordList = coordList + coord
        
    return coordList

def allVisibleWormNumbers(is_alive, is_visible):
    nums = []
    for ii in range(len(is_alive)):
        if is_alive[ii] and is_visible[ii]:
            nums.append(ii)
        
    return nums

# KRT 14/06/2012 rewrite event detection to deal with mouse use
def checkForKeyPress():
    for event in pygame.event.get():
        if event.type == QUIT:      #event is quit 
            terminate()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:   #event is escape key
                terminate()
            else:
                return event.key   #key found return with it
    # no quit or key events in queue so return None    
    return None

    
def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Wormy Wars!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Wormy Wars!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    
    #KRT 14/06/2012 rewrite event detection to deal with mouse use
    pygame.event.get()  #clear out event queue
    
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()
        #KRT 14/06/2012 rewrite event detection to deal with mouse use
        key = checkForKeyPress()
        if key:
            return key
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen(winning_player, color):
    gameOverFont = pygame.font.Font('freesansbold.ttf', 60)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)

    winning_string = 'Player {} Wins!'.format(winning_player)
    
    playerSurf = gameOverFont.render(winning_string, True, color)
    
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    playerRect = playerSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)
    playerRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 100 + overRect.height)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    DISPLAYSURF.blit(playerSurf, playerRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
#KRT 14/06/2012 rewrite event detection to deal with mouse use
    pygame.event.get()  #clear out event queue
    while True:
        key = checkForKeyPress()
        if key:
            return key
#KRT 12/06/2012 reduce processor loading in gameover screen.
        pygame.time.wait(100)

def drawScore(player_number, score, color):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, color)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (INFO_POSITION[player_number]['x'], INFO_POSITION[player_number]['y'])
    DISPLAYSURF.blit(scoreSurf, scoreRect)

def drawTurbos(player_number, turbos, color):
    scoreSurf = BASICFONT.render('Turbos: %s' % (turbos), True, color)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (INFO_POSITION[player_number]['x'], INFO_POSITION[player_number]['y'] + 20)
    DISPLAYSURF.blit(scoreSurf, scoreRect)    

def drawLives(player_number, lives, color):
    scoreSurf = BASICFONT.render('Lives: %s' % (lives), True, color)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (INFO_POSITION[player_number]['x'], INFO_POSITION[player_number]['y'] + 40)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

def drawWorm(wormCoords, wormColor, is_robot=False, is_shrinking=False, is_turbo=False):
    cc = 0
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE

        # Do outer blocks
        if cc%2 == 0:
            color = wormColor
        else:
            if is_robot:
                color = PURPLE
            else:
                color = DARKGREEN

        if is_turbo:
            color = getPulseColor(color, WHITE, 1.0)
            
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, color, wormSegmentRect)

        # Do inner blocks
        if cc > 0:
            if cc%2 == 0:
                if is_robot:
                    color = PURPLE
                else:
                    color = DARKGREEN   
            else:
                color = wormColor           

            if is_shrinking:
                color = getPulseColor(color, BLACK, 2.0)
                
            wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
            pygame.draw.rect(DISPLAYSURF, color, wormInnerSegmentRect)
            
        cc += 1

def drawPortals(portalCoords):
    use_color = getPulseColor(PURPLE, GREEN, 2.0) 
    for portal in portalCoords:
        drawPortal(portal, use_color)


def getPulseColor(color1, color2, pulse_time=2.0):
    half_time = pulse_time/2.0
    use_color = list(color1)
    
    for ii in range(len(use_color)):
        color_dist = color2[ii] - use_color[ii]
        if (GLOBAL_TIME % pulse_time) < half_time:
            # Ramp up
            use_color[ii] = (GLOBAL_TIME % half_time)/half_time * color_dist + use_color[ii]
        else:
            # Ramp down
            use_color[ii] = (GLOBAL_TIME % half_time)/half_time * (-color_dist) + color2[ii]
    use_color = tuple(use_color)       
    return use_color


def drawPortal(portalCoords, color):
    for coord in portalCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        portalSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, color, portalSegmentRect)


def drawFruit(coord, color=RED, is_shiny=False, is_bad=False):
    if len(coord) == 0:
        return
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    fruitRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, color, fruitRect)

    if is_bad:
        fruitRect = pygame.Rect(x+3, y+3, CELLSIZE-14, CELLSIZE-14)
        pygame.draw.rect(DISPLAYSURF, BLACK, fruitRect)       
    elif is_shiny:
        fruitRect = pygame.Rect(x+3, y+3, CELLSIZE-14, CELLSIZE-14)
        pygame.draw.rect(DISPLAYSURF, WHITE, fruitRect)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()
