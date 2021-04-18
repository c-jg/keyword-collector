from extract_words import extract
from resample import resample_audio

from youtube.video_dl import download_audio
from youtube.video_search import SearchQuery
import gcp_db
import gcp_bkt

import argparse
import os 
import sys 
from tqdm import tqdm


def get_keywords_loop(keyword):
    search_query = SearchQuery(query=keyword)
    search_results = search_query.search() # list of video id's

    total_ext = 0
    total_saved = 0

    # download and extract each video in search results 
    for video_id in tqdm(search_results):
        # count number of utterances collected in GCP bucket 
        total_files = gcp_bkt.count_files(keyword)
        print(f"Total utterances: {total_files}")

        if total_files < 75:
            try:
                # download full video audio
                og_wav = download_audio(video_id=video_id)
                print("Downloaded audio.")

                # upload original audio to GCP bkt 
                gcp_bkt.upload_long(keyword=keyword, wav=og_wav, resampled=False)
                print("Uploaded original audio.")

                # resample 
                resampled = resample_audio(og_wav, keyword)
                print("Resampled.")

                # extract keywords
                num_saved = extract(conv_audio=resampled, keyword=keyword)
                
                # upload resampled audio file to GCP and delete
                gcp_bkt.upload_long(keyword=keyword, wav=resampled, resampled=True)

                # add video IDs to GCP PSQL DB
                gcp_db.store_record(keyword=keyword, video_id=video_id, count=num_saved)
                
                total_ext += 1
                total_saved += num_saved
            except Exception as e:
                print(e)
        
    print(f"Done with data gathering.")
    print(f"Total videos analyzed: {total_ext}")
    print(f"Total utterances added: {total_saved}")
    print(f"Total utterances of '{keyword}': {total_files}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--keyword',
        type=str,
        help='Keyword to collect'
    )
    
    FLAGS, _ = parser.parse_known_args()
    
    if len(sys.argv) > 1:
        get_keywords_loop(keyword=FLAGS.keyword)
    else:
        print("No keyword entered.")
