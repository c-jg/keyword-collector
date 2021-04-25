import os
import librosa
import soundfile as sf


def resample_audio(audio_file):
    ''' 
    Downsamples and converts audio from stereo to mono.
    Saves audio to file on machine.

    audio_file: Name of .wav file 

    Returns path to converted file. Saves converted file to 'data' directory.
    '''
    y, sr = librosa.load(audio_file, sr=16000, mono=True)

    audio_file_name = audio_file.split("/")[-1][:-4]
    out_file_name = audio_file_name + "_16kHz.wav"
    out_file_path = os.path.join("data", out_file_name)

    sf.write(out_file_path, y, sr)

    return out_file_path


def resample_local(audio_file):
    ''' 
    Downsamples and converts audio from stereo to mono. Does not save file.

    audio_file: Path to .wav file 

    Returns signal array and name of file.
    '''
    y, sr = librosa.load(audio_file, sr=16000, mono=True)

    return y, audio_file
