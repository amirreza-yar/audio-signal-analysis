import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write
from scipy.fft import rfft, rfftfreq, irfft
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, 
                             QFileDialog, QSlider, QLabel, QHBoxLayout, QStyle, QSplitter, QFrame)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Function to read audio file
def read_voice(path):
    rate, data = read(path)
    amplitude = np.abs(rfft(data))
    frequency = rfftfreq(len(data), 1 / rate)
    return rate, data, amplitude, frequency

# Function to apply low-pass filter
def low_pass_filter(frequency, amplitude, cutoff):
    filtered_amplitude = np.where(frequency > cutoff, 0, amplitude)
    return filtered_amplitude

# Function to change speed
def change_speed(data, speed_factor):
    indices = np.round(np.arange(0, len(data), speed_factor))
    indices = indices[indices < len(data)].astype(int)
    return data[indices]

# Function to plot spectrogram
def plot_spectrogram(data, rate, title="Spectrogram"):
    fig, ax = plt.subplots()
    ax.specgram(data, Fs=rate)
    ax.set_xlabel('Time')
    ax.set_ylabel('Frequency')
    ax.set_title(title)
    return fig

# Function to create a frame with title and button
def create_audio_frame(title, play_callback):
    frame = QFrame()
    frame.setFrameShape(QFrame.StyledPanel)
    frame_layout = QVBoxLayout()
    frame_label = QLabel(title)
    frame_label.setAlignment(Qt.AlignCenter)
    play_button = QPushButton("Play/Pause")
    play_button.clicked.connect(play_callback)
    play_button.setEnabled(False)
    frame_layout.addWidget(frame_label)
    frame_layout.addWidget(play_button)
    frame.setLayout(frame_layout)
    return frame, play_button

# Main application window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audio Signal Analysis")

        self.rate = None
        self.data = None
        self.filtered_data = None
        self.speed_data = None
        self.reversed_data = None
        self.original_file_path = None

        self.player = QMediaPlayer()

        # Create main layout
        main_layout = QHBoxLayout()
        
        # Create splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Left widget with buttons and audio controls
        left_widget = QWidget()
        left_layout = QVBoxLayout()

        load_button = QPushButton("Load Audio")
        load_button.clicked.connect(self.load_audio)
        left_layout.addWidget(load_button)

        # Create frames for each audio type
        self.original_frame, self.play_original_button = create_audio_frame("Original Audio", self.play_original_audio)
        self.filtered_frame, self.play_filtered_button = create_audio_frame("Filtered Audio", self.play_filtered_audio)
        self.speed_frame, self.play_speed_button = create_audio_frame("Speed Changed Audio", self.play_speed_audio)
        self.reversed_frame, self.play_reversed_button = create_audio_frame("Reversed Audio", self.play_reversed_audio)
        
        left_layout.addWidget(self.original_frame)
        left_layout.addWidget(self.filtered_frame)
        left_layout.addWidget(self.speed_frame)
        left_layout.addWidget(self.reversed_frame)

        left_widget.setLayout(left_layout)
        splitter.addWidget(left_widget)
        
        # Right widget with plot
        self.canvas = FigureCanvas(plt.figure())
        splitter.addWidget(self.canvas)

        main_layout.addWidget(splitter)
        
        # Set splitter sizes
        splitter.setSizes([200, 800])
        
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
    
    def load_audio(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Audio File", "", "WAV files (*.wav)")
        if file_path:
            self.original_file_path = file_path
            self.rate, self.data, amplitude, frequency = read_voice(file_path)

            # Low-pass filter
            filtered_amplitude = low_pass_filter(frequency, amplitude, cutoff=1000)
            self.filtered_data = irfft(filtered_amplitude)
            self.filtered_file_path = file_path.replace('.wav', '_filtered.wav')
            write(self.filtered_file_path, self.rate, self.filtered_data.astype(np.int16))
            
            # Change speed
            self.speed_data = change_speed(self.data, speed_factor=1.5)
            self.speed_file_path = file_path.replace('.wav', '_speed.wav')
            write(self.speed_file_path, self.rate, self.speed_data.astype(np.int16))
            
            # Reverse audio
            self.reversed_data = self.data[::-1]
            self.reversed_file_path = file_path.replace('.wav', '_reversed.wav')
            write(self.reversed_file_path, self.rate, self.reversed_data.astype(np.int16))

            # Enable buttons
            self.play_original_button.setEnabled(True)
            self.play_filtered_button.setEnabled(True)
            self.play_speed_button.setEnabled(True)
            self.play_reversed_button.setEnabled(True)

            # Plot spectrogram of the original audio
            fig = plot_spectrogram(self.data, self.rate, title="Original Spectrogram")
            self.canvas.figure = fig
            self.canvas.draw()

    def play_audio(self, file_path):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
            self.player.play()
        
    def play_original_audio(self):
        if self.original_file_path:
            self.play_audio(self.original_file_path)

    def play_filtered_audio(self):
        if self.filtered_file_path:
            self.play_audio(self.filtered_file_path)

    def play_speed_audio(self):
        if self.speed_file_path:
            self.play_audio(self.speed_file_path)

    def play_reversed_audio(self):
        if self.reversed_file_path:
            self.play_audio(self.reversed_file_path)

# Main entry point
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
