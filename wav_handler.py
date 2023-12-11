import os
from pydub import AudioSegment
from tkinter import filedialog
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
import wave
import matplotlib.pyplot as plt

class AudioAnalyzer:
    def __init__(self):
        self.file_path = None
        self.signal = None

    def mp3_to_wav(self, mp3_audio):
        dst, ext = os.path.splitext(mp3_audio)
        wav_audio = dst + '.wav'

        sound = AudioSegment.from_mp3(mp3_audio)
        sound.export(wav_audio, format='wav')
        return sound

    def get_audio_files(self):
        audio_files = []
        for file in os.listdir():
            if file.endswith('.wav'):
                audio_files.append(file)
            elif file.endswith('.mp3'):
                self.mp3_to_wav(file)
                audio_files.append(file)
        return audio_files

    def load_audio_file(self):
        file_types = ["*.wav", "*.mp3"]
        self.file_path = filedialog.askopenfilename(title="Select Audio File", filetypes=[("Audio Files", file_types)])

        if self.file_path:
            self.signal = self.plot_wave(self.file_path)
            show_freq_button.pack()

    def plot_wave(self, file_path):
        wave_file = wave.open(file_path, 'rb')
        framerate = wave_file.getframerate()
        frames = wave_file.readframes(-1)
        signal = np.frombuffer(frames, dtype=np.int16)

        fig, ax = plt.subplots(figsize=(8, 6))

        time = np.linspace(0, len(signal) / framerate, num=len(signal))
        plt.plot(time, signal, color='red')

        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.title('Clap Audio')

        image_path = 'waveform_plot.png'
        plt.savefig(image_path)

        img = Image.open(image_path)
        photo = ImageTk.PhotoImage(img)
        label.config(image=photo)
        label.image = photo

        # Return the signal array
        return signal

    def plot_frequency_spectrum(self):
        if self.file_path:
            wave_file = wave.open(self.file_path, 'rb')
            framerate = wave_file.getframerate()
            frames = wave_file.readframes(-1)
            signal = np.frombuffer(frames, dtype=np.int16)

            fig, ax = plt.subplots(figsize=(8, 6))

            result = plt.specgram(signal, NFFT=1024, Fs=framerate, noverlap=512, cmap='viridis')
            Sxx = result[2]

            plt.xlabel('Time (s)')
            plt.ylabel('Frequency (Hz)')
            plt.title('Clap Audio')

           
            plt.show()

# Setting up the main window with tkinter
root = tk.Tk()
root.title("Waveform")

audio_analyzer = AudioAnalyzer()

# button to load an audio file
load_button = tk.Button(root, text="Load Audio File", command=audio_analyzer.load_audio_file)
load_button.pack(pady=20, padx=30)

#label to display the waveform image
label = tk.Label(root)
label.pack()

#  button to show frequency graph
show_freq_button = tk.Button(root, text="Show Frequency", command=audio_analyzer.plot_frequency_spectrum)

# Call 
root.mainloop()
