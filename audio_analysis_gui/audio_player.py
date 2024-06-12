import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QSlider, QLabel, QHBoxLayout, QStyle
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt


class AudioPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.player = QMediaPlayer()
        self.player.durationChanged.connect(self.update_duration)
        self.player.positionChanged.connect(self.update_position)

        layout = QVBoxLayout()

        self.play_button = QPushButton()
        self.play_button.setIcon(
            self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_button.clicked.connect(self.toggle_play_pause)
        self.play_button.setEnabled(False)

        self.stop_button = QPushButton()
        self.stop_button.setIcon(
            self.style().standardIcon(QStyle.SP_MediaStop))
        self.stop_button.clicked.connect(self.stop_audio)
        self.stop_button.setEnabled(False)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setEnabled(False)
        self.slider.sliderMoved.connect(self.set_position)

        self.time_label = QLabel("00:00 / 00:00")

        controls = QHBoxLayout()
        controls.addWidget(self.play_button)
        controls.addWidget(self.stop_button)
        controls.addWidget(self.slider)
        controls.addWidget(self.time_label)

        layout.addLayout(controls)
        self.setLayout(layout)

    def load_audio(self, file_path):
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))
        self.play_button.setEnabled(True)
        self.stop_button.setEnabled(True)
        self.slider.setEnabled(True)

    def toggle_play_pause(self):
        print(self.player.state())
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.play_button.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))
        else:
            self.player.play()
            self.play_button.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))

    def stop_audio(self):
        self.player.stop()
        self.play_button.setIcon(
            self.style().standardIcon(QStyle.SP_MediaPlay))

    def set_position(self, position):
        self.player.setPosition(position)

    def update_duration(self, duration):
        self.slider.setRange(0, duration)
        self.update_time_label(duration, self.player.position())

    def update_position(self, position):
        self.slider.setValue(position)
        self.update_time_label(self.player.duration(), position)

    def update_time_label(self, duration, position):
        total_time = self.format_time(duration)
        current_time = self.format_time(position)
        self.time_label.setText(f"{current_time} / {total_time}")

    def format_time(self, ms):
        seconds = ms // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"
