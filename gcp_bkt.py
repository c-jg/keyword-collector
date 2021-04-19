import os 
from google.cloud import storage 


def upload_clip(keyword, wav):
    ''' Uploads collected keyword utterance to GCP bucket.
        Deletes original.
    
    keyword:    Gathered keyword (name of directory)
    wav:        Path to wav file to be uploaded 
    '''
    
    bucket_name = "clip_bkt"
    wav_name = wav.split("/")[-1]
    destination = f"{keyword}/{wav_name}"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination)

    blob.upload_from_filename(wav)

    os.remove(wav)


def upload_long(keyword, wav, resampled):
    ''' Uploads full audio. Deletes original.
    
    keyword:    Gathered keyword
    wav:        Path to wav file to be uploaded 
    resampled:  Whether or not the file has been resampled.
    '''
    
    bucket_name = "long-bkt"
    wav_name = wav.split("/")[-1]

    if resampled is True:
        destination = f"resampled/{keyword}/{wav_name}"
    else:
        destination = f"original/{keyword}/{wav_name}"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination)

    blob.upload_from_filename("data/" + wav)

    os.remove("data/" + wav)


def count_files(keyword):
    ''' Returns number of wav files in directory 
    
    keyword: Keyword to count 
    '''

    bucket_name = "clip_bkt"
    storage_client = storage.Client()
    
    files = storage_client.list_blobs(bucket_name, prefix=keyword)

    num_files = 0
    for f in files:
        num_files += 1
    
    return num_files
