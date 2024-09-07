import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries, count_staging_events, count_staging_songs, count_songplays, count_users, count_songs, \
    count_artists, count_time


def print_table_counts(cur):
    """Print row counts for each table after ETL"""

    # List of tables and their count queries
    count_queries = {
        "staging_events": count_staging_events,
        "staging_songs": count_staging_songs,
        "songplays": count_songplays,
        "users": count_users,
        "songs": count_songs,
        "artists": count_artists,
        "time": count_time
    }

    for table, query in count_queries.items():
        cur.execute(query)
        result = cur.fetchone()
        print(f"SELECT COUNT(*) FROM {table}: {result[0]} rows")

def load_staging_tables(cur, conn):
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    print(conn)
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)
    print('loan and insert have been succesfully done')
    print_table_counts(cur)

    conn.close()


if __name__ == "__main__":
    main()