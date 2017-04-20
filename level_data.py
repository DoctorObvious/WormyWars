from level_class import PortalPoint, Action, Level
from settings import *

#
# Define information for level 1, etc.
#

middle_y = CELLHEIGHT / 2 + 1
middle_x = CELLWIDTH / 2 + 1

portals2 = [
    # Left Side, Top
    PortalPoint({'x': 3, 'y': 10},
                left_action=Action({'x': CELLWIDTH-5, 'y': 10}, LEFT),
                right_action=Action({'x': CELLWIDTH-3, 'y': 10}, RIGHT),
                down_action=Action({'x': 3, 'y': 25}, DOWN)),
    PortalPoint({'x': 3, 'y': 11},
                left_action=Action({'x': CELLWIDTH-5, 'y': 11}, LEFT),
                right_action=Action({'x': CELLWIDTH-3, 'y': 11}, RIGHT)),
    PortalPoint({'x': 3, 'y': 12},
                left_action=Action({'x': CELLWIDTH-5, 'y': 12}, LEFT),
                right_action=Action({'x': CELLWIDTH-3, 'y': 12}, RIGHT),
                up_action=Action({'x': 3, 'y': 21}, UP)),

    # Left Side, Bottom
    PortalPoint({'x': 3, 'y': 22},
                left_action=Action({'x': CELLWIDTH-5, 'y': 22}, LEFT),
                right_action=Action({'x': CELLWIDTH-3, 'y': 22}, RIGHT),
                down_action=Action({'x': 3, 'y': 12}, DOWN)),
    PortalPoint({'x': 3, 'y': 23},
                left_action=Action({'x': CELLWIDTH-5, 'y': 23}, LEFT),
                right_action=Action({'x': CELLWIDTH-3, 'y': 23}, RIGHT)),
    PortalPoint({'x': 3, 'y': 24},
                left_action=Action({'x': CELLWIDTH-5, 'y': 24}, LEFT),
                right_action=Action({'x': CELLWIDTH-3, 'y': 24}, RIGHT),
                up_action=Action({'x': 3, 'y': 10}, UP)),

    # Right Side, Top
    PortalPoint({'x': CELLWIDTH-4, 'y': 10},
                left_action=Action({'x': 2, 'y': 10}, LEFT),
                right_action=Action({'x': 4, 'y': 10}, RIGHT),
                down_action=Action({'x': CELLWIDTH-4, 'y': 24}, DOWN)),
    PortalPoint({'x': CELLWIDTH-4, 'y': 11},
                left_action=Action({'x': 2, 'y': 11}, LEFT),
                right_action=Action({'x': 4, 'y': 11}, RIGHT)),
    PortalPoint({'x': CELLWIDTH-4, 'y': 12},
                left_action=Action({'x': 2, 'y': 12}, LEFT),
                right_action=Action({'x': 4, 'y': 12}, RIGHT),
                up_action=Action({'x': CELLWIDTH-4, 'y': 21}, UP)),

    # Right Side, Bottom
    PortalPoint({'x': CELLWIDTH-4, 'y': 22},
                left_action=Action({'x': 2, 'y': 22}, LEFT),
                right_action=Action({'x': 4, 'y': 22}, RIGHT),
                down_action=Action({'x':CELLWIDTH-4 , 'y': 12}, DOWN)),
    PortalPoint({'x': CELLWIDTH-4, 'y': 23},
                left_action=Action({'x': 2, 'y': 23}, LEFT),
                right_action=Action({'x': 4, 'y': 23}, RIGHT)),
    PortalPoint({'x': CELLWIDTH-4, 'y': 24},
                left_action=Action({'x': 2, 'y': 24}, LEFT),
                right_action=Action({'x': 4, 'y': 24}, RIGHT),
                up_action=Action({'x': CELLWIDTH-4, 'y': 10}, UP)),

    # Top, Left Side
    PortalPoint({'x': 13, 'y': 3},
                right_action=Action({'x': 32, 'y': 3}, RIGHT),
                up_action=Action({'x': 13, 'y': CELLHEIGHT-5}, UP),
                down_action=Action({'x': 13, 'y': CELLHEIGHT-4}, DOWN)),
    PortalPoint({'x': 14, 'y': 3},
                up_action=Action({'x': 14, 'y': CELLHEIGHT-5}, UP),
                down_action=Action({'x': 14, 'y': CELLHEIGHT-4}, DOWN)),
    PortalPoint({'x': 15, 'y': 3},
                up_action=Action({'x': 15, 'y': CELLHEIGHT-5}, UP),
                down_action=Action({'x': 15, 'y': CELLHEIGHT-4}, DOWN),
                left_action=Action({'x': 28, 'y': 3}, LEFT)),

    # Top, Right Side
    PortalPoint({'x': 29, 'y': 3},
                right_action=Action({'x': 16, 'y': 3}, RIGHT),
                up_action=Action({'x': 29, 'y': CELLHEIGHT-5}, UP),
                down_action=Action({'x': 29, 'y': CELLHEIGHT-3}, DOWN)),
    PortalPoint({'x': 30, 'y': 3},
                up_action=Action({'x': 30, 'y': CELLHEIGHT-5}, UP),
                down_action=Action({'x': 30, 'y': CELLHEIGHT-3}, DOWN)),
    PortalPoint({'x': 31, 'y': 3},
                up_action=Action({'x': 31, 'y': CELLHEIGHT-5}, UP),
                down_action=Action({'x': 31, 'y': CELLHEIGHT-3}, DOWN),
                left_action=Action({'x': 12, 'y': 3}, LEFT)),

    # Bottom, Left Side
    PortalPoint({'x': 13, 'y': CELLHEIGHT-4},
                right_action=Action({'x': 32, 'y': CELLHEIGHT-4}, RIGHT),
                up_action=Action({'x': 13, 'y': 2}, UP),
                down_action=Action({'x': 13, 'y': 4}, DOWN)),
    PortalPoint({'x': 14, 'y': CELLHEIGHT-4},
                up_action=Action({'x': 14, 'y': 2}, UP),
                down_action=Action({'x': 14, 'y': 4}, DOWN)),
    PortalPoint({'x': 15, 'y': CELLHEIGHT-4},
                up_action=Action({'x': 15, 'y': 2}, UP),
                down_action=Action({'x': 15, 'y': 4}, DOWN),
                left_action=Action({'x': 28, 'y': CELLHEIGHT-4}, LEFT)),

    # Bottom, Right Side
    PortalPoint({'x': 29, 'y': CELLHEIGHT-4},
                right_action=Action({'x': 16, 'y': CELLHEIGHT-4}, RIGHT),
                up_action=Action({'x': 29, 'y': 2}, UP),
                down_action=Action({'x': 29, 'y': 4}, DOWN)),
    PortalPoint({'x': 30, 'y': CELLHEIGHT-4},
                up_action=Action({'x': 30, 'y': 2}, UP),
                down_action=Action({'x': 30, 'y': 4}, DOWN)),
    PortalPoint({'x': 31, 'y': CELLHEIGHT-4},
                up_action=Action({'x': 31, 'y': 2}, UP),
                down_action=Action({'x': 31, 'y': 4}, DOWN),
                left_action=Action({'x': 12, 'y': CELLHEIGHT-4}, LEFT)),
]

walls1 = [
    {'x': range(middle_x - 7, middle_x + 7 + 1), 'y': middle_y + 2},
    {'x': range(middle_x - 7, middle_x + 7 + 1), 'y': middle_y - 2},
    {'x': 10, 'y': range(middle_y - 7, middle_y + 7 + 1)},
    {'x': CELLWIDTH - 9, 'y': range(middle_y - 7, middle_y + 7 + 1)},
    ]

walls3 = [
    {'x': middle_x, 'y': range(0, CELLHEIGHT)},
    {'x': middle_x + 1, 'y': range(0, CELLHEIGHT)},
    {'x': middle_x - 1, 'y': range(0, CELLHEIGHT)},
]

portals3 = [
    # Left Side, Top
    PortalPoint({'x': middle_x-1, 'y': 7}, right_action=Action({'x': middle_x+2, 'y': CELLHEIGHT-8}, RIGHT)),
    PortalPoint({'x': middle_x-1, 'y': 8}, right_action=Action({'x': middle_x+2, 'y': CELLHEIGHT-9}, RIGHT)),
    PortalPoint({'x': middle_x-1, 'y': 9}, right_action=Action({'x': middle_x+2, 'y': CELLHEIGHT-10}, RIGHT)),

    # Left Side, Bottom
    PortalPoint({'x': middle_x - 1, 'y': CELLHEIGHT - 8}, right_action=Action({'x': middle_x + 2, 'y': 7}, RIGHT)),
    PortalPoint({'x': middle_x - 1, 'y': CELLHEIGHT - 9}, right_action=Action({'x': middle_x + 2, 'y': 8}, RIGHT)),
    PortalPoint({'x': middle_x - 1, 'y': CELLHEIGHT - 10}, right_action=Action({'x': middle_x + 2, 'y': 9}, RIGHT)),

    # Right Side, Top
    PortalPoint({'x': middle_x + 1, 'y': 7}, left_action=Action({'x': middle_x - 2, 'y': CELLHEIGHT - 8}, LEFT)),
    PortalPoint({'x': middle_x + 1, 'y': 8}, left_action=Action({'x': middle_x - 2, 'y': CELLHEIGHT - 9}, LEFT)),
    PortalPoint({'x': middle_x + 1, 'y': 9}, left_action=Action({'x': middle_x - 2, 'y': CELLHEIGHT - 10}, LEFT)),

    # Right Side, Bottom
    PortalPoint({'x': middle_x + 1, 'y': CELLHEIGHT - 8}, left_action=Action({'x': middle_x - 2, 'y': 7}, LEFT)),
    PortalPoint({'x': middle_x + 1, 'y': CELLHEIGHT - 9}, left_action=Action({'x': middle_x - 2, 'y': 8}, LEFT)),
    PortalPoint({'x': middle_x + 1, 'y': CELLHEIGHT - 10}, left_action=Action({'x': middle_x - 2, 'y': 9}, LEFT)),
]

walls4 = [
    {'x': range(1, middle_x - 2), 'y': middle_y - 1},
    {'x': range(middle_x + 1, CELLWIDTH - 1), 'y': middle_y - 1},
    {'x': middle_x - 1, 'y': range(1, middle_y - 1)},
    {'x': middle_x - 1, 'y': range(middle_y, CELLHEIGHT - 1)},
]

walls6 = [
    {'x': range(0, CELLWIDTH), 'y': middle_y},
    {'x': middle_x, 'y': range(0, CELLHEIGHT)},
]

walls5 = [
    {'x': range(0, CELLWIDTH), 'y': middle_y},
    {'x': middle_x, 'y': range(0, CELLHEIGHT)},
    {'x': range(0, CELLWIDTH / 4), 'y': CELLHEIGHT / 5},
    {'x': range(CELLWIDTH / 4 + 1, middle_x), 'y': CELLHEIGHT / 5},
    {'x': range(middle_x, middle_x + 11), 'y': CELLHEIGHT / 5},
    {'x': range(middle_x + 12, CELLWIDTH), 'y': CELLHEIGHT / 5},
    {'x': range(0, CELLWIDTH / 4), 'y': CELLHEIGHT / 5 + 19},
    {'x': range(CELLWIDTH / 4 + 1, middle_x), 'y': CELLHEIGHT / 5 + 19},
    {'x': range(middle_x + 1, CELLWIDTH - 12), 'y': CELLHEIGHT / 5 + 19},
    {'x': range(CELLWIDTH - 11, CELLWIDTH), 'y': CELLHEIGHT / 5 + 19},
        
]

level0 = Level(0, "Here We Go!", [], [], 3)
level1 = Level(0, "Walls!", [], walls1, 3)
level2 = Level(0, "Portals!", portals2, [], 5)
level3 = Level(0, "Trickier!", portals3, walls3, 5)
level4 = Level(0, "Can You Survive?!", portals2, walls4, 10)
level5 = Level(0, "Pure Skill!", portals2, walls5, 10)
level6 = Level(0, "Only Portals!", portals2, walls6, 10)

all_levels = [level0, level1, level2, level3, level4, level5, level6]
