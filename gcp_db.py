import psycopg2
import os 

def store_record(keyword, video_id, count):
    ''' Stores number of keyword utterances collected per video id 
    
    keyword (str):        Keyword being extracted from video
    video_id (str):       Video id of YouTube video
    count (int):          Number of utterances collected from video
    '''

    params = {
        'sslmode': 'verify-ca',
        'sslrootcert': 'gcp_creds/server-ca.pem', 
        'sslcert': 'gcp_creds/client-cert.pem', 
        'sslkey': 'gcp_creds/client-key.pem', 
        'hostaddr': '34.67.189.94',
        'port': 5432,
        'user': 'postgres',
        'password': os.environ["DB_KEY"],
        'dbname': 'collected_kw'
    }

    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    table = keyword 

    # get list of tables 
    list_tables_query = "SELECT table_schema, table_name FROM information_schema.tables WHERE (table_schema = 'public');"
    cur.execute(list_tables_query)
    tables = cur.fetchall()

    # create table if it doesn't exist 
    if table not in [t[1] for t in tables]:
        query = f'CREATE TABLE {table} (VIDEO_ID VARCHAR PRIMARY KEY, num_kw INT DEFAULT 0);'
        cur.execute(query)
        conn.commit()
        print(f"Created table: {table}")

    # add record into DB
    query = f"INSERT INTO {table} (VIDEO_ID, num_kw) VALUES ('{video_id}', {count});"
    cur.execute(query)
    conn.commit()

    # retrieve all records from DB
    # cur.execute(f"SELECT * FROM {table};")
    # out = cur.fetchall()
    # print(out)

    conn.close()
