# This file keeps the state information of the system

# from view import *
import os
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
from scipy.io import wavfile


# Debug printing function
def debugg(fstring):
    print(fstring)
    # pass

# Converting .mp3 file to .wav
def mp3_to_wav(mp3_audio):
    dst, ext = os.path.splitext(mp3_audio)
    wav_audio = dst + ".wav"
    
    sound = AudioSegment.from_mp3(mp3_audio)
    sound.export(wav_audio, format="wav")
    debugg(f"sound: {wav_audio}")
    return wav_audio

# Returns all .wav and .mp3 files as .wav files
def get_audio_files():
    # List of audio files
    audio_files = []
    # Getting audio files in audio directory
    for file in os.listdir():
        if file.endswith(".wav"):
            audio_files.append(file)
        elif file.endswith(".mp3"):
            mp3_to_wav(file)
            audio_files.append(file)
    return audio_files

# Strips extra channels and metadata
def audio_stripper(audio_file):
    raw_audio = AudioSegment.from_file(audio_file, format="wav")
    mono_wav = raw_audio.set_channels(1)
    mono_wav.export(audio_file, format="wav")
    debugg(f"mono_wav path: {audio_file}")
    return audio_file

# Find a nearest value
def find_nearest_value(array, value):
    array = np.asarray(array)
    debugg(f"array {array[:10]}")
    idx = (np.abs(array - value)).argmin()
    debugg(f"idx {idx}")
    debugg(f"array[idx] {round(array[idx], 2)}")
    return array[idx]

def find_target_frequency(freqs, ideal_freq):
    for x in freqs:
        if x > ideal_freq:
            break
    return x

def frequency_check(frequency):
    debugg(f"freqs {freqs[:10]}")
    target_frequency = find_target_frequency(freqs, frequency)
    debugg(f"target_frequency {round(target_frequency, 2)}")
    index_of_frequency = np.where(freqs == target_frequency) [0][0]
    debugg(f"index_of_frequency {index_of_frequency}")
    
    # Find a sound data for a particular frequency
    data_for_frequency = spectrum[index_of_frequency]
    debugg(f"data_for_frequency {data_for_frequency[:10]}")
    
    # Change a digital signal for a values in decibles
    data_in_db_fun = 10 * np.log10(data_for_frequency)
    return data_in_db_fun

def calculate_rt60(audio_file, frequency, color):
    # Getting sample rates and data from audio file
    sample_rate, data = wavfile.read(audio_file)

    global freqs, spectrum, t

    # Create a single subplot with two sets of axes
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12), sharex=True)

    # Plot the spectrogram
    spectrum, freqs, t, im = ax1.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap("autumn_r"))
    ax1.set_title("Spectrogram")
    ax1.set_ylabel("Frequency (Hz)")

    # Plot reverb time on the second subplot
    data_in_db = frequency_check(frequency)
    ax2.plot(t, data_in_db, linewidth=1, alpha=0.7, color=color)
    ax2.set_title(f"Reverb Time Plot - Frequency: {frequency} Hz")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Power (dB)")

    # Find an index of a max value
    index_of_max = np.argmax(data_in_db)
    value_of_max = data_in_db[index_of_max]

    # Slice array from a max value
    sliced_array = data_in_db[index_of_max:]

    value_of_max_less_5 = value_of_max - 5
    value_of_max_less_25 = value_of_max - 25

    # Getting index of the closest value in the data to the max value minus 5
    value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)
    index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)

    # Getting index of the closest value in the data to the max value minus 25
    value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)
    index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)

    # Plot max, mid, and min points on the reverb time plot
    ax2.plot(t[index_of_max], value_of_max, "go", label="Max")
    ax2.plot(t[index_of_max_less_5], value_of_max_less_5, "yo", label="Max - 5dB")
    ax2.plot(t[index_of_max_less_25], value_of_max_less_25, "ro", label="Max - 25dB")
    ax2.legend()

    # Extraploating rt20 to get rt60
    rt20 = (t[index_of_max_less_5] - t[index_of_max_less_25])[0]
    rt60 = 3 * rt20

    debugg(f"The RT60 reverb time for {frequency} Hz is {round(abs(rt60), 2)} seconds")

    plt.show()

def combine_rt60s(audio_file, frequencies = [], colors = {}):
    for frequency in frequencies:
        target_frequency = find_target_frequency(freqs, frequency)
        index_of_frequency = np.where(freqs == target_frequency) [0][0]
        data_for_frequency = spectrum[index_of_frequency]
        data_in_db = 10 * np.log10(data_for_frequency)

        plt.plot(t, data_in_db, linewidth=1, alpha=0.7, color=colors[frequency])
        plt.set_title(f"Reverb Time Plot - Frequency: {frequencies} Hz")
        plt.set_xlabel("Time (s)")
        plt.set_ylabel("Power (dB)")

    plt.show()

def calculate_rt60_time(wave_file, frequency):
    # # Plot reverb time on the second subplot
    # data_in_db = frequency_check(frequency)

    # # Find an index of a max value
    # index_of_max = np.argmax(data_in_db)
    # value_of_max = data_in_db[index_of_max]

    # # Slice array from a max value
    # sliced_array = data_in_db[index_of_max:]

    # value_of_max_less_5 = value_of_max - 5
    # value_of_max_less_25 = value_of_max - 25

    # # Getting index of the closest value in the data to the max value minus 5
    # value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)
    # index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)

    # # Getting index of the closest value in the data to the max value minus 25
    # value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)
    # index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)

    # rt20 = (t[index_of_max_less_5] - t[index_of_max_less_25])[0]
    # return 3 * rt20

    # Plot reverb time on the second subplot
    data_in_db = frequency_check(frequency)

    # Find an index of a max value
    index_of_max = np.argmax(data_in_db)
    value_of_max = data_in_db[index_of_max]

    # Slice array from a max value
    sliced_array = data_in_db[index_of_max:]

    value_of_max_less_5 = value_of_max - 5
    value_of_max_less_25 = value_of_max - 25

    # Getting index of the closest value in the data to the max value minus 5
    value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)
    index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)

    # Getting index of the closest value in the data to the max value minus 25
    value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)
    index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)

    rt20 = (t[index_of_max_less_5] - t[index_of_max_less_25])[0]
    return 3 * rt20

def rt60_difference(wave_file):
    rt60_difference_reduced = int(0)
    frequencies = [250, 1000, 5000]
    for frequency in frequencies:
        rt60_difference_reduced += calculate_rt60_time(wave_file, frequency)

    return (rt60_difference_reduced // 3) - 0.5
