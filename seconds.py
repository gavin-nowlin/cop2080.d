from scipy.io import wavfile
import scipy.io


def get_audio_length(audio_file):
    samplerate, data = wavfile.read(audio_file)
    print(f"number of channels = {data.shape[len(data.shape) - 1]}")
    print(f"sample rate = {samplerate}Hz")
    length = data.shape[0] / samplerate
    return length
