"""
main.py
This script demonstrates the usage of the AudioAnalysis class for processing audio files.
It applies noise reduction, changes the speed of the audio, and reverses the audio.
The processed audio and their respective plots are saved in the specified directory.
"""

from audio_analysis.analysis import AudioAnalysis, save_outputs
from pathlib import Path

# Initialize the AudioAnalysis with the sample audio file
sample_audio = AudioAnalysis(path='potc.wav')

# Create a directory to save the processed audio files
save_dir = Path(__file__).parent / 'newaudio'
if not save_dir.exists():
    save_dir.mkdir(parents=True, exist_ok=True)

# Apply multi-band stop filter for noise cancellation and save the output
noise_cancled_audio_amplitude, noise_cancled_audio_data = sample_audio.multi_band_stop_filter([
                                                                                              1000, 5000, 7000], [14, 14, 14])
save_outputs(noise_cancled_audio_amplitude, noise_cancled_audio_data,
             sample_audio.frequency, sample_audio.rate, file_dir_name=save_dir / 'cleanpotc')

# Initialize AudioAnalysis with the noise-canceled audio for further processing
clean_audio = AudioAnalysis(audio_data={'rate': sample_audio.rate, 'data': noise_cancled_audio_data,
                            'amplitude': noise_cancled_audio_amplitude, 'frequency': sample_audio.frequency})

# Change the speed of the audio (x2) and save the output
fast_audio_x2_data, fast_audio_x2_amp, fast_audio_x2_freq, fast_audio_x2_rate = clean_audio.change_speed(
    2)
save_outputs(fast_audio_x2_amp, fast_audio_x2_data, fast_audio_x2_freq,
             clean_audio.rate, file_dir_name=save_dir / 'fastpotc_x2')

# Change the speed of the audio (x0.5) and save the output
slow_audio_x_half_data, slow_audio_x_half_amp, slow_audio_x_half_freq, slow_audio_x_half_rate = clean_audio.change_speed(
    0.5)
save_outputs(slow_audio_x_half_amp, slow_audio_x_half_data, slow_audio_x_half_freq,
             clean_audio.rate, file_dir_name=save_dir / 'slowpotc_x_half')

# Reverse the audio and save the output
reversed_data, reversed_amp = clean_audio.reverse_voice()
save_outputs(reversed_amp, reversed_data, clean_audio.frequency,
             clean_audio.rate, file_dir_name=save_dir / 'revpotc')
