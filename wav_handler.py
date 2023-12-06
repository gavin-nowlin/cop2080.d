import os
from pydub import AudioSegment

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
