import numpy as np


class VUSpectrum:
    input_ref = 2 << 15  # 0 dBFS is 32678 with an int16 signal

    sample_rate = 44100
    lower_band = 80
    upper_band = 16000

    def __init__(self, samples=2048):
        self.samples = samples
        # blackman might be faster?
        self.window = np.hanning(self.samples)
        self.bands = None
        self.bins = []

        self.last_levels = []
        self.peaks = []

    def set_bands(self, bands):
        if bands != self.bands:
            self.bands = bands
            self.peaks = [-61] * self.bands
            self.last_levels = [-61] * self.bands
            self.setup_bins()

    @staticmethod
    def logarithmic_distribution(low, high, num):
        multiplier = (high / low) ** (1 / (num - 1))
        return [low * (multiplier ** idx) for idx in range(num)]

    def setup_bins(self):
        bin_width = self.sample_rate / self.samples
        frequencies = VUSpectrum.logarithmic_distribution(self.lower_band, self.upper_band, self.bands + 1)
        centers = [freq / bin_width for freq in frequencies]
        bins = []
        for idx in range(self.bands):
            high = int((centers[idx + 1] - centers[idx]) / 2 + centers[idx])
            if idx == 0:
                # At least first bin, else <=40Hz bins or maximum one bin for first band
                lower = int(min(max(int(round(40 / bin_width)), 1), high - 1))
            else:
                lower = bins[-1][0]
            bins.append((lower, high))
        self.bins = bins[0: self.bands]

    def calculate(self, signal, ref=2 << 15):
        # Reduce peaks
        self.peaks = [p - 0.1 if p > -60 else p for p in self.peaks]

        # Process input
        x = signal * self.window  # multiply by window function
        sp = np.fft.rfft(x)  # Calculate real FFT
        # Scale the magnitude of FFT by window and factor of 2, because we are using half of FFT spectrum
        s_mag = np.abs(sp) * 2 / np.sum(self.window)
        # s_dbfs = 20 * np.log10(s_mag / ref)  # Convert to dBFS

        levels = []
        for index, bin in enumerate(self.bins):
            # Sum bins and calculate dBFS
            s = sum(s_mag[bin[0]: bin[1]]) / ref
            levels.append(20 * np.log10(s) if s != 0 else self.last_levels[len(levels)])
        # Apply some mean for smoother look
        levels = np.add(self.last_levels, levels) / 2

        self.last_levels = levels
        self.peaks = [max(self.peaks[idx], levels[idx]) for idx in range(self.bands)]
        return levels, self.peaks
