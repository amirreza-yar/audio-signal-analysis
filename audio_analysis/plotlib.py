"""
plotlib.py
This module provides functions to plot various aspects of audio data, including amplitude over time, amplitude-frequency spectrum, and spectrograms.
"""

import matplotlib.pyplot as plt
import numpy as np

plt.style.use('Solarize_Light2')


def plot_amplitude_frequency(amplitude, frequency, show=False, file_name=None, title="Amplitude-Frequency"):
    """
    Plot the amplitude-frequency spectrum.

    Args:
        amplitude (np.ndarray): Amplitude spectrum.
        frequency (np.ndarray): Frequency spectrum.
        show (bool): Whether to display the plot.
        file_name (str): Filename to save the plot.
        title (str): Title of the plot.
    """
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


def plot_spectrogram(data, rate, show=False, file_name=None, title="Spectrogram"):
    """
    Plot the spectrogram of the audio data.

    Args:
        data (np.ndarray): Audio data.
        rate (int): Sampling rate.
        show (bool): Whether to display the plot.
        file_name (str): Filename to save the plot.
        title (str): Title of the plot.
    """
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
    """
    Plot the amplitude of the audio data over time.

    Args:
        data (np.ndarray): Audio data.
        rate (int): Sampling rate.
        show (bool): Whether to display the plot.
        file_name (str): Filename to save the plot.
        title (str): Title of the plot.
    """
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


def subplot_spec_amp(data, rate, amplitude, frequency, show=False, file_name=None, title="Spectrogram and Amplitude-Frequency"):
    """
    Create a subplot with the spectrogram and amplitude-frequency spectrum.

    Args:
        data (np.ndarray): Audio data.
        rate (int): Sampling rate.
        amplitude (np.ndarray): Amplitude spectrum.
        frequency (np.ndarray): Frequency spectrum.
        show (bool): Whether to display the plot.
        file_name (str): Filename to save the plot.
        title (str): Title of the subplot.
    """
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plot_amplitude_frequency(amplitude, frequency, title="Amplitude-Frequency")
    plt.subplot(1, 2, 2)
    plot_spectrogram(data, rate, title="Spectrogram")
    if show:
        plt.show()
    if file_name:
        plt.savefig(file_name, dpi=300, bbox_inches='tight')
