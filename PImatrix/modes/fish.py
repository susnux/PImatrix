import random

import numpy as np
from .. import led, CHANNEL_SPEED

small_fish = np.array(
    [[1, 0, 1, 1, 0],
     [1, 1, 1, 1, 1],
     [1, 0, 1, 1, 0]])

medium_fish = np.array(
    [[0, 0, 0, 1, 0, 0],
     [1, 0, 1, 1, 1, 0],
     [1, 1, 1, 1, 1, 1],
     [1, 0, 1, 1, 1, 0],
     [0, 0, 0, 1, 0, 0]]
)

big_fish = np.array(
    [  # [0, 0, 0, 0, 0, 1, 0, 0, 0],
        [1, 0, 0, 0, 1, 1, 1, 0, 0],
        [1, 1, 0, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 1, 1, 1, 1, 1, 0],
        [1, 0, 0, 0, 1, 1, 1, 0, 0],
        # [0, 0, 0, 0, 0, 1, 0, 0, 0]
    ]
)

angelfish = np.array(
    [
        [0, 0, 1, 1, 0, 0, 0],
        [1, 0, 0, 1, 1, 0, 0],
        [1, 1, 0, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 1, 1, 1, 0],
        [1, 0, 0, 1, 1, 0, 0],
        [0, 0, 1, 1, 0, 0, 0],
    ]
)


class Fish:
    def __init__(self):
        self.model = random.choices([small_fish, medium_fish, big_fish, angelfish], weights=[4, 4, 1, 2])[0]
        self.pos = [0, random.randint(0, led.HEIGHT)]
        self._last = 0

    def may_move(self, speed, next_fish):
        if next_fish is None or self.pos[0] < (next_fish.pos[0] - next_fish.model.shape[1] - 2):
            if random.choices([0, 1], weights=[250, speed])[0] == 1:
                self.pos[0] += 1
        dir = random.choices([self._last, 0, -1, 1], weights=np.array([48, 300, 1, 1]))[0]
        if 0 < (self.pos[1] + dir) < led.HEIGHT:
            self.pos[1] += dir
            self._last = dir


BLUE = 0x0000FF
ORANGE = 0xFF9B00


def run(local: object, data: [], leds):
    speed = 1 + data[CHANNEL_SPEED] / 64
    if not hasattr(local, "fish"):
        local.fish = []

    if len(local.fish) == 0 or (local.fish[0].pos[0] > local.fish[0].model.shape[0] + 1):
        if random.randint(0, 6) == 1:
            local.fish.insert(0, Fish())

    for idx in range(len(local.fish) - 1, -1, -1):
        fish = local.fish[idx]
        fish.may_move(speed, local.fish[idx + 1] if idx + 1 < len(local.fish) else None)
        if fish.pos[0] > fish.model.shape[0] + led.WIDTH:
            local.fish.remove(fish)

    # Set background color
    for y in range(led.HEIGHT):
        color = (((8 - y) * 25) << 8) | BLUE
        for x in range(led.WIDTH):
            leds.set_led(x, y, color)

    # Render fish
    for fish in local.fish:
        diff_y = fish.model.shape[0] // 2
        diff_x = fish.model.shape[1] - 1
        coords = list(zip(*np.where(fish.model == 1)))
        for y, x in coords:
            x = int(x - diff_x + fish.pos[0])
            y = int(y - diff_y + fish.pos[1])
            if 0 <= x < led.WIDTH and 0 <= y < led.HEIGHT:
                leds.set_led(x, y, ORANGE)
    return True
