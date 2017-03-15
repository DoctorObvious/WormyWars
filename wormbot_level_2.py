from worm_class import *
from settings import *
from utilities import *
import random


# Goes for all fruit
class WormBotLevel2(Worm):

    is_robot = True

    def choose_direction(self, visible_worms_info, portal_coords, apple, fruits):

        # Give points to the best directions [LEFT, RIGHT, UP, DOWN]
        # Add a little randomness
        rand_part = 5.0
        goodness = [random.random()*rand_part, random.random()*rand_part,
                    random.random()*rand_part, random.random()*rand_part]

        # Give a very slight preference to the current direction, all else being equal
        goodness[DIRECTIONS.index(self._direction)] += 4.0

        # Find the closest fruit.
        apple_distance = total_distance_to_target(self.coords[HEAD], apple)
        fruit_coords = get_existing_fruit_coords(fruits)
        fruit_target = apple
        if len(fruit_coords) > 0:
            close_fruit, fruit_distance = closest_fruit(self.coords[HEAD], fruit_coords)

            if fruit_distance < (apple_distance - 4):   # Prefer the apple a bit
                fruit_target = close_fruit

        goodness = prefer_direction_to_fruit(self.coords, fruit_target, goodness, 1.0)

        # Can't go the opposite of the current direction
        # print "Current direction: {}".format(current_direction)
        # print "DIRECTIONS.index(current_direction): {}".format(DIRECTIONS.index(current_direction))
        goodness[D_OPPOSITE.index(self._direction)] = -1000  # Impossible choice

        # Check each direction for collision with other objects
        visible_worm_coords = collect_worms_coords(visible_worms_info)
        for jj in range(4):
            new_head = get_new_head(DIRECTIONS[jj], self.coords)
            found_hit = False

            # check if the worm will hit its body, other worm bodies
            for coord in visible_worm_coords + self.coords:
                if same_coord(coord, new_head):
                    found_hit = True
                    goodness[jj] -= 90.0   # A hit is not a good choice.

            # check if the worm will hit a portal
            for coord in portal_coords:
                if same_coord(coord, new_head):
                    found_hit = True
                    goodness[jj] -= 25.0   # A portal is an uncertain good choice.

            # check if the worm will hit the edge
            if not found_hit:
                if new_head['x'] == -1 or new_head['x'] == CELLWIDTH \
                        or new_head['y'] == -1 or new_head['y'] == CELLHEIGHT:
                    found_hit = True
                    goodness[jj] -= 90   # A hit is not a good choice.

            # check if the worm is going to hit where it looks like the other worm is going
            if not found_hit:
                for worm_info in visible_worms_info:
                    if worm_info.player_number == self.player_number:
                        continue   # Don't check against the same worm

                    other_new_head = get_new_head(worm_info.direction, worm_info.coords)
                    if utils.same_coord(new_head, other_new_head):
                        # found_hit = True
                        goodness[jj] -= 10.0   # Avoid were other worm is headed

                    # And check where other worm MIGHT go
                    if total_distance(new_head, worm_info.coords[HEAD]) == 1:
                        goodness[jj] -= 5.0   # Avoid where other worm is might be headed

            # Check if it is a single lane road
            if not found_hit:
                # See if something is occupying the "sides" of the new direction
                # That would be the alternate direction from the new head and the opposite of the alternate
                side_check_1 = get_new_head(D_ALTERNATE[jj], [new_head])
                side_check_2 = get_new_head(D_ALT_ALT[jj], [new_head])
                if side_check_1 in visible_worm_coords and side_check_2 in visible_worm_coords:
                    # print "tunnel warning"
                    goodness[jj] -= 20.0

        # Find the "most goodness" direction
        new_direction = DIRECTIONS[goodness.index(max(goodness))]
        # print "new_direction: {}".format(new_direction)
        self._direction = new_direction
