from game_clock import *


def get_shifting_color(colors, pulse_time=2.0):
    num_colors = len(colors)
    one_color_time = pulse_time/num_colors

    mod_time = (current_time() % pulse_time)
    norm_time = mod_time/one_color_time
    ix1 = int(norm_time)
    ix2 = (ix1+1) % num_colors
    fraction = norm_time - ix1

    use_color = list(colors[0])
    for ii in range(3):
        use_color[ii] = int((1.0-fraction) * float(colors[ix1][ii]) + fraction * float(colors[ix2][ii]))

    use_color = tuple(use_color)
    return use_color


def get_pulse_color(colors, pulse_time=2.0, pulse_start_time=0.0):
    num_colors = len(colors)
    one_color_time = pulse_time/num_colors

    mod_time = ((current_time() - pulse_start_time) % pulse_time)
    norm_time = mod_time/one_color_time
    ix1 = int(norm_time)
    ix2 = (ix1+1) % num_colors
    fraction = norm_time - ix1

    use_color = list(colors[0])
    for ii in range(3):
        use_color[ii] = int((1.0-fraction) * float(colors[ix1][ii]) + fraction * float(colors[ix2][ii]))

    use_color = tuple(use_color)
    return use_color


def make_coord_list(coords):
    coord_list = []
    for coord in coords:
        coord_list = coord_list + coord
    return coord_list


def get_wall_coords(walls):
    all_wall_coords = []
    for item in walls:
        if type(item['x']) == list:
            for x in item['x']:
                all_wall_coords += [{'x': x, 'y': item['y']}]
        elif type(item['y']) == list:
            for y in item['y']:
                all_wall_coords += [{'x': item['x'], 'y': y}]
        else:
            all_wall_coords += [item]

    return all_wall_coords
    

def same_coord(coord1, coord2):
    return coord1['x'] == coord2['x'] and coord1['y'] == coord2['y']


def are_coords_safe(new_coords, existing_coords=None):
    if existing_coords is None:
        return True

    for new_coord in new_coords:
        for existing_coord in existing_coords:
            if same_coord(new_coord, existing_coord):
                return False

    return True


def closest_fruit(source, fruits):
    distances = [total_distance_to_target(source, fruit) for fruit in fruits]
    min_index = distances.index(min(distances))
    return fruits[min_index], distances[min_index]


def get_existing_fruit_coords(fruits):
    fruit_coords = []
    for fruit in fruits:
        if len(fruit) > 0:
            fruit_coords.append(fruit)

    return fruit_coords


def xy_distance_to_target(source, target):
    x_dist = target['x'] - source['x']
    y_dist = target['y'] - source['y']
    return x_dist, y_dist


def total_distance_to_target(source, target):
    x_dist, y_dist = xy_distance_to_target(source, target)
    total_dist = abs(x_dist) + abs(y_dist)
    return total_dist


def total_distance(coord1, coord2):
    x_dist = coord1['x'] - coord2['x']
    y_dist = coord1['y'] - coord2['y']
    total_dist = abs(x_dist) + abs(y_dist)
    return total_dist
