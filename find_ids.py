import psycopg2
import os 
import gcp_db


def check_records(keyword):
    '''
    Checks for saved video ids before searching YouTube

    keyword (str): Desired keyword being collected 
    '''
    # check for existing search records 
    search_results_records = os.path.join(os.getcwd(), f"records/{keyword}_searched.txt")
    
    if os.path.exists(search_results_records):
        # read local txt records 
        search_results_records = os.path.join(os.getcwd(), f"records/{keyword}_searched.txt")
        results_txt = open(search_results_records, 'r')
        found_ids = [i.strip() for i in results_txt.readlines()]
        results_txt.close()
        return get_txt_ids(table=keyword, found_ids=found_ids)
    return []


def get_txt_ids(table, found_ids):
    '''
    Checks database to see searched ID's that haven't been analyzed yet.
    Returns list of video ids to download.

    table (str):        Name of table (Desired keyword being collected)
    found_ids (list):   List of video ID's in txt file
    '''
    
    # connect to DB and get list of records 
    db_video_ids = gcp_db.list_records(table=table, column="VIDEO_ID")

    new_ids = []

    # check if id in txt is already in DB
    for video in found_ids:
        if video not in db_video_ids:
            new_ids.append(video)
    
    return new_ids
