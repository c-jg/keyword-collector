from deepspeech import Model

import soundfile as sf
import numpy as np
import gcp_bkt

import os 
import wave


def read_wav_file(filename):
    ''' Must be already resampled (16kHz, mono) '''
    with wave.open(filename, 'rb') as w:
        rate = w.getframerate()
        frames = w.getnframes()
        buffer = w.readframes(frames)

    audio = np.frombuffer(buffer, dtype=np.int16)

    return audio, buffer, rate
    

def get_model():
    model_file_path = "models/deepspeech-0.9.3-models.pbmm"
    lm_file_path = "models/deepspeech-0.9.3-models.scorer"

    beam_width = 100
    lm_alpha = 0.93
    lm_beta = 1.18

    model = Model(model_file_path)
    model.enableExternalScorer(lm_file_path)

    model.setScorerAlphaBeta(lm_alpha, lm_beta)
    model.setBeamWidth(beam_width)
    
    return model 


def transcribe_batch(audio):
    ''' Get letters and timestamps '''
    model = get_model()
    return model.sttWithMetadata(audio).transcripts[0].tokens


def extract_keywords(metadata):
    ''' Combine letters and timestamps to form words '''
    word = ''
    transcript = []
    start = metadata[0].start_time
    
    for i, token in enumerate(metadata):
        letter = token.text

        if letter == ' ' or i == len(metadata):
            last_letter = metadata[i-1].start_time
            transcript.append((word, start, last_letter))
            start = token.start_time 
            word = ''
        else:
            word += letter
    
    return transcript


def save_keywords(transcript, keyword, audio, auth):
    ''' Save utterances in individual .wav files '''

    kw_dir = os.path.join("data", keyword)
    
    sample_rate = 16000

    key = len(os.listdir(kw_dir))

    saved = 0
    for i, entry in enumerate(transcript):
        word = entry[0] # keyword
        
        # save only desired keyword 
        if word == keyword:    
            # get start and end times 
            start = int(entry[1] * sample_rate)
            end = int(entry[2] * sample_rate)

            # save wav file 
            save_file = f"{word}_{i+key}.wav"
            out_file_path = os.path.join(kw_dir, save_file)
            sf.write(out_file_path, audio[start:end], sample_rate)

            if auth is True:
                # upload to google storage bucket
                gcp_bkt.upload_clip(keyword=keyword, wav=out_file_path)
            
            saved += 1

    return saved


def inspect_keywords(transcript):
    ''' Returns unique words and their frequencies. '''

    words = []

    for i, entry in enumerate(transcript):
        word = entry[0] # keyword
        words.append(word)

    u_words, counts = np.unique(words, return_counts=True)

    word_counts = list(zip(u_words, counts))

    sorted_counts = sorted(word_counts, key=lambda x: x[1])
    
    return sorted_counts


def extract(conv_audio, keyword, auth):
    '''
    Extracts keywords from audio file,

    conv_audio: Path to resampled audio file 
    keyword:    Desired keyword to collect
    auth:       True if saving to GCP cloud storage bucket 
    '''
    print(f"Extracting '{keyword}' utterances from {conv_audio}.")
    # time series, number of samples, sampling rate 
    audio, buffer, rate = read_wav_file(conv_audio)

    # tokens 
    transcribed_metadata = transcribe_batch(audio=audio)

    # list of words with start, end times 
    transcript = extract_keywords(transcribed_metadata)

    num_saved = save_keywords(transcript=transcript, keyword=keyword, 
                            audio=audio, auth=auth)

    print(f"Utterances saved: {num_saved}")

    return num_saved 
    