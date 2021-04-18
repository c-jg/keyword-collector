import librosa
import soundfile as sf


def resample_audio(audio_file, keyword):
    ''' 
    Downsamples and converts audio from stereo to mono. 

    audio_file: name of .wav file 

    Returns path to converted file. Saves converted file to 'data' directory.
    '''

    file_name = audio_file.split(".wav")[0]
    file_path = "data/" + audio_file

    sample_rate = 16000
    y, sr = librosa.load(file_path, sr=sample_rate, mono=True)

    out_file_name = file_name + "_16kHz.wav"
    out_file_path = f"data/{file_name}_16kHz.wav"

    # save audio file
    sf.write(out_file_path, y, sr)
    print("Converted file saved to: " + out_file_path)

    return out_file_name
