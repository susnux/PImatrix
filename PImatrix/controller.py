import time
import threading

from . import led, CHANNEL_MODE, CHANNEL_BRIGHTNESS
from .modes import fish, color_modes, audio


class Controller:
    def __init__(self, driver=led.LEDs):
        self.running = False
        self.leds = driver()
        self.data = [0] * 1024

    def set_data(self, payload, begin=0):
        self.data[begin: begin + len(payload)] = payload

    def run(self):
        modes = {
            0: Controller.blackout,
            1: color_modes.fade,
            2: color_modes.rainbow,
            3: fish.run,
            4: color_modes.static,
            5: audio.vu_meter,
            6: audio.spectrum}
        local = threading.local()
        function = modes.get(self.data[CHANNEL_MODE], Controller.blackout)
        self.running = True
        while self.running:
            begin = time.monotonic()
            brightness = self.data[CHANNEL_BRIGHTNESS]
            if brightness != self.leds.getBrightness():
                self.leds.setBrightness(brightness)
            self.running = function(local, self.data, self.leds)
            self.leds.show()
            sleep = 0.02 - (time.monotonic() - begin)
            if sleep > 0:
                time.sleep(sleep)

    @staticmethod
    def blackout(local, data, leds):
        for pos in range(led.WIDTH * led.HEIGHT):
            leds.setPixelColor(pos, 0)
        return False
