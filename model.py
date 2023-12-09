# This file keeps the state information of the system

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
    wav_audio = dst + '.wav'
    
    sound = AudioSegment.from_mp3(mp3_audio)
    sound.export(wav_audio, format='wav')
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

def frequency_check():
    debugg(f"freqs {freqs[:10]}")
    target_frequency = find_target_frequency(freqs, 1000)
    debugg(f"target_frequency {round(target_frequency, 2)}")
    index_of_frequency = np.where(freqs == target_frequency) [0][0]
    debugg(f"index_of_frequency {index_of_frequency}")
    
    # Find a sound data for a particular frequency
    data_for_frequency = spectrum[index_of_frequency]
    debugg(f"data_for_frequency {data_for_frequency[:10]}")
    
    # Change a digital signal for a values in decibles
    data_in_db_fun = 10 * np.log10(data_for_frequency)
    return data_in_db_fun

# --------------------
def calulate_rt60(audio_file):
    # Getting sample rates and data from audio file
    sample_rate, data = wavfile.read(audio_file)

    global freqs, spectrum

    spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, \
    NFFT=1024, cmap=plt.get_cmap("autumn_r"))
    
    data_in_db = frequency_check()
    plt.figure()

    # Plot reverb time on grid
    plt.plot(t, data_in_db, linewidth=1, alpha=0.7, color="#004bc6")
    plt.xlabel("Time (s)")
    plt.ylabel("Power (dB)")

    # Find an index of a max value
    index_of_max = np.argmax(data_in_db)

    value_of_max = data_in_db[index_of_max]

    plt.plot(t[index_of_max], data_in_db[index_of_max], "go")

    # Slice array from a max value
    sliced_array = data_in_db[index_of_max:]

    value_of_max_less_5 = value_of_max - 5

    # Getting index of the closest value in the data to the max value minus 5
    value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)

    index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)

    plt.plot(t[index_of_max_less_5], data_in_db[index_of_max_less_5], "yo")

    # Slice array from a max -5dB
    value_of_max_less_25 = value_of_max - 25

    value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)

    index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)

    plt.plot(t[index_of_max_less_25], data_in_db[index_of_max_less_25], "ro")
    rt20 = (t[index_of_max_less_5] - t[index_of_max_less_25])[0]

    plt.show()

    # Extraploating rt20 to get rt60
    rt60 = 3 * rt20

    debugg(f"The RT60 reverb time is {round(abs(rt60), 2)} seconds")
# --------------------


