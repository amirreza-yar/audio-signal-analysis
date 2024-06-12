import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

# A function to record the audio
def record_audio(duration=15, rate=44100, filename="sample_audio"):
    print("Recording...")
    audio_data = sd.rec(int(duration * rate), samplerate=rate, channels=1, dtype='int16')
    sd.wait()
    print("Recording finished.")
    write(f"{filename}.wav", rate, audio_data)
    print(f"Audio recorded and saved as {filename}.")

# A function to play the audio
def play_audio(audio_data, rate):
    print("Recording finished. Playing back...")
    sd.play(audio_data, rate)
    sd.wait()
    print("Playback finished.")