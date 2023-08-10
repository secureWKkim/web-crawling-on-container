import datetime
import sys
import psycopg2
import logging

from connect_cache import return_sqlite_conn
from connect_db import return_postgresql_conn


def fetch_cached_data():
    sqlite_conn = return_sqlite_conn()
    sqlite_cursor = sqlite_conn.cursor()
    sqlite_cursor.execute("SELECT title, event_time FROM events")
    data_to_insert = list(map(lambda x: (x[0], datetime.datetime.strptime(x[1], "%Y-%m-%d %H:%M:%S")), sqlite_cursor.fetchall()))
    sqlite_conn.close()
    return data_to_insert


def store_crawled_data_psql():
    postgre_conn = return_postgresql_conn()
    postgre_cursor = postgre_conn.cursor()

    try:
        # TODO: Add more DB columns (event_type, deleted_at, ...)
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS events (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            event_time TIMESTAMP NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP);
        '''
        postgre_cursor.execute(create_table_query)

        postgre_cursor.executemany("""
        MERGE INTO events AS target
        USING (
            VALUES (%s, %s)
        ) AS source (title, event_time)
        ON (target.title = source.title)
        WHEN MATCHED THEN
            UPDATE SET event_time = source.event_time,
            updated_at = CASE
                            WHEN target.event_time <> source.event_time THEN CURRENT_TIMESTAMP
                            ELSE updated_at
                        END
        WHEN NOT MATCHED THEN
            INSERT (title, event_time)
            VALUES (source.title, source.event_time);
        """, fetch_cached_data())

        # TODO: find better way to process transactions. ex) 커밋/롤백하는 동작 따로 분리 후 각각 주기 설정
        postgre_conn.commit()
        logging.info("Data successfully stored in the database.")

    except psycopg2.Error as err:
        logging.error(f"Error: {err}")
        postgre_conn.rollback()
        sys.exit(1)

    finally:
        postgre_cursor.close()
        postgre_conn.close()




# def store_crawled_data_maria(conn, data_to_insert):
# import mysql.connector
#     cursor = conn.cursor()
#     try:
#         create_table_query = '''
#         CREATE TABLE IF NOT EXISTS events (
#             `id` int(11) NOT NULL AUTO_INCREMENT,
#             `title` varchar(255) NOT NULL,
#             `event_time` datetime NOT NULL,
#             `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
#             `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE
#             CURRENT_TIMESTAMP,
#             PRIMARY KEY (`id`)
#             ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
#         '''
#         cursor.execute(create_table_query)
#
#         # Insert data into the table
#         insert_query = 'INSERT INTO events (title, STR_TO_DATE(event_time)) VALUES (%s, %s)'
#         cursor.executemany(insert_query, data_to_insert)  # data_to_store: list of tuple
#         conn.commit()
#
#         print("Data successfully stored in the database.")
#
#     except mysql.connector.Error as err:
#         print(f"Error: {err}")
#         conn.rollback()
#         sys.exit(1)
#
#     finally:
#         cursor.close()
#         conn.close()