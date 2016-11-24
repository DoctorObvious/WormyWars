# Wormy Wars! (a Nibbles clone)
# Originally by Al Sweigart al@inventwithpython.com
# Modified and expanded by Mark and Lincoln Phillips
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random
import pygame
import sys
from pygame.locals import *
from settings import *
from utilities import *
from worm_class import *
from wormbot_level_1 import WormBotLevel1
from wormbot_level_2 import WormBotLevel2


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

    num_players = 1
    num_robots = 0

    key = show_start_screen()

    # Keep playing more games until escape
    while True:
        if key == K_1:
            num_players = 1
            num_robots = 0
        elif key == K_2:
            num_players = 2
            num_robots = 0
        elif key == K_3:
            num_players = 3
            num_robots = 0
        elif key == K_4:
            num_players = 4
            num_robots = 0
        elif key == K_F1:
            num_players = 1
            num_robots = 1
        elif key == K_F2:
            num_players = 2
            num_robots = 1
        elif key == K_F3:
            num_players = 3
            num_robots = 1
        elif key == K_F4:
            num_players = 4
            num_robots = 1
        elif key == K_F6:
            num_players = 4
            num_robots = 2
        elif key == K_r:
            num_players = 4
            num_robots = 4
        winning_player = run_game(num_players, num_robots)
        key = show_game_over_screen(winning_player, WORM_COLORS[winning_player[0] - 1])


def get_safe_starting_coords(player_number, existing_coords=None):
    start_x = 5
    worm_coords = []
    for y_try in range(4, 26):
        start_y = y_try + 7 * player_number
        start_y = ((start_y - 4) % 22) + 4
        worm_coords = worm_starting_coords(start_x, start_y)
        if are_coords_safe(worm_coords, existing_coords):
            break

    return worm_coords


def worm_starting_coords(start_x, start_y):
    return [{'x': start_x, 'y': start_y},
            {'x': start_x - 1, 'y': start_y},
            {'x': start_x - 2, 'y': start_y}]


def get_portal_coords():
    # Do sides
    left_portal_coords = [0] * PORTALS_PER_SIDE
    left_portal_names = ['left'] * PORTALS_PER_SIDE
    right_portal_coords = [0] * PORTALS_PER_SIDE
    right_portal_names = ['right'] * PORTALS_PER_SIDE

    portal_incr = int(CELLHEIGHT / (PORTALS_PER_SIDE + 1))
    portal_offset = (PORTAL_LENGTH - 1) / 2
    for hh in range(PORTALS_PER_SIDE):
        left_portal_coords[hh] = [0] * PORTAL_LENGTH
        right_portal_coords[hh] = [0] * PORTAL_LENGTH

        for xx in range(PORTAL_LENGTH):
            left_portal_coords[hh][xx] = {'x': LEFT_PORTAL_X, 'y': (hh + 1) * portal_incr - portal_offset + xx}
            right_portal_coords[hh][xx] = {'x': RIGHT_PORTAL_X, 'y': (hh + 1) * portal_incr - portal_offset + xx}

    up_portal_coords = [0] * PORTALS_PER_SIDE
    up_portal_names = ['up'] * PORTALS_PER_SIDE
    down_portal_coords = [0] * PORTALS_PER_SIDE
    down_portal_names = ['down'] * PORTALS_PER_SIDE

    portal_incr = int(CELLWIDTH / (PORTALS_PER_SIDE + 1))
    portal_offset = (PORTAL_LENGTH - 1) / 2
    for hh in range(PORTALS_PER_SIDE):
        up_portal_coords[hh] = [0] * PORTAL_LENGTH
        down_portal_coords[hh] = [0] * PORTAL_LENGTH

        for xx in range(PORTAL_LENGTH):
            up_portal_coords[hh][xx] = {'y': UP_PORTAL_Y, 'x': (hh + 1) * portal_incr - portal_offset + xx}
            down_portal_coords[hh][xx] = {'y': DOWN_PORTAL_Y, 'x': (hh + 1) * portal_incr - portal_offset + xx}

    portal_coords = left_portal_coords + right_portal_coords + up_portal_coords + down_portal_coords
    portal_names = left_portal_names + right_portal_names + up_portal_names + down_portal_names
    return portal_coords, portal_names


def run_game(num_players, num_robots=0):
    start_the_clock()

    # Create worms
    worms = []
    for ii in range(num_players):
        starting_coords = get_safe_starting_coords(player_number=ii, existing_coords=None)
        if ii >= num_players - num_robots:
            if ii % 2 == 0:
                worms.append(WormBotLevel1(WORM_COLORS[ii], starting_coords, player_number=ii))
            else:
                worms.append(WormBotLevel2(WORM_COLORS[ii], starting_coords, player_number=ii))

        else:
            worms.append(Worm(WORM_COLORS[ii], starting_coords, player_number=ii))

    sound_happy = pygame.mixer.Sound(SOUND_HAPPY)
    sound_happy.set_volume(0.5)
    sound_die = pygame.mixer.Sound(SOUND_DIE)
    sound_beep = pygame.mixer.Sound(SOUND_BEEP)
    sound_portal = pygame.mixer.Sound(SOUND_PORTAL)
    sound_life = pygame.mixer.Sound(SOUND_LIFE)
    sound_reverse = pygame.mixer.Sound(SOUND_REVERSE)

    do_switcheroo = False
    do_switcheroo_effect = False
    switcheroo_start_time = 0.0

    # Get the portal coordinates
    portal_coords, portal_names = get_portal_coords()

    existing_coords = make_coord_list(portal_coords) + collect_worms_coords(worms)

    # Start the apple in a random place.    
    apple = get_safe_fruit_location(existing_coords)
    apple_is_bad = False
    grape = []
    banana = []
    golden_apple = []
    blueberry = []
    lime = []

    apple_number = 1
    frame_count = 0.0
    pause_end_time = 0.0

    # How long since the LAST appearance of a fruit
    last_grape_time = 0
    last_banana_time = 0
    last_golden_time = 0
    last_blueberry_time = 0
    last_lime_time = 0

    # Initialize time since a fruit has appeared
    apple_time = 0
    golden_time = -1000
    blueberry_time = -1000
    lime_time = -1000

    while True:  # main game loop
        frame_count += 1.0

        if do_switcheroo_effect:
            DISPLAYSURF.fill(get_pulse_color([BGCOLOR, LIMEGREEN], pulse_time=SWITCH_PAUSE_TIME,
                                             pulse_start_time=switcheroo_start_time))
        else:
            DISPLAYSURF.fill(BGCOLOR)

        draw_grid()

        keys_processed = [0] * num_players

        if current_time() > pause_end_time:
            do_switcheroo_effect = False

            # Handle robots based on current state of worms and board
            visible_worms_info = gather_visible_worms_info(worms)  # Gather before any of this frame's choices are made
            fruits = [banana, grape, lime, blueberry, golden_apple]
            for ii in range(num_players):
                if worms[ii].is_robot and worms[ii].is_in_play:
                    worms[ii].choose_direction(visible_worms_info, portal_coords, apple, fruits)

            for event in pygame.event.get():  # event handling loop

                if event.type == QUIT:
                    terminate()

                # See how key presses affect direction for each worm!
                for ii in range(num_players):
                    direction = worms[ii].get_direction()
                    new_direction = direction

                    if event.type == KEYDOWN:
                        key_press = None
                        if event.key == ALL_LEFTS[ii]:
                            key_press = LEFT
                            if direction != RIGHT:
                                new_direction = LEFT
                        elif event.key == ALL_RIGHTS[ii]:
                            key_press = RIGHT
                            if direction != LEFT:
                                new_direction = RIGHT
                        elif event.key == ALL_UPS[ii]:
                            key_press = UP
                            if direction != DOWN:
                                new_direction = UP
                        elif event.key == ALL_DOWNS[ii]:
                            key_press = DOWN
                            if direction != UP:
                                new_direction = DOWN
                        elif event.key == K_ESCAPE:
                            terminate()
                        elif event.key == K_F5:
                            for worm in worms:
                                worm.terminate()

                        if key_press == worms[ii].last_key_press \
                                and current_time() - worms[ii].last_press_time < DOUBLE_CLICK_TIME:
                            # Double click in same direction for turbo
                            worms[ii].go_turbo()

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
                                    worms[ii].last_key_press = key_press
                                    worms[ii].last_press_time = current_time()
                            else:
                                worms[ii].last_key_press = key_press
                                worms[ii].last_press_time = current_time()

                        worms[ii].set_direction(direction)

            # Do for each worm!
            for ii in range(num_players):
                if worms[ii].is_in_play:

                    num_moves = 1
                    if worms[ii].is_in_turbo():
                        num_moves = 2

                    direction = worms[ii].get_direction()
                    for kk in range(num_moves):
                        if worms[ii].is_dying or worms[ii].is_dead():  # In case worm died in previous (turbo) move.
                            continue

                        worms[ii].move()

                        worm_coords = worms[ii].coords

                        # check if the worm has hit the edge
                        if worm_coords[HEAD]['x'] == -1 or worm_coords[HEAD]['x'] == CELLWIDTH \
                                or worm_coords[HEAD]['y'] == -1 or worm_coords[HEAD]['y'] == CELLHEIGHT:
                            worms[ii].die()

                        # check if the worm has hit its body
                        for worm_body in worm_coords[1:]:
                            if same_coord(worm_coords[HEAD], worm_body):
                                worms[ii].die()

                        # check if the worm has hit a portal
                        hit_portal = False
                        for portal_coord in portal_coords:
                            for coord in portal_coord:
                                if same_coord(worm_coords[HEAD], coord):
                                    sound_portal.play()
                                    hit_portal = True

                        # teleport logic:  Should update to use x AND y checks and/or use the portal "name".
                        if hit_portal:
                            if worm_coords[HEAD]['x'] == LEFT_PORTAL_X:
                                if direction == UP or direction == DOWN:
                                    worm_coords[HEAD] = move_worm_same_side_portal(worm_coords[HEAD], portal_coords)
                                elif direction == LEFT:
                                    worm_coords[HEAD]['x'] = RIGHT_PORTAL_X - 1
                                else:
                                    worm_coords[HEAD]['x'] = RIGHT_PORTAL_X + 1

                            elif worm_coords[HEAD]['x'] == RIGHT_PORTAL_X:
                                if direction == UP or direction == DOWN:
                                    worm_coords[HEAD] = move_worm_same_side_portal(worm_coords[HEAD], portal_coords)
                                elif direction == LEFT:
                                    worm_coords[HEAD]['x'] = LEFT_PORTAL_X - 1
                                else:
                                    worm_coords[HEAD]['x'] = LEFT_PORTAL_X + 1

                            elif worm_coords[HEAD]['y'] == UP_PORTAL_Y:
                                if direction == LEFT or direction == RIGHT:
                                    worm_coords[HEAD] = move_worm_same_side_portal(worm_coords[HEAD], portal_coords)
                                elif direction == DOWN:
                                    worm_coords[HEAD]['y'] = DOWN_PORTAL_Y + 1
                                else:
                                    worm_coords[HEAD]['y'] = DOWN_PORTAL_Y - 1

                            elif worm_coords[HEAD]['y'] == DOWN_PORTAL_Y:
                                if direction == LEFT or direction == RIGHT:
                                    worm_coords[HEAD] = move_worm_same_side_portal(worm_coords[HEAD], portal_coords)
                                elif direction == DOWN:
                                    worm_coords[HEAD]['y'] = UP_PORTAL_Y + 1
                                else:
                                    worm_coords[HEAD]['y'] = UP_PORTAL_Y - 1

                        # check if the worm has hit another worm
                        for jj in range(num_players):
                            # make sure it is not the same worm
                            if jj == ii:
                                continue

                            # make sure the worm isn't dead
                            if not worms[jj].is_in_play or worms[jj].is_dead():
                                continue

                            # Actual checking for collision
                            kk = 0
                            for worm_block in worms[jj].coords:
                                if same_coord(worm_coords[HEAD], worm_block):
                                    worms[ii].die()  # This worm dies
                                    worms[ii].draw(DISPLAYSURF)
                                    if kk == 0:  # This is the other head block
                                        worms[jj].die()  # The other worm dies
                                kk += 1

                        existing_coords = make_coord_list(portal_coords) + collect_worms_coords(worms)

                        # check if worm has eaten an apple
                        if same_coord(worm_coords[HEAD], apple):
                            apple = get_safe_fruit_location(existing_coords)  # set a new apple somewhere
                            apple_time = current_time()
                            sound_happy.play()
                            worms[ii].add_score(apple_number)
                            if apple_is_bad:
                                worms[ii].shrink()
                            else:
                                worms[ii].grow(apple_number)
                                worms[ii].add_turbo()

                            apple_number += 1

                        if len(golden_apple) > 0:
                            # check if a worm has eaten a golden_apple
                            if same_coord(worm_coords[HEAD], golden_apple):
                                last_golden_time = current_time()
                                sound_life.play()
                                golden_apple = []
                                worms[ii].add_life()

                        if len(blueberry) > 0:
                            # check if a worm has eaten a blueberry
                            if same_coord(worm_coords[HEAD], blueberry):
                                last_blueberry_time = current_time()
                                sound_happy.play()
                                blueberry = []
                                for mm in range(num_players):
                                    if mm != ii:
                                        worms[mm].freeze()
                                        remove_worm_events(mm)

                        if len(grape) > 0:
                            # check if a worm has eaten a grape
                            if same_coord(worm_coords[HEAD], grape):
                                last_grape_time = current_time()
                                sound_happy.play()
                                worms[ii].make_invisible()
                                worms[ii].add_score(GRAPE_POINTS)
                                grape = []

                        if len(banana) > 0:
                            # check if a worm has eaten a banana, and flip the coordinates
                            if same_coord(worm_coords[HEAD], banana):
                                last_banana_time = current_time()
                                sound_reverse.play()
                                worms[ii].reverse()
                                worms[ii].add_score(BANANA_POINTS)
                                banana = []

                        # Do lime switch after length is adjusted
                        if len(lime) > 0 and not worms[ii].is_dying:
                            # check if a worm has eaten a lime
                            if same_coord(worm_coords[HEAD], lime):
                                last_lime_time = current_time()
                                sound_happy.play()
                                worms[ii].add_score(LIME_POINTS)
                                lime = []
                                do_switcheroo = True
                                for jj in range(num_players):
                                    remove_worm_events(jj)

        # Was a switcheroo triggered?
        if do_switcheroo:
            pause_end_time = get_pause_end_time(SWITCH_PAUSE_TIME)
            switcheroo_start_time = current_time()
            switcheroo(worms)
            do_switcheroo = False
            do_switcheroo_effect = True

        # ------------- Time check ----------------

        # Has the apple gone bad?
        is_alive = [worm.is_in_play for worm in worms]
        bad_apple_time = max(7, BAD_APPLE_TIME - sum(is_alive) * 2)
        if elapsed_time(apple_time) > bad_apple_time:
            apple_is_bad = True
        else:
            apple_is_bad = False

        # Is it time to make a golden_apple?
        if len(golden_apple) == 0 and (elapsed_time(last_golden_time) > GOLDEN_APPEAR_TIME):
            # Make a golden_apple!
            golden_apple = get_safe_fruit_location(existing_coords)
            golden_time = current_time()
            last_golden_time = golden_time
        elif len(golden_apple) > 0 and (elapsed_time(golden_time) > GOLDEN_DISAPPEAR_TIME):
            # It is time for the golden_apple to disappear
            golden_apple = []

        # Is it time to make a blueberry?
        if len(blueberry) == 0 and (elapsed_time(last_blueberry_time) > BLUEBERRY_APPEAR_TIME):
            # Make a blueberry!
            blueberry = get_safe_fruit_location(existing_coords)
            blueberry_time = current_time()
            last_blueberry_time = blueberry_time
        elif len(blueberry) > 0 and (elapsed_time(blueberry_time) > BLUEBERRY_DISAPPEAR_TIME):
            # It is time for the blueberry to disappear
            blueberry = []

        # Is it time to make a lime?
        if len(lime) == 0 and (elapsed_time(last_lime_time) > LIME_APPEAR_TIME) and sum(is_alive) > 1:
            # Make a lime!
            lime = get_safe_fruit_location(existing_coords)
            lime_time = current_time()
            last_lime_time = lime_time
        elif (len(lime) > 0 and (elapsed_time(lime_time) > LIME_DISAPPEAR_TIME)) or sum(is_alive) < 2:
            # It is time for the lime to disappear
            lime = []

        # Is it time to make a grape?
        if len(grape) == 0 and (elapsed_time(last_grape_time) > GRAPE_APPEAR_TIME):
            # Make a grape!
            grape = get_safe_fruit_location(existing_coords)

        # Is it time to make a banana?
        if len(banana) == 0 and (elapsed_time(last_banana_time) > BANANA_APPEAR_TIME):
            # Make a banana!
            banana = get_safe_fruit_location(existing_coords)

        existing_coords = make_coord_list(portal_coords) + collect_worms_coords(worms)

        # ----------------  Draw everything! ---------------------------
        for ii in range(num_players):
            draw_score(ii, worms[ii].score, worms[ii].color)
            draw_turbos(ii, worms[ii].num_turbos, worms[ii].color)
            draw_lives(ii, worms[ii].num_lives, worms[ii].color)
            worms[ii].draw(DISPLAYSURF)

        draw_portals(portal_coords)

        draw_fruit(apple, RED, is_bad=apple_is_bad)
        draw_fruit(golden_apple, GOLD, is_shiny=True)
        draw_fruit(grape, PURPLE)
        draw_fruit(banana, YELLOW)
        draw_fruit(blueberry, BLUE2)
        draw_fruit(lime, LIMEGREEN)

        for ii in range(num_players):
            if worms[ii].is_dead():
                remove_worm_events(ii)

                if worms[ii].is_in_play:
                    starting_coords = get_safe_starting_coords(ii, existing_coords)
                    worms[ii].birth(starting_coords)
                    if worms[ii].num_lives == 0:
                        sound_die.play()
                else:
                    worms[ii].draw(DISPLAYSURF)

        # Update coordinates where things are
        existing_coords = make_coord_list(portal_coords) + collect_worms_coords(worms)

        pygame.display.update()
        FPSCLOCK.tick(FPS)
        # sound_beep.play()

        # Check to see if the game is over
        if not any(is_alive):
            scores = [worm.score for worm in worms]
            max_score = max(scores)
            winning_player = []
            for ii in range(num_players):
                if scores[ii] == max_score:
                    winning_player.append(ii + 1)

            return winning_player  # game over


def move_worm_same_side_portal(worm_head, portal_coords):
    # Find which portal we're in
    for portal in portal_coords:
        if worm_head in portal:
            found_portal = portal

    # Is it a vertical or horizontal portal?
    if found_portal[0]['x'] == found_portal[1]['x']:
        use_key = 'x'
        other_key = 'y'
    else:
        use_key = 'y'
        other_key = 'x'

    # Are we going in the min or max end?
    min_of_found = find_min_coord(found_portal, other_key)
    if worm_head[other_key] == min_of_found:
        entered_min = True
    else:
        entered_min = False

    # Find the other one on the same side
    other_portal = []
    for portal in portal_coords:
        if portal[0][use_key] == found_portal[0][use_key] and portal[0][other_key] != found_portal[0][other_key]:
            other_portal = portal

    # Figure out the correct end of the portal to exit
    if entered_min:
        use_val = find_max_coord(other_portal, other_key)
        use_val += 1  # Go beyond end of portal
    else:
        use_val = find_min_coord(other_portal, other_key)
        use_val -= 1  # Go beyond end of portal

    new_head = dict()
    new_head[use_key] = found_portal[0][use_key]
    new_head[other_key] = use_val

    return new_head


def find_min_coord(coords, key):
    use_val = max(WINDOWWIDTH, WINDOWHEIGHT)
    for coord in coords:
        if coord[key] < use_val:
            use_val = coord[key]

    return use_val


def find_max_coord(coords, key):
    use_val = 0
    for coord in coords:
        if coord[key] > use_val:
            use_val = coord[key]

    return use_val


def get_safe_fruit_location(existing_coords):
    fruit = get_random_location()  # set a new apple somewhere
    while not are_coords_safe([fruit], existing_coords):
        fruit = get_random_location()  # set a new apple somewhere

    return fruit


def remove_worm_events(worm_number):
    for event in pygame.event.get():  # event handling loop
        if event.type == KEYDOWN:
            if event.key == ALL_LEFTS[worm_number]:
                continue
            elif event.key == ALL_RIGHTS[worm_number]:
                continue
            elif event.key == ALL_UPS[worm_number]:
                continue
            elif event.key == ALL_DOWNS[worm_number]:
                continue

        pygame.event.post(event)


def switcheroo(worms):
    num_players = len(worms)

    # TODO: Cleanup
    all_worm_coords = []
    all_directions = []
    for ii in range(num_players):
        all_worm_coords = all_worm_coords + [worms[ii].coords]
        all_directions = all_directions + [worms[ii].get_direction()]

    for ii in range(num_players):
        for jj in range(1, num_players):
            new_index = (ii + jj) % num_players
            if worms[new_index].is_in_play:
                break

        worms[ii].coords = all_worm_coords[new_index]
        worms[ii].set_direction(all_directions[new_index])


def get_pause_end_time(pause_length):
    return current_time() + pause_length


def draw_press_key_msg():
    press_key_surf = BASICFONT.render('Press # of players (1-4) to play.', True, LIGHTGRAY)
    press_key_rect = press_key_surf.get_rect()
    press_key_rect.topleft = (WINDOWWIDTH - 300, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(press_key_surf, press_key_rect)


def check_for_key_press():
    for event in pygame.event.get():
        if event.type == QUIT:  # event is quit
            terminate()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:  # event is escape key
                terminate()
            else:
                return event.key  # key found return with it
    # no quit or key events in queue so return None    
    return None


def show_start_screen():
    title_font = pygame.font.Font('freesansbold.ttf', 100)
    # title_surf_1 = title_font.render('Wormy Wars!', True, WHITE, DARKGREEN)
    # title_surf_1 = title_font.render('Wormy Wars!', True, WHITE)
    # title_surf_2 = title_font.render('Wormy Wars!', True, PURPLE)

    degrees1 = 0
    degrees2 = 0

    # KRT 14/06/2012 rewrite event detection to deal with mouse use
    pygame.event.get()  # clear out event queue

    while True:
        DISPLAYSURF.fill(BGCOLOR)

        use_color = get_pulse_color([BLACK, PURPLE], pulse_time=2.0)
        title_surf_2 = title_font.render('Wormy Wars!', True, use_color)

        rotated_surf_2 = pygame.transform.rotate(title_surf_2, degrees2)
        rotated_rect_2 = rotated_surf_2.get_rect()
        rotated_rect_2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotated_surf_2, rotated_rect_2)

        # Get use_color for non-rotating title
        use_color = get_pulse_color(TITLE_COLORS, pulse_time=8.0)
        title_surf_1 = title_font.render('Wormy Wars!', True, use_color)

        rotated_surf_1 = pygame.transform.rotate(title_surf_1, degrees1)
        rotated_rect_1 = rotated_surf_1.get_rect()
        rotated_rect_1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotated_surf_1, rotated_rect_1)

        draw_press_key_msg()
        key = check_for_key_press()
        if key:
            return key
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 0  # rotate by 3 degrees each frame
        degrees2 += 7  # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def get_random_location():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def show_game_over_screen(winning_player, use_color):
    game_over_font = pygame.font.Font('freesansbold.ttf', 60)
    game_surf = game_over_font.render('Game', True, WHITE)
    over_surf = game_over_font.render('Over', True, WHITE)

    winning_string = 'Player {} Wins!'.format(winning_player)

    player_surf = game_over_font.render(winning_string, True, use_color)

    game_rect = game_surf.get_rect()
    over_rect = over_surf.get_rect()
    player_rect = player_surf.get_rect()
    game_rect.midtop = (WINDOWWIDTH / 2, 10)
    over_rect.midtop = (WINDOWWIDTH / 2, game_rect.height + 10 + 25)
    player_rect.midtop = (WINDOWWIDTH / 2, game_rect.height + 100 + over_rect.height)

    DISPLAYSURF.blit(game_surf, game_rect)
    DISPLAYSURF.blit(over_surf, over_rect)
    DISPLAYSURF.blit(player_surf, player_rect)
    draw_press_key_msg()
    pygame.display.update()
    pygame.time.wait(500)
    # KRT 14/06/2012 rewrite event detection to deal with mouse use
    pygame.event.get()  # clear out event queue
    while True:
        key = check_for_key_press()
        if key:
            return key
        # KRT 12/06/2012 reduce processor loading in game over screen.
        pygame.time.wait(100)


def draw_score(player_number, score, use_color):
    score_surf = BASICFONT.render('Score: %s' % score, True, use_color)
    score_rect = score_surf.get_rect()
    score_rect.topleft = (INFO_POSITION[player_number]['x'], INFO_POSITION[player_number]['y'])
    DISPLAYSURF.blit(score_surf, score_rect)


def draw_turbos(player_number, turbos, worm_color):
    score_surf = BASICFONT.render('Turbos: %s' % turbos, True, worm_color)
    score_rect = score_surf.get_rect()
    score_rect.topleft = (INFO_POSITION[player_number]['x'], INFO_POSITION[player_number]['y'] + 20)
    DISPLAYSURF.blit(score_surf, score_rect)


def draw_lives(player_number, lives, worm_color):
    score_surf = BASICFONT.render('Lives: %s' % lives, True, worm_color)
    score_rect = score_surf.get_rect()
    score_rect.topleft = (INFO_POSITION[player_number]['x'], INFO_POSITION[player_number]['y'] + 40)
    DISPLAYSURF.blit(score_surf, score_rect)


def draw_portals(portal_coords):
    use_color = get_pulse_color([PURPLE, GREEN], 2.0)
    for portal in portal_coords:
        draw_portal(portal, use_color)


def draw_portal(portal_coords, portal_color):
    for coord in portal_coords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        portal_segment_rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, portal_color, portal_segment_rect)


def draw_fruit(coord, fruit_color=RED, is_shiny=False, is_bad=False):
    if len(coord) == 0:
        return
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    fruit_rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, fruit_color, fruit_rect)

    if is_bad:
        fruit_rect = pygame.Rect(x + 3, y + 3, CELLSIZE - 14, CELLSIZE - 14)
        pygame.draw.rect(DISPLAYSURF, BLACK, fruit_rect)
    elif is_shiny:
        fruit_rect = pygame.Rect(x + 3, y + 3, CELLSIZE - 14, CELLSIZE - 14)
        pygame.draw.rect(DISPLAYSURF, WHITE, fruit_rect)


def draw_grid(grid_color=DARKGRAY):
    for x in range(0, WINDOWWIDTH, CELLSIZE):  # draw vertical lines
        pygame.draw.line(DISPLAYSURF, grid_color, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):  # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, grid_color, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()
