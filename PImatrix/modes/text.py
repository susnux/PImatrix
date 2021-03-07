import os
import pickle

from . import calc_speed, rgb_as_color, rainbow
from .. import CHANNEL_SPEED, led, CHANNEL_TEXT_BEGIN, CHANNEL_TEXT_END, CHANNEL_RED, CHANNEL_BLUE, CHANNEL_TEXT_MODE


def run(local, data: [], leds):
    speed = calc_speed(data[CHANNEL_SPEED], 5, 0.15)
    if not hasattr(local, "current_pos"):
        local.current_pos = 0
    else:
        local.current_pos += speed
    if not hasattr(local, "matrix") or local.current_pos >= (len(local.matrix[0]) + led.WIDTH):
        font = "font_7x3.pkl" if data[CHANNEL_TEXT_MODE] < 127 else "font_7x5.pkl"
        with open(os.path.dirname(__file__) + f"/data/{font}", "rb") as file:
            font = pickle.load(file)
        local.current_pos = 0
        local.matrix = [[0]]
        idx = 0
        while data[CHANNEL_TEXT_BEGIN + idx] != 0 and CHANNEL_TEXT_BEGIN + idx < CHANNEL_TEXT_END:
            char = font.get(data[CHANNEL_TEXT_BEGIN + idx], None)
            if char is None:
                char = font.get(ord("?"))
            # Char height changed
            while len(local.matrix) < len(char):
                local.matrix.insert(0, [0] * len(local.matrix[0]))
            offset = len(local.matrix) - len(char)
            for i in range(offset):
                local.matrix[i] += [0] * (len(char[0]) + 1)
            for i, row in enumerate(char):
                local.matrix[i + offset] += row + [0]
            idx += 1
        # Fill top
        while len(local.matrix) < led.HEIGHT:
            local.matrix.insert(0, [0] * len(local.matrix[0]))

    if data[CHANNEL_TEXT_MODE] % 127 == 0:
        local.color = [rgb_as_color(*data[CHANNEL_RED : CHANNEL_BLUE + 1])] * led.WIDTH
    else:
        local.color = rainbow(led.WIDTH)

    for y in range(led.HEIGHT):
        for x in range(led.WIDTH):
            if len(local.matrix[0]) <= led.WIDTH:
                leds.set_led(x, y, local.matrix[y][x] * local.color[x] if x < len(local.matrix[0]) else 0)
            else:
                m_x = int(local.current_pos - led.WIDTH + x)
                leds.set_led(x, y, local.matrix[y][m_x] * local.color[x] if 0 <= m_x < len(local.matrix[0]) else 0)
    return True
