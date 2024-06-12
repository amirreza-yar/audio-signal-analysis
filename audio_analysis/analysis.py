"""
analysis.py
This module provides the AudioAnalysis class and utility functions for processing audio signals.
It includes functionalities for reading audio files, applying filters, changing speed, reversing audio, and saving outputs.
"""

import numpy as np
from scipy.io import wavfile
from scipy.fft import rfft, rfftfreq

from .plotlib import plot_amplitude_time, plot_amplitude_frequency, plot_spectrogram

class AudioAnalysis:
    """
    AudioAnalysis class for processing audio signals.
    
    Attributes:
        rate (int): Sampling rate of the audio.
        data (np.ndarray): Audio data.
        amplitude (np.ndarray): Amplitude spectrum of the audio.
        frequency (np.ndarray): Frequency spectrum of the audio.
    """

    def __init__(self, path=None, audio_data=None) -> None:
        self.rate, self.data, self.amplitude, self.frequency = self.read_voice(path=path, audio_data=audio_data)

    def read_voice(self, path, audio_data):
        """
        Read an audio file or initialize from existing audio data.
        
        Args:
            path (str): Path to the audio file.
            audio_data (dict): Dictionary containing rate, data, amplitude, and frequency.
        
        Returns:
            tuple: rate, data, amplitude, frequency
        """
        if path:
            rate, data = wavfile.read(path)
            amplitude = rfft(data)
            frequency = rfftfreq(len(data), 1 / rate)
            return rate, data, amplitude, frequency
        if audio_data:
            return audio_data['rate'], audio_data['data'], audio_data['amplitude'], audio_data['frequency']

    def change_speed(self, speed_factor):
        """
        Change the speed of the audio.
        
        Args:
            speed_factor (float): Factor by which to change the speed.
        
        Returns:
            tuple: changed_data, new_amplitude, new_frequency, new_rate
        """
        indices = np.round(np.arange(0, len(self.data), speed_factor)).astype(int)
        indices = indices[indices < len(self.data)]
        changed_data = self.data[indices]

        new_amplitude = np.abs(rfft(changed_data))
        new_frequency = rfftfreq(len(changed_data), 1 / self.rate)
        new_rate = int(self.rate / speed_factor)
        return changed_data, new_amplitude, new_frequency, new_rate

    def reverse_voice(self):
        """
        Reverse the audio data.
        
        Returns:
            tuple: new_data, new_amplitude
        """
        new_data = self.data[::-1]
        new_amplitude = np.abs(rfft(new_data))
        return new_data, new_amplitude

    def low_pass_filter(self, cutoff_freq):
        """
        Apply a low-pass filter to the audio data.
        
        Args:
            cutoff_freq (float): Cutoff frequency for the low-pass filter.
        
        Returns:
            np.ndarray: Filtered amplitude
        """
        filtered_amplitude = np.where(self.frequency > cutoff_freq, 0, self.amplitude)
        return filtered_amplitude

    def band_stop_filter(self, band_freq, band_width):
        """
        Apply a band-stop filter to the audio data.
        
        Args:
            band_freq (float): Central frequency of the stop band.
            band_width (float): Width of the stop band.
        
        Returns:
            tuple: filtered_amplitude, filtered_data
        """
        low_cutoff = band_freq - band_width / 2
        high_cutoff = band_freq + band_width / 2
        filtered_amplitude = np.where((self.frequency >= low_cutoff) & (self.frequency <= high_cutoff), 0, self.amplitude)
        filtered_data = np.fft.irfft(filtered_amplitude)
        return filtered_amplitude, filtered_data

    def multi_band_stop_filter(self, band_freqs: list, band_widths: list):
        """
        Apply multiple band-stop filters to the audio data.
        
        Args:
            band_freqs (list): List of central frequencies for the stop bands.
            band_widths (list): List of widths for the stop bands.
        
        Returns:
            tuple: filtered_amplitude, filtered_data
        """
        filtered_amplitude = self.amplitude.copy()
        for band_freq, band_width in zip(band_freqs, band_widths):
            low_cutoff = band_freq - band_width / 2
            high_cutoff = band_freq + band_width / 2
            band_mask = (self.frequency >= low_cutoff) & (self.frequency <= high_cutoff)
            filtered_amplitude[band_mask] = 0
        filtered_data = np.fft.irfft(filtered_amplitude)
        return filtered_amplitude, filtered_data

def mix_voices(data_list, rate_list):
    """
    Mix multiple audio signals together.
    
    Args:
        data_list (list): List of audio data arrays.
        rate_list (list): List of sampling rates for the audio data.
    
    Returns:
        tuple: rate, mixed_data
    """
    min_length = min(len(data) for data in data_list)
    mixed_data = np.zeros(min_length)

    for data in data_list:
        mixed_data += data[:min_length]

    mixed_data /= len(data_list)
    return rate_list[0], mixed_data

def write_voice(data, rate, path):
    """
    Write audio data to a WAV file.
    
    Args:
        data (np.ndarray): Audio data.
        rate (int): Sampling rate.
        path (str): Path to save the WAV file.
    """
    wavfile.write(path, rate, data.astype(np.int16))

def amp_to_data(amplitude):
    """
    Convert amplitude spectrum back to audio data.
    
    Args:
        amplitude (np.ndarray): Amplitude spectrum.
    
    Returns:
        np.ndarray: Audio data.
    """
    return np.fft.irfft(amplitude)

def save_outputs(amplitude, data, frequency, rate, file_dir_name):
    """
    Save audio data and generate plots for amplitude and spectrogram.
    
    Args:
        amplitude (np.ndarray): Amplitude spectrum.
        data (np.ndarray): Audio data.
        frequency (np.ndarray): Frequency spectrum.
        rate (int): Sampling rate.
        file_dir_name (str): Directory name to save the files.
    """
    write_voice(data, rate, f"{file_dir_name}.wav")
    plot_amplitude_time(data, rate, file_name=f"{file_dir_name}_data.png")
    plot_spectrogram(data, rate, file_name=f"{file_dir_name}_spectogram.png")
    plot_amplitude_frequency(amplitude, frequency, file_name=f"{file_dir_name}_amplitude.png")
