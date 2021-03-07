from colorsys import hsv_to_rgb


def rgb_as_color_f(r: float, g: float, b: float):
    return rgb_as_color(int(r * 255), int(g * 255), int(b * 255))


def rgb_as_color(r: int, g: int, b: int):
    return r << 16 | g << 8 | b


def rainbow(steps):
    return [rgb_as_color_f(*hsv_to_rgb((2 / 3) * ((steps - 1 - x) / (steps - 1)), 1, 1)) for x in range(steps)]


def calc_speed(speed, slowest=180, fastest=10):
    assert fastest < slowest
    # Target rate is 50 Hz
    per_second = 1 / 0.02
    m = (fastest - slowest) / 255
    return 1 / (m * per_second * speed + slowest * per_second)
