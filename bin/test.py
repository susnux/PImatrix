# Script used for testing the controller and developing new modes
# (openCV as LED replacement, yes overkill but it was installed locally ;-) )
import sys
import cv2 as cv
import numpy as np
from time import sleep
from PImatrix import controller, led


class FakeDriver:
    def __init__(self):
        self.buffer = [(0, 0, 0)] * (led.HEIGHT * led.WIDTH)
        self.brightness = 255
        self.image = np.ones((led.HEIGHT * 10, led.WIDTH * 10, 3), dtype=np.uint8)

    def getBrightness(self):
        return self.brightness

    def setBrightness(self, b):
        self.brightness = b

    def setPixelColor(self, pos, color):
        self.buffer[pos] = color & 255, (color >> 8) & 255, (color >> 16) & 255

    def set_led(self, x, y, color):
        self.setPixelColor(x + y * led.WIDTH, color)

    def get_led(self, x, y):
        b, g, r = self.buffer[x + y * led.WIDTH]
        return (r << 16) | (g << 8) | b

    def show(self):
        for index, color in enumerate(self.buffer):
            p0 = (index % led.WIDTH) * 10, index // led.WIDTH * 10
            p1 = ((index % led.WIDTH) + 1) * 10, (index // led.WIDTH + 1) * 10
            cv.rectangle(self.image, p0, p1, color, cv.FILLED)
        cv.imshow("display", self.image)
        cv.waitKey(1)
        sleep(.01)


c = controller.Controller(FakeDriver)
#       MODE   DIMMER    SPEED  RED   GREEN  BLUE  SPEC_MODE SPEC_BAND TEXT_MODE
data = [7,     255,      255,   255,      0,  255,         0,        8,      128]
data += [0] * (32 - len(data))
data += [ord(c) for c in "This is a test! :-)"]
c.set_data(data)
c.run()
sys.exit(1)
