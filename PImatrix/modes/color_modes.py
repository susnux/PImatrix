from colorsys import hsv_to_rgb

from .. import led, CHANNEL_SPEED


def rgb_as_color_f(r: float, g: float, b: float):
    return rgb_as_color(int(r*255), int(g*255), int(b*255))


def rgb_as_color(r: int, g: int, b: int):
    return r << 16 | g << 8 | b


def __calc_speed(speed):
    per_second = 1 / 0.02
    b = 180  # Slowest time for one circle in seconds
    m = -170 / 255  # 180 - 170 = 10 == 10 s for one circle (fastest)
    return 1 / (m * per_second * speed + b * per_second)


def fade(local, data: [], leds):
    if not hasattr(local, "current_step"):
        local.current_step = 0.0
    local.step = __calc_speed(data[CHANNEL_SPEED])
    color = rgb_as_color_f(*hsv_to_rgb(local.current_step, 1, 1))
    for p in range(led.WIDTH * led.HEIGHT):
        leds.setPixelColor(p, color)

    if local.current_step >= 1:
        local.current_step = 0
    else:
        local.current_step += local.step
    return True


def rainbow(local, data: [], leds):
    if not hasattr(local, "distance"):
        local.distance = 1 / led.WIDTH
        local.current_step = 0.0
    local.step = __calc_speed(data[CHANNEL_SPEED])

    for x in range(led.WIDTH):
        color = rgb_as_color_f(*hsv_to_rgb(local.current_step + local.distance * x, 1, 1))
        for y in range(led.HEIGHT):
            leds.set_led(x, y, color)

    local.current_step += local.step
    if local.current_step >= 1:
        local.current_step = 0
    return True


def static(local, data: [], leds):
    for y in range(led.HEIGHT):
        for x in range(led.WIDTH):
            leds.set_led(
                x,
                y,
                rgb_as_color(
                    data[110 + y * led.WIDTH * 3 + x * 3],
                    data[110 + y * led.WIDTH * 3 + x * 3 + 1],
                    data[110 + y * led.WIDTH * 3 + x * 3 + 2],
                ),
            )
    return True
