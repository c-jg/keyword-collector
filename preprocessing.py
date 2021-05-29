import os
import librosa
import soundfile as sf


def process_audio(filename):
    ''' 
    Downsamples to 16kHz and converts audio from stereo to mono.
    Saves audio to file and returns its path.

    Arguments
        filename: Path to WAV file 
    '''
    y, sr = librosa.load(filename, sr=16000, mono=True)

    audio_file_name = os.path.basename(filename)[:-4]
    out_file_name = audio_file_name + "_16kHz.wav"

    sf.write(out_file_name, y, sr)

    return out_file_name


def process_inplace(audio_file):
    ''' 
    Downsamples and converts audio from stereo to mono. Does not save file.

    audio_file: Path to .wav file 

    Returns signal array and name of file.
    '''
    y, sr = librosa.load(audio_file, sr=16000, mono=True)

    return y, audio_file
