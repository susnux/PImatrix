from rpi_ws281x import PixelStrip, WS2811_STRIP_GRB

# Matrix:
WIDTH = 13 + 25
HEIGHT = 8
# LED configuration.
LED_COUNT = WIDTH * HEIGHT  # How many LEDs to light.
LED_DMA_NUM = 10  # DMA channel to use, can be 0-14.
LED_GPIO = 21  # GPIO connected to the LED signal line.  Must support PWM!


class LEDs(PixelStrip):
    def __init__(self):
        # TODO: Check if GRB or RGB
        super().__init__(LED_COUNT, LED_GPIO, dma=LED_DMA_NUM, strip_type=WS2811_STRIP_GRB)
        self.begin()

    def set_led(self, x, y=None, color=0x000000):
        if y is None:
            y = int(x / WIDTH)
            x -= y * WIDTH
        if y % 2 == 1:
            x = WIDTH - x - 1
        self.setPixelColor(x + WIDTH * y, color)

    def get_led(self, x, y):
        if y % 2 == 1:
            x = WIDTH - x - 1
        return self.getPixelColor(x + WIDTH * y)
