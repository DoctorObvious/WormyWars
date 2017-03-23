from settings import *
import pygame


class Action:

    def __init__(self, new_coord, new_direction):
        self.new_coord = new_coord
        self.new_direction = new_direction


class PortalPoint:

    def __init__(self, coord, left_action=None, right_action=None,
                 up_action=None, down_action=None):

        self.coord = coord
        self.left_action = left_action
        self.right_action = right_action
        self.up_action = up_action
        self.down_action = down_action

    def get_action(self, direction):

        if direction == LEFT:
            return self.left_action
        elif direction == RIGHT:
            return self.right_action
        elif direction == UP:
            return self.up_action
        elif direction == DOWN:
            return self.down_action


# class Portal:
#     def __init__(self, portal_points):
#         self.portal_points = portal_points

# Examples of making instances of classes
# coord = {'x': 56, 'y': 65}
#
# paction = Action(coord, LEFT)
#
# p1 = PortalPoint(coord,
#                  left_action=Action(coord, LEFT),
#                  right_action=Action({'x': 678, 'y':34}, DOWN))

class Level:
    def __init__(self, number, name, portals, walls, num_apples):
        self.portals = portals
        self.walls = walls
        self.number = number
        self.name = name
        self.num_apples = num_apples

    def get_all_portal_coords(self):
        all_portals_coords = []

        for portal_point in self.portals:
            all_portals_coords.append(portal_point.coord)

        return all_portals_coords

#
# Define information for level 1
#

portals2 = [
    # Left Side, Top
    PortalPoint({'x': 2, 'y': 10},
                left_action=Action({'x': 41, 'y': 10}, LEFT),
                right_action=Action({'x': 43, 'y': 10}, RIGHT),
                down_action=Action({'x': 2, 'y': 24}, DOWN)),
    PortalPoint({'x': 2, 'y': 11},
                left_action=Action({'x': 41, 'y': 11}, LEFT),
                right_action=Action({'x': 43, 'y': 11}, RIGHT)),
    PortalPoint({'x': 2, 'y': 12},
                left_action=Action({'x': 41, 'y': 12}, LEFT),
                right_action=Action({'x': 43, 'y': 12}, RIGHT),
                up_action=Action({'x': 2, 'y': 20}, UP)),

    # Left Side, Bottom
    PortalPoint({'x': 2, 'y': 21},
                left_action=Action({'x': 41, 'y': 21}, LEFT),
                right_action=Action({'x': 43, 'y': 21}, RIGHT),
                down_action=Action({'x': 2, 'y': 12}, DOWN)),
    PortalPoint({'x': 2, 'y': 22},
                left_action=Action({'x': 41, 'y': 22}, LEFT),
                right_action=Action({'x': 43, 'y': 22}, RIGHT)),
    PortalPoint({'x': 2, 'y': 23},
                left_action=Action({'x': 41, 'y': 23}, LEFT),
                right_action=Action({'x': 43, 'y': 23}, RIGHT),
                up_action=Action({'x': 2, 'y': 10}, UP)),

    # Right Side, Top
    PortalPoint({'x': 42, 'y': 10},
                left_action=Action({'x': 1, 'y': 10}, LEFT),
                right_action=Action({'x': 3, 'y': 10}, RIGHT),
                down_action=Action({'x': 42, 'y': 23}, DOWN)),
    PortalPoint({'x': 42, 'y': 11},
                left_action=Action({'x': 1, 'y': 11}, LEFT),
                right_action=Action({'x': 3, 'y': 11}, RIGHT)),
    PortalPoint({'x': 42, 'y': 12},
                left_action=Action({'x': 1, 'y': 12}, LEFT),
                right_action=Action({'x': 3, 'y': 12}, RIGHT),
                up_action=Action({'x': 42, 'y': 20}, UP)),

    # Right Side, Bottom
    PortalPoint({'x': 42, 'y': 21},
                left_action=Action({'x': 1, 'y': 21}, LEFT),
                right_action=Action({'x': 3, 'y': 21}, RIGHT),
                down_action=Action({'x':42 , 'y': 12}, DOWN)),
    PortalPoint({'x': 42, 'y': 22},
                left_action=Action({'x': 1, 'y': 22}, LEFT),
                right_action=Action({'x': 3, 'y': 22}, RIGHT)),
    PortalPoint({'x': 42, 'y': 23},
                left_action=Action({'x': 1, 'y': 23}, LEFT),
                right_action=Action({'x': 3, 'y': 23}, RIGHT),
                up_action=Action({'x': 42, 'y': 10}, UP)),

    # Top, Left Side
    PortalPoint({'x': 14, 'y': 2},
                right_action=Action({'x': 32, 'y': 2}, RIGHT),
                up_action=Action({'x': 14, 'y': 31}, UP),
                down_action=Action({'x': 14, 'y': 32}, DOWN)),
    PortalPoint({'x': 15, 'y': 2},
                up_action=Action({'x': 15, 'y': 31}, UP),
                down_action=Action({'x': 15, 'y': 32}, DOWN)),
    PortalPoint({'x': 16, 'y': 2},
                up_action=Action({'x': 16, 'y': 31}, UP),
                down_action=Action({'x': 16, 'y': 32}, DOWN),
                left_action=Action({'x': 28, 'y': 2}, LEFT)),

    # Top, Right Side
    PortalPoint({'x': 29, 'y': 2},
                right_action=Action({'x': 17, 'y': 2}, RIGHT),
                up_action=Action({'x': 29, 'y': 31}, UP),
                down_action=Action({'x': 29, 'y': 33}, DOWN)),
    PortalPoint({'x': 30, 'y': 2},
                up_action=Action({'x': 30, 'y': 31}, UP),
                down_action=Action({'x': 30, 'y': 33}, DOWN)),
    PortalPoint({'x': 31, 'y': 2},
                up_action=Action({'x': 31, 'y': 31}, UP),
                down_action=Action({'x': 31, 'y': 33}, DOWN),
                left_action=Action({'x': 13, 'y': 2}, LEFT)),

    # Bottom, Left Side
    PortalPoint({'x': 14, 'y': 32},
                right_action=Action({'x': 32, 'y': 32}, RIGHT),
                up_action=Action({'x': 14, 'y': 1}, UP),
                down_action=Action({'x': 14, 'y': 3}, DOWN)),
    PortalPoint({'x': 15, 'y': 32},
                up_action=Action({'x': 15, 'y': 1}, UP),
                down_action=Action({'x': 15, 'y': 3}, DOWN)),
    PortalPoint({'x': 16, 'y': 32},
                up_action=Action({'x': 16, 'y': 1}, UP),
                down_action=Action({'x': 16, 'y': 3}, DOWN),
                left_action=Action({'x': 28, 'y': 32}, LEFT)),

    # Bottom, Right Side
    PortalPoint({'x': 29, 'y': 32},
                right_action=Action({'x': 17, 'y': 32}, RIGHT),
                up_action=Action({'x': 29, 'y': 1}, UP),
                down_action=Action({'x': 29, 'y': 3}, DOWN)),
    PortalPoint({'x': 30, 'y': 32},
                up_action=Action({'x': 30, 'y': 1}, UP),
                down_action=Action({'x': 30, 'y': 3}, DOWN)),
    PortalPoint({'x': 31, 'y': 32},
                up_action=Action({'x': 31, 'y': 1}, UP),
                down_action=Action({'x': 31, 'y': 3}, DOWN),
                left_action=Action({'x': 13, 'y': 32}, LEFT)),
]

walls1 = [
    {'x': range(16, 30), 'y': CELLHEIGHT/2 + 2},
    {'x': range(16, 30), 'y': CELLHEIGHT/2 - 2},
    ]

walls3 = [
    {'x': range(16, 30), 'y': CELLHEIGHT / 2},
    {'x': CELLWIDTH / 2, 'y': range(16, 30) },
]

level0 = Level(0, "Here We Go!", [], [], 1)
level1 = Level(0, "Walls!", [], walls1, 3)
level2 = Level(0, "Portals!", portals2, [], 5)
level3 = Level(0, "Trickier!", portals2, walls3, 10)

all_levels = [level0, level1, level2, level3]