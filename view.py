# This file will show how the model is presented and interacted with by
# the user

from model import *
import os
from tkinter import filedialog
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
import wave
import matplotlib.pyplot as plt


def load_audio_file():
    #filedialogue allows user to pick file w button
    #askopenfilename is just the request
    file_types = ["*.wav", "*.mp3"]
    file_path = filedialog.askopenfilename(title="Select Audio File", filetypes=[("Audio Files", file_types)])
    #checks if user selects a file
    if file_path:
        debugg(f"file_path: {file_path}")
        wave_file = clean_file(file_path)
        plot_wave(wave_file)
        plot_frequency_spectrum(wave_file)

def clean_file(file_path):
    # audio_file = open(file_path, 'rb')
    # debugg(f"audio_file: {audio_file.name}")
    # Checking if file is .mp3 and converting to .wav if so
    if (os.path.splitext(file_path))[1] == ".mp3":
        debugg(f"File extension: {(os.path.splitext(file_path))[1]}")
        wave_file = mp3_to_wav(file_path)
    else:
        wave_file = wave.open(file_path, 'rb')
    debugg(f"wave_file: {wave_file}")
    # Stripping channels and metadata
    wave_file = audio_stripper(wave_file)
    return wave_file

def plot_frequency_spectrum(file_path):
    # Load audio file
    wave_file = wave.open(file_path, 'rb')
    framerate = wave_file.getframerate()
    frames = wave_file.readframes(-1)
    signal = np.frombuffer(frames, dtype=np.int16)

   # Create a Matplotlib figure
    fig, ax = plt.subplots(figsize=(8, 6))

    # Calculate the Short-Time Fourier Transform (STFT)
    result = plt.specgram(signal, NFFT=1024, Fs=framerate, noverlap=512, cmap='viridis')
    Sxx = result[2]

    # Displays for the chart
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.title('Clap Audio')

    # PIL Image from the Matplotlib figure
    fig.canvas.draw()
    img = Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())

    # Display the image
    photo = ImageTk.PhotoImage(img)
    label.config(image=photo)
    label.image = photo

def plot_wave(file_path):
    # Load audio file
    wave_file = wave.open(file_path, 'rb')
    framerate = wave_file.getframerate()
    frames = wave_file.readframes(-1)
    signal = np.frombuffer(frames, dtype=np.int16)

    # Create a Matplotlib figure
    fig, ax = plt.subplots(figsize=(8, 6))

    # plot wave
    time = np.linspace(0, len(signal) / framerate, num=len(signal))
    plt.plot(time, signal, color='red')

    # Displays for the chart
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Clap Audio')

    #display as image instead of calling .show()
    #.show does not work for the wave
    image_path = 'waveform_plot.png'
    plt.savefig(image_path)

    #display image using tk
    img = Image.open(image_path)
    photo = ImageTk.PhotoImage(img)
    label.config(image=photo)
    label.image = photo

def file_gui():
    # Setting up main window with tkinter
    root = tk.Tk()
    root.title("Waveform")

    # Create a button to load an audio file
    load_button = tk.Button(root, text="Load Audio File", command=load_audio_file)
    load_button.pack(pady=20, padx=30)

    # Create a label to display the spectrogram image
    global label
    label = tk.Label(root)
    label.pack()

    # call 
    root.mainloop()


