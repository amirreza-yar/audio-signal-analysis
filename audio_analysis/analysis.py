import numpy as np
from scipy.io import wavfile
from scipy.fft import rfft, rfftfreq

from .plotlib import plot_amplitude_time, plot_amplitude_frequency, plot_spectrogram


class AudioAnalysis:

    def __init__(self, path=None, audio_data=None) -> None:
        self.rate, self.data, self.amplitude, self.frequency = self.read_voice(
            path=path, audio_data=audio_data)

    def read_voice(self, path, audio_data):
        if path:
            rate, data = wavfile.read(path)
            amplitude = rfft(data)
            frequency = rfftfreq(len(data), 1/rate)
            return rate, data, amplitude, frequency
        if audio_data:
            return audio_data['rate'], audio_data['data'], audio_data['amplitude'], audio_data['frequency']

    def change_speed(self, speed_factor):
        indices = np.round(
            np.arange(0, len(self.data), speed_factor)).astype(int)
        indices = indices[indices < len(self.data)]
        changed_data = self.data[indices]

        # Calculate the new amplitude
        new_amplitude = np.abs(rfft(changed_data))

        # Calculate the new frequency
        new_frequency = rfftfreq(len(changed_data), 1 / self.rate)

        # The rate is adjusted by the speed factor
        new_rate = int(self.rate / speed_factor)
        return changed_data, new_amplitude, new_frequency, new_rate

    def reverse_voice(self):
        new_data = self.data[::-1]
        # Calculate the new amplitude
        new_amplitude = np.abs(rfft(new_data))
        return new_data, new_amplitude

    def low_pass_filter(self, cutoff_freq):
        filtered_amplitude = np.where(
            self.frequency > cutoff_freq, 0, self.amplitude)
        return filtered_amplitude

    def band_stop_filter(self, band_freq, band_width):
        low_cutoff = band_freq - band_width / 2
        high_cutoff = band_freq + band_width / 2
        filtered_amplitude = np.where((self.frequency >= low_cutoff) & (
            self.frequency <= high_cutoff), 0, self.amplitude)
        filtered_data = np.fft.irfft(filtered_amplitude)
        return filtered_amplitude, filtered_data

    def multi_band_stop_filter(self, band_freqs: list, band_widths: list):
        filtered_amplitude = self.amplitude.copy()
        for band_freq, band_width in zip(band_freqs, band_widths):
            low_cutoff = band_freq - band_width / 2
            high_cutoff = band_freq + band_width / 2
            band_mask = (self.frequency >= low_cutoff) & (
                self.frequency <= high_cutoff)
            filtered_amplitude[band_mask] = 0
        filtered_data = np.fft.irfft(filtered_amplitude)
        return filtered_amplitude, filtered_data


def mix_voices(data_list, rate_list):
    min_length = min(len(data) for data in data_list)
    mixed_data = np.zeros(min_length)

    for data in data_list:
        mixed_data += data[:min_length]

    mixed_data /= len(data_list)
    return rate_list[0], mixed_data


def write_voice(data, rate, path):
    wavfile.write(path, rate, data.astype(np.int16))


def amp_to_data(amplitude):
    return np.fft.irfft(amplitude)


def save_outputs(amplitude, data, frequency, rate, file_dir_name):
    write_voice(data, rate,
                f"{file_dir_name}.wav")
    plot_amplitude_time(data,
                        rate, file_name=f"{file_dir_name}_data.png")
    plot_spectrogram(data,
                     rate, file_name=f"{file_dir_name}_spectogram.png")
    plot_amplitude_frequency(amplitude,
                             frequency, file_name=f"{file_dir_name}_amplitude.png")
