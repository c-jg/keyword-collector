from extract_words import extract
from resample import resample_audio, resample_local

from youtube.video_dl import download_audio
from youtube.video_search import SearchQuery
import find_ids
import gcp_db
import gcp_bkt

import argparse
import os 
import shutil
import sys 
from glob import glob 
from tqdm import tqdm


def get_keywords_loop_yt(keyword, query):
    '''
    Downloads audio from YouTube and searches through audio until enough 
    utterances are collected.

    keyword (str): Desired keyword
    query (str):   YouTube search query 
    '''

    # check for existing search results
    search_results = find_ids.check_records(keyword=keyword)

    if len(search_results) == 0:
        if query is None:
            query = keyword 

        search_query = SearchQuery(keyword=keyword, query=query)
        search_results = search_query.search() # list of video id's

    total_ext = 0
    total_saved = 0

    # list of videos in DB
    extracted = gcp_db.list_records(table=keyword, column="VIDEO_ID")

    kw_dir = os.path.join("data", keyword)
    if not os.path.exists(kw_dir):
        os.makedirs(kw_dir)

    # download and extract each video in search results 
    for video_id in tqdm(search_results):
        # skip if video has already been analyzed 
        if video_id in extracted:
            continue 

        # count number of utterances collected in GCP bucket 
        total_files = gcp_bkt.count_files(keyword)
        print(f"Total utterances: {total_files}")

        if total_files < 75:
            try:
                og_wav = download_audio(video_id=video_id)
                resampled = resample_audio(og_wav)

                gcp_bkt.upload_long(keyword=keyword, wav=og_wav, 
                                    resampled=False)

                # extract keywords
                num_saved = extract(conv_audio=resampled, keyword=keyword, 
                                    auth=True)
                
                gcp_bkt.upload_long(keyword=keyword, wav=resampled, 
                                    resampled=True)
                gcp_db.store_record(table=keyword, video_id=video_id, 
                                    count=num_saved)
                
                total_ext += 1
                total_saved += num_saved
            except Exception as e:
                print(e)
        
    print(f"Done with data gathering.")
    print(f"Total videos analyzed: {total_ext}")
    print(f"Total utterances added: {total_saved}")
    print(f"Total utterances of '{keyword}': {total_files}")


def get_keywords_loop_local(keyword, data_dir):
    '''
    Searches through local wav files for utterancs. Does not upload to cloud.
    Compresses files and returns path to zip file containing utterances.
    
    keyword (str):     Desired keyword to collect 
    data_dir (str):    Path to directory containing local wav files
    '''
    kw_dir = os.path.join("data", keyword)
    if not os.path.exists(kw_dir):
        os.makedirs(kw_dir)

    wav_files = glob(os.path.join(data_dir, "*.wav"))

    for wav in tqdm(wav_files):
        resampled = resample_audio(wav)
        
        # extract keyword utterances 
        num_saved = extract(conv_audio=resampled, keyword=keyword, auth=False)

        os.remove(resampled)

    return shutil.make_archive(keyword, 'zip', kw_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--keyword',
        type=str,
        help='Keyword to collect'
    )

    parser.add_argument(
        '--query',
        type=str,
        help='Query to search on YouTube'
    )

    parser.add_argument(
        '--data_dir',
        type=str,
        help="Directory containing wav files"
    )
    
    FLAGS, _ = parser.parse_known_args()

    if FLAGS.keyword is not None:
        if FLAGS.data_dir is None:
            get_keywords_loop_yt(keyword=FLAGS.keyword, query=FLAGS.query)
        else:
            archive = get_keywords_loop_local(keyword=FLAGS.keyword, 
                                        data_dir=FLAGS.data_dir)
            print(f"Collected utterances saved to: {archive}")
    else:
        print("No keyword entered.")
