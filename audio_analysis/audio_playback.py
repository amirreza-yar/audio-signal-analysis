"""
audio_playback.py
This module provides functions for recording and playing back audio using the sounddevice library.
"""

import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

def record_audio(duration=15, rate=44100, filename="sample_audio"):
    """
    Record audio from the microphone.
    
    Args:
        duration (int): Duration of the recording in seconds.
        rate (int): Sampling rate.
        filename (str): Filename to save the recorded audio.
    """
    print("Recording...")
    audio_data = sd.rec(int(duration * rate), samplerate=rate, channels=1, dtype='int16')
    sd.wait()
    print("Recording finished.")
    write(f"{filename}.wav", rate, audio_data)
    print(f"Audio recorded and saved as {filename}.")

def play_audio(audio_data, rate):
    """
    Play audio data.
    
    Args:
        audio_data (np.ndarray): Audio data to play.
        rate (int): Sampling rate.
    """
    print("Playing back...")
    sd.play(audio_data, rate)
    sd.wait()
    print("Playback finished.")

