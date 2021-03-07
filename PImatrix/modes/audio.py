import time
import numpy as np
from colorsys import hsv_to_rgb

from .. import MAX_CHANNEL, led, vuspectrum
from .color_modes import rgb_as_color_f


CHANNEL_SPECTRUM_MODE = MAX_CHANNEL + 1
CHANNEL_SPECTRUM_BANDS = CHANNEL_SPECTRUM_MODE + 1


def __rainbow(steps):
    return [rgb_as_color_f(*hsv_to_rgb((2 / 3) * ((steps - 1 - x) / (steps - 1)), 1, 1)) for x in range(steps)]


def __read_audio(local):
    samples = 2048
    sample_rate = 44100
    # DEBUG:
    if not hasattr(local, "stream"):
        import wave

        local.stream = wave.open("/tmp/last.wav", "rb")
    signal = local.stream.readframes(samples)
    time.sleep(samples / sample_rate)

    # PRODUCTION:
    # if not hasattr(local, "stream"):
    #    local._audio = pyaudio.PyAudio()
    #    local.stream = local._audio.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True,
    #                                     frames_per_buffer=samples)
    # signal = self.stream.read(self.samples)
    return np.frombuffer(signal, dtype=np.int16)


def vu_meter(local, data: [], leds):
    if not hasattr(local, "scale"):
        local.scale = [-4, -8, -12, -16, -20, -28, -30, -40, -60]

    signal = __read_audio(local)
    signal = signal / (2 << 15)
    volume = 20 * np.log10(np.sqrt(np.sum(np.square(signal*2)) / len(signal)) * np.sqrt(2))
    if volume == np.nan:
        return True

    for x in range(led.WIDTH - 1, -1, -1):
        color = 0
        num = int(x / (led.WIDTH / len(local.scale)))
        if volume >= local.scale[num]:
            if num == 0:
                color = 0xFF0000
            elif num < 3:
                color = 0xFFFF00
            else:
                color = 0x00FF00
        for y in range(led.HEIGHT):
            leds.set_led(led.WIDTH-x-1, y, color)
    return True


def spectrum(local, data: [], leds):
    def color_normal():
        clr = None
        if levels[band_num] >= local.scale[y]:
            if y == led.HEIGHT - 1:
                clr = 0xFF0000
            elif y > led.HEIGHT - 3:
                clr = 0xFFFF00
            else:
                clr = 0x00FF00
        return clr or 0

    def color_rainbow():
        if not hasattr(local, "rainbow_color"):
            local.rainbow_color = __rainbow(local.vu.bands)
        if levels[band_num] >= local.scale[y]:
            return local.rainbow_color[band_num]
        return 0

    def color_rainbow_bar():
        if not hasattr(local, "rainbow_bar"):
            local.rainbow_bar = __rainbow(led.HEIGHT)
        if levels[band_num] >= local.scale[y]:
            return local.rainbow_bar[y]
        return 0

    def show_peaks():
        if local.scale[y + 1] < peaks[band_num] >= local.scale[y]:
            return 0xFFFFFF
        return color

    # Mode: 0 default Spectrum
    #       1 same as 0 but without peaks
    #       2 Rainbow spectrum (like 0)
    #       3 Rainbow spectrum without peaks
    #       4 Rainbow bars
    #       5 Rainbow bars without peaks
    #       6 Endless horizontal spectrum (scrolling)
    if not hasattr(local, "vu"):
        local.i = 0
        local.vu = vuspectrum.VUSpectrum()
        local.vu.set_bands(data[CHANNEL_SPECTRUM_BANDS] if data[CHANNEL_SPECTRUM_BANDS] != 0 else 8)
        local.scale = vuspectrum.VUSpectrum.logarithmic_distribution(-1, -60, led.HEIGHT)
        # as 0dB does not work for distribution, lets patch it (0dBFS is max)
        local.scale[0] = 0
        # Every signal below -70 dBFS is assumed to be noise
        local.scale += [-70]
        local.scale.reverse()

    # In endless mode bands equal led Height
    if data[CHANNEL_SPECTRUM_MODE] == 6:
        local.vu.set_bands(led.HEIGHT)
    else:
        local.vu.set_bands(data[CHANNEL_SPECTRUM_BANDS])

    levels, peaks = local.vu.calculate(__read_audio(local))

    if data[CHANNEL_SPECTRUM_MODE] != 6:
        for x in range(led.WIDTH):
            for y in range(led.HEIGHT):
                band_num = int(x / (led.WIDTH / local.vu.bands))
                if data[CHANNEL_SPECTRUM_MODE] < 2:
                    color = color_normal()
                elif data[CHANNEL_SPECTRUM_MODE] < 4:
                    color = color_rainbow()
                elif data[CHANNEL_SPECTRUM_MODE] < 6:
                    color = color_rainbow_bar()
                if data[CHANNEL_SPECTRUM_MODE] % 2 == 0:
                    show_peaks()
                leds.set_led(x, led.HEIGHT - y - 1, color)
    else:
        local.i += 1
        #if local.i % 20 != 1:
        #    return True
        # Endless scroll mode
        levels = [(level + 70) / 70 for level in levels]
        for x in range(led.WIDTH - 1, 0, -1):
            for y in range(led.HEIGHT):
                leds.set_led(x, y, leds.get_led(x - 1, y))
                if x == 1:
                    leds.set_led(0, y, rgb_as_color(*hsv_to_rgb(4 / 6 - 4 / 6 * levels[y], 1, 1)))
    return True



