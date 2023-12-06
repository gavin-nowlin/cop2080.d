from wav_handler import *

# Strips extra channels and meta data
def channel_stripper():
    audio_files = get_audio_files()
    for file in audio_files:
        raw_audio = AudioSegment.from_file(file, format="wav")
        mono_wav = raw_audio.set_channels(1)
        mono_wav.export(file, format="wav")
        mono_wav_audio = AudioSegment.from_file(file, format="wav")

def main():
    channel_stripper()

if __name__ == "__main__":
    main()
