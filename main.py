import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read

def read_voice(path):
    rate, data = read(path)
    amplitude = np.abs(np.fft.rfft(data))
    frequency = np.fft.rfftfreq(len(data), 1/rate)
    return rate, data, amplitude, frequency

def plot_amplitude_frequency(amplitude, frequency, title="Amplitude-Frequency"):
    plt.plot(frequency, amplitude)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.title(title)

def plot_spectrogram(data, rate, title="Spectrogram"):
    plt.specgram(data, Fs=rate)
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.title(title)

# Plotting all charts in subplots
fig, axs = plt.subplots(4, 2, figsize=(15, 20))

# Original audio
rate, data, amplitude, frequency = read_voice('data/audio/potc.wav')
plt.subplot(4, 2, 1)
plot_amplitude_frequency(amplitude, frequency, title="Original Amplitude-Frequency")
plt.subplot(4, 2, 2)
plot_spectrogram(data, rate, title="Original Spectrogram")

# Filtered audio
filtered_rate, filtered_data, filtered_amplitude, filtered_frequency = read_voice('data/newaudio/cleanpotc.wav')
plt.subplot(4, 2, 3)
plot_amplitude_frequency(filtered_amplitude, filtered_frequency, title="Filtered Amplitude-Frequency")
plt.subplot(4, 2, 4)
plot_spectrogram(filtered_data, filtered_rate, title="Filtered Spectrogram")

# Reversed audio
reversed_rate, reversed_data, reversed_amplitude, reversed_frequency = read_voice('data/newaudio/revpotc.wav')
plt.subplot(4, 2, 5)
plot_amplitude_frequency(reversed_amplitude, reversed_frequency, title="Reversed Amplitude-Frequency")
plt.subplot(4, 2, 6)
plot_spectrogram(reversed_data, reversed_rate, title="Reversed Spectrogram")

# Mixed audio
mixed_rate, mixed_data, mixed_amplitude, mixed_frequency = read_voice('data/newaudio/mixpotc.wav')
plt.subplot(4, 2, 7)
plot_amplitude_frequency(mixed_amplitude, mixed_frequency, title="Mixed Amplitude-Frequency")
plt.subplot(4, 2, 8)
plot_spectrogram(mixed_data, mixed_rate, title="Mixed Spectrogram")

# Adjust layout
plt.tight_layout()
plt.show()
