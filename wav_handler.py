import os
from pydub import AudioSegment

# Converting .mp3 file to .wav
def mp3_to_wav(mp3_audio):
    dst, ext = os.path.splitext(mp3_audio)
    wav_audio = dst + '.wav'
    
    sound = AudioSegment.from_mp3(mp3_audio)
    sound.export(wav_audio, format='wav')
    return sound

# List of audio files
audio_files = []

# Getting audio files in audio directory
for file in os.listdir():
    if file.endswith('.mp3'):
        mp3_to_wav(file)
        audio_files.append(file)
    elif file.endswith('.wav'):
        audio_files.append(file)
