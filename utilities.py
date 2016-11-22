from worm_clock import *


def get_shifting_color(colors, pulse_time=2.0):
    num_colors = len(colors)
    one_color_time = pulse_time/num_colors

    mod_time = (elapsed_time() % pulse_time)
    norm_time = mod_time/one_color_time
    ix1 = int(norm_time)
    ix2 = (ix1+1) % num_colors
    fraction = norm_time - ix1

    use_color = list(colors[0])
    for ii in range(3):
        use_color[ii] = int((1.0-fraction) * float(colors[ix1][ii]) + fraction * float(colors[ix2][ii]))

    use_color = tuple(use_color)
    return use_color
