# Audio Signal Processing and Analysis

This repository contains a comprehensive suite of tools and scripts for processing and analyzing audio signals. It includes functionalities for reading, filtering, manipulating, and visualizing audio data. The project utilizes Python libraries such as `numpy`, `scipy`, and `matplotlib` to perform tasks like noise reduction, speed alteration, frequency domain filtering, audio reversal, and sound mixing. The repository also features functions to generate and display spectrograms, providing a visual representation of the audio signals over time.

## Key Features

- **Read and Write WAV Files**: Efficiently read and write WAV audio files using `scipy.io.wavfile`.
- **Noise Reduction**: Apply low-pass filters to remove noise from audio signals.
- **Speed Alteration**: Change the playback speed of audio files.
- **Audio Reversal**: Reverse audio signals.
- **Sound Mixing**: Combine multiple audio files in the frequency domain.
- **Visualization**: Generate and visualize amplitude-frequency plots and spectrograms.

## Installation

Ensure you have the following Python libraries installed:
- `numpy`
- `scipy`
- `matplotlib`

You can install them using pip:
```bash
pip install numpy scipy matplotlib
```
To use jupyter notebook file ensure you have the following Python libraries installed:
- `notebook`
- `IPython`

You can install them using pip:
```bash
pip install notebook IPython
```
Also to use the gui ensure you have the following Python libraries installed:
- `PyQt5`

You can install them using pip:
```bash
pip install PyQt5
```
## Usage
#### Recording Audio

To record audio using your microphone:

```python
from audio_playback import record_audio

record_audio(duration=10, rate=44100, filename="sample_audio")
```
#### Playing Audio

To play an audio file:

```python
from scipy.io import wavfile
from audio_playback import play_audio

rate, data = wavfile.read('sample_audio.wav')
play_audio(data, rate)
```
#### Processing Audio

To process an audio file (e.g., noise reduction, speed change, reversal):

```python
from audio_analysis.analysis import AudioAnalysis, save_outputs
from pathlib import Path

# Initialize the AudioAnalysis with the sample audio file
sample_audio = AudioAnalysis(path='sample_audio.wav')

# Create a directory to save the processed audio files
save_dir = Path('processed_audio')
if not save_dir.exists():
    save_dir.mkdir(parents=True, exist_ok=True)

# Apply multi-band stop filter for noise cancellation and save the output
noise_canceled_audio_amplitude, noise_canceled_audio_data = sample_audio.multi_band_stop_filter([1000, 5000, 7000], [14, 14, 14])
save_outputs(noise_canceled_audio_amplitude, noise_canceled_audio_data, sample_audio.frequency, sample_audio.rate, file_dir_name=save_dir / 'clean_audio')

# Initialize AudioAnalysis with the noise-canceled audio for further processing
clean_audio = AudioAnalysis(audio_data={'rate': sample_audio.rate, 'data': noise_canceled_audio_data, 'amplitude': noise_canceled_audio_amplitude, 'frequency': sample_audio.frequency})

# Change the speed of the audio (x2) and save the output
fast_audio_x2_data, fast_audio_x2_amp, fast_audio_x2_freq, fast_audio_x2_rate = clean_audio.change_speed(2)
save_outputs(fast_audio_x2_amp, fast_audio_x2_data, fast_audio_x2_freq, clean_audio.rate, file_dir_name=save_dir / 'fast_audio_x2')

# Change the speed of the audio (x0.5) and save the output
slow_audio_x_half_data, slow_audio_x_half_amp, slow_audio_x_half_freq, slow_audio_x_half_rate = clean_audio.change_speed(0.5)
save_outputs(slow_audio_x_half_amp, slow_audio_x_half_data, slow_audio_x_half_freq, clean_audio.rate, file_dir_name=save_dir / 'slow_audio_x_half')

# Reverse the audio and save the output
reversed_data, reversed_amp = clean_audio.reverse_voice()
save_outputs(reversed_amp, reversed_data, clean_audio.frequency, clean_audio.rate, file_dir_name=save_dir / 'reversed_audio')
```

#### Visualization

To generate and save visualizations of the audio data:

```python
from audio_analysis.plotlib import plot_amplitude_time, plot_amplitude_frequency, plot_spectrogram

# Plot amplitude over time
plot_amplitude_time(data, rate, file_name='amplitude_time.png')

# Plot amplitude-frequency spectrum
amplitude = np.abs(np.fft.rfft(data))
frequency = np.fft.rfftfreq(len(data), 1/rate)
plot_amplitude_frequency(amplitude, frequency, file_name='amplitude_frequency.png')

# Plot spectrogram
plot_spectrogram(data, rate, file_name='spectrogram.png')
```
## License

This project is licensed under the MIT License.
