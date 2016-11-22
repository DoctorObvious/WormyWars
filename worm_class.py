import settings
import pygame
import utilities as utils
from worm_clock import *

HEAD = 0  # syntactic sugar: index of the worm's head

class Worm:

    coords = []
    direction = []
    num_lives = []
    score = []
    is_alive = []
    num_to_grow = []
    num_turbos = []
    turbo_ticks = []
    freeze_ticks = []
    invisible_ticks = []
    is_shrinking = []

    last_shrink_time = []
    last_press_time = []
    last_key_press = []

    # is_dying = []   TODO: Do we need this?

    is_robot = False
    starting_turbos = settings.NUM_TURBOS

    def __init__(self, color, starting_coords):
        self.color = color
        self.num_lives = settings.NUM_LIVES
        self.score = 0
        self.last_shrink_time = -100
        self.last_press_time = -100
        self.last_key_press = None

        self.birth(starting_coords)

    def birth(self, starting_coords):
        self.coords = starting_coords
        self.is_alive = True
        self.num_to_grow = 0
        self.num_turbos = self.starting_turbos
        self.turbo_ticks = 0
        self.freeze_ticks = 0
        self.invisible_ticks = 0
        self.is_shrinking = False

    def kill(self):
        self.num_lives -= 1
        self.is_shrinking = False
        self.turbo_ticks = 0
        pass

    def is_visible(self):
        return self.invisible_ticks == 0
    
    def is_turbo(self):
        return self.turbo_ticks > 0
    
    def draw(self, display_surface):
        inner_size = settings.CELLSIZE - 8
        inner_offset = 4
        outer_size = settings.CELLSIZE

        cc = 0
        for coord in self.coords:
            x = coord['x'] * settings.CELLSIZE
            y = coord['y'] * settings.CELLSIZE

            # Do outer blocks
            if cc % 2 == 0:
                color = self.color
            else:
                if self.is_robot:
                    color = settings.PURPLE
                else:
                    color = settings.DARKGREEN

            if self.is_turbo():
                color = utils.get_shifting_color([color, settings.WHITE], 1.0)

            if not self.is_visible:
                color = settings.BLACK

            worm_outer_rect = pygame.Rect(x, y, outer_size, outer_size)
            pygame.draw.rect(display_surface, color, worm_outer_rect)

            # Do inner blocks
            if cc > 0:
                if cc % 2 == 0:
                    if self.is_robot:
                        color = settings.PURPLE
                    else:
                        color = settings.DARKGREEN
                else:
                    color = self.color

                if self.is_shrinking:
                    color = utils.get_shifting_color([color, settings.BLACK], 2.0)

                if not self.is_visible():
                    color = settings.BLACK

                worm_inner_rect = pygame.Rect(x + inner_offset, y + inner_offset, inner_size, inner_size)
                pygame.draw.rect(display_surface, color, worm_inner_rect)

            cc += 1

    def set_direction(self, direction):
        self.direction = direction

    def move(self):
        # move the worm by adding a segment in the direction it is moving
        new_head = self.get_new_head()

        # Grow new head
        self.coords.insert(0, new_head)
        
        # delete the tail unless growing
        if self.num_to_grow > 0:
            # Don't delete the tail, grow instead!
            self.num_to_grow -= 1
        else:
            del self.coords[-1]  # remove worm's tail segment

        if self.is_shrinking and (elapsed_time() - self.last_shrink_time > settings.SHRINK_TIME):
            self.last_shrink_time = elapsed_time()
            if len(self.coords) == 1:
                self.kill()
                return
            else:
                del self.coords[-1]     # remove worm's tail segment


    def grow(self, num_to_grow):
        self.num_to_grow += num_to_grow
        
    def get_new_head(self):
        if self.direction == settings.UP:
            new_head = {'x': self.coords[HEAD]['x'], 'y': self.coords[HEAD]['y'] - 1}
        elif self.direction == settings.DOWN:
            new_head = {'x': self.coords[HEAD]['x'], 'y': self.coords[HEAD]['y'] + 1}
        elif self.direction == settings.LEFT:
            new_head = {'x': self.coords[HEAD]['x'] - 1, 'y': self.coords[HEAD]['y']}
        elif self.direction == settings.RIGHT:
            new_head = {'x': self.coords[HEAD]['x'] + 1, 'y': self.coords[HEAD]['y']}
    
        return new_head  # return the head (don't add it) because it could be used for testing a path

    def add_life(self):
        self.num_lives += 1

    def reverse(self):
        pass

    def switcheroo(self):
        pass

    def freeze(self):
        self.freeze_ticks += settings.NUM_TICKS_IN_FREEZE

    def make_invisible(self):
        self.invisible_ticks += settings.NUM_INVISIBLE_TICKS

    def turbo(self):
        self.turbo_ticks += settings.NUM_TICKS_IN_TURBO

    

