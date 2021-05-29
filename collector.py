import os
from glob import glob
from tqdm import tqdm

from youtube.video_dl import download_audio
from preprocessing import process_audio
from extract_words import extract


def collect_local(data_dir, keyword):
    '''
    Loop to collect keywords from local WAV files.

    Arguments
        data_dir: Directory containing WAV files
        keyword:  Desired keyword to collect
    '''
    wav_files = glob(os.path.join(data_dir, "*.wav"))
    total_collected = 0

    for wav in tqdm(wav_files):
        processed_audio = process_audio(wav)
        num_collected = extract(processed_audio, keyword)

        os.remove(processed_audio)
        
        print("Utterances collected:", num_collected)
        total_collected += num_collected
    
    return print(f"Total utterances collected from {data_dir}: {total_collected}")


def collect_yt(video_ids, keyword, quantity):
    '''
    Loop to download YouTube videos and extract keywords.

    Arguments
        video_ids: List of YouTube ID's to downloads
        keyword:   Desired keyword to collect
        quantity:  How many utterances to collect
    '''
    total_collected = 0

    for video in tqdm(video_ids):
        downloaded_audio = download_audio(video)
        processed_audio = process_audio(downloaded_audio)
        num_collected = extract(processed_audio, keyword)
        
        os.remove(processed_audio)
        os.remove(downloaded_audio)
        
        total_collected += num_collected
        print("Utterances collected:", num_collected)

        if total_collected >= quantity:
            break

    return print("Total utterances collected:", total_collected)
