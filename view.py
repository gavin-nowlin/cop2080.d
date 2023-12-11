from seconds import *
from model import *
import os
from tkinter import filedialog
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
import wave
import matplotlib.pyplot as plt


def load_audio_file():
    # filedialogue allows user to pick file w button
    # askopenfilename is just the request
    file_types = ["*.wav", "*.mp3"]
    file_path = filedialog.askopenfilename(title="Select Audio File", filetypes=[("Audio Files", file_types)])
    #checks if user selects a file
    if file_path:
        debugg(f"file_path: {file_path}")
        global wave_file
        wave_file = clean_file(file_path)

        extra_data_button()
        plot_rt60(wave_file)
        show_audio_length(wave_file)
        show_rt60(wave_file)
        plot_wave(wave_file)
        plot_all_rt60s()


def clean_file(file_path):
    # audio_file = open(file_path, 'rb')
    # debugg(f"audio_file: {audio_file.name}")
    # Checking if file is .mp3 and converting to .wav if so
    if (os.path.splitext(file_path))[1] == ".mp3":
        debugg(f"File extension: {(os.path.splitext(file_path))[1]}")
        wave_file = mp3_to_wav(file_path)
    else:
        # wave_file = wave.open(file_path, 'rb')
        wave_file = file_path
    debugg(f"wave_file: {wave_file}")
    # Stripping channels and metadata
    # wave_file = audio_stripper(wave_file)
    return wave_file

def plot_rt60(file_path):
    # Specify a list of frequencies
    frequencies = [250, 1000, 5000]

    # Create a color map for different frequencies
    color_map = {250: "blue", 1000: "green", 5000: "red"}

    # Calculate and plot RT60 for each frequency
    for frequency in frequencies:
        calculate_rt60(file_path, frequency, color_map.get(frequency))

def plot_all_rt60s():
    # Specify a list of frequencies
    frequencies = [250, 1000, 5000]
    colors = {250: "blue", 1000: "green", 5000: "red"}

    combine_rt60s(frequencies, colors)

def plot_frequency_spectrum(file_path):
    # Load audio file
    wave_file = wave.open(file_path, "rb")
    framerate = wave_file.getframerate()
    frames = wave_file.readframes(-1)
    signal = np.frombuffer(frames, dtype=np.int16)

   # Create a Matplotlib figure
    fig, ax = plt.subplots(figsize=(8, 6))

    # Calculate the Short-Time Fourier Transform (STFT)
    result = plt.specgram(signal, NFFT=1024, Fs=framerate, noverlap=512, cmap="viridis")
    Sxx = result[2]

    # Displays for the chart
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.title("Clap Audio")

    plt.show()

def plot_wave(file_path):
    # Load audio file
    wave_file = wave.open(file_path, "rb")
    framerate = wave_file.getframerate()
    frames = wave_file.readframes(-1)
    signal = np.frombuffer(frames, dtype=np.int16)

    # Create a Matplotlib figure
    fig, ax = plt.subplots(figsize=(8, 6))

    # plot wave
    time = np.linspace(0, len(signal) / framerate, num=len(signal))
    plt.plot(time, signal, color="red")

    # Displays for the chart
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("Clap Audio")

    plt.show()

def load_extra_data():
    plot_frequency_spectrum(wave_file)

def extra_data_button():
    # Create a button to load extra data
    extra_data_button = tk.Button(root, text="Extra Data", command=load_extra_data)
    extra_data_button.pack(pady=20, padx=30)

def file_gui():
    # Setting up main window with tkinter
    global root
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

def show_rt60(wave_file):
    # Showing rt60 value reduce to 0.5 seconds
    rt60_text = tk.Text(root)
    rt60_text.insert(tk.END, f"Difference: {round(abs(rt60_difference(wave_file)), 2)}")
    rt60_text.pack()

def show_audio_length(wave_file):
    # Showing audio file length
    audio_length_text = tk.Text(root)
    audio_length_text.insert(tk.END, f"Audio file length: {round(get_audio_length(wave_file), 2)} s")
    audio_length_text.pack()
