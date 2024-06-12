import matplotlib.pyplot as plt
import numpy as np

plt.style.use('Solarize_Light2')


def plot_amplitude_frequency(amplitude: list, frequency: int, show=False, file_name=None, title="Amplitude-Frequency"):
    plt.figure(figsize=(10, 4))
    plt.plot(frequency, amplitude)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.title(title)
    plt.grid(True)
    if show:
        plt.show()
    if file_name:
        plt.savefig(file_name, dpi=300, bbox_inches='tight')


def plot_spectrogram(data: list, rate: int, show=False, file_name=None, title="Spectrogram"):
    plt.figure(figsize=(10, 4))
    Pxx, freqs, bins, im = plt.specgram(data, Fs=rate)
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.title(title)
    plt.grid(True)
    cbar = plt.colorbar(im)
    cbar.set_label('Intensity (dB)')
    if show:
        plt.show()
    if file_name:
        plt.savefig(file_name, dpi=300, bbox_inches='tight')


def plot_amplitude_time(data, rate, show=False, file_name=None, title="Amplitude-Time"):
    plt.figure(figsize=(10, 4))
    time = np.arange(0, len(data)) / rate
    plt.plot(time, data)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.title(title)
    if show:
        plt.show()
    if file_name:
        plt.savefig(file_name, dpi=300, bbox_inches='tight')


def subplot_sepc_amp(data: list, rate: int, amplitude: list, frequency: int, show=False, file_name=None, title="Spectrogram and Amp-Freq"):
    fig, axs = plt.subplots(1, 2, )
    plt.subplot(1, 2, 1)
    plot_amplitude_frequency(
        amplitude, frequency, title="Original Amplitude-Frequency")
    plt.subplot(1, 2, 2)
    plot_spectrogram(data,
                     rate, title="Original Spectogram")
    if show:
        plt.show()
    if file_name:
        plt.savefig(file_name, dpi=300, bbox_inches='tight')
