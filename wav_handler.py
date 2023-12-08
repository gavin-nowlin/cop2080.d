import os
from pydub import AudioSegment
from tkinter import filedialog
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
import wave
import matplotlib.pyplot as plt

# Converting .mp3 file to .wav
def mp3_to_wav(mp3_audio):
    dst, ext = os.path.splitext(mp3_audio)
    wav_audio = dst + '.wav'
    
    sound = AudioSegment.from_mp3(mp3_audio)
    sound.export(wav_audio, format='wav')
    return sound

# Returns all .wav and .mp3 files as .wav files
def get_audio_files():
    # List of audio files
    audio_files = []
    # Getting audio files in audio directory
    for file in os.listdir():
        if file.endswith('.wav'):
            audio_files.append(file)
        elif file.endswith('.mp3'):
            mp3_to_wav(file)
            audio_files.append(file)
    return audio_files

def main():
    get_audio_files()

if __name__ == "__main__":
    main()

#katelyns changes //////////////////////////////////////


def load_audio_file():
    #filedialogue allows user to pick file w button
    #askopenfilename is just the request

    file_path = filedialog.askopenfilename(title="Select Audio File", filetypes=[("Audio Files", "*.wav")])
    #checks if user selects a file
    if file_path:
        plot_wave(file_path)
        plot_frequency_spectrum(file_path)

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


# Setting up main window with tkinter
root = tk.Tk()
root.title("Waveform")

# Create a button to load an audio file
load_button = tk.Button(root, text="Load Audio File", command=load_audio_file)
load_button.pack(pady=20, padx=30)

# Create a label to display the spectrogram image
label = tk.Label(root)
label.pack()

# call 
root.mainloop()
