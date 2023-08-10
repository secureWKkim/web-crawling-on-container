import psycopg2
import time
import logging


def return_postgresql_conn():
    # Connect to PostgreSQL Docker container
    db_config = {
        'user': 'postgres',
        'password': '1234',
        # 'host': 'localhost',  # for local environment test
        'host': 'database',
        'port': 5432,
        'database': 'postgres'
    }

    # Easy ver. of Blocking Call
    MAX_RETRIES, RETRY_DELAY = 5, 5
    for retry_count in range(MAX_RETRIES):
        try:
            conn = psycopg2.connect(**db_config)
            logging.info("Connected to PostgreSQL.")
            return conn
        except psycopg2.OperationalError:
            logging.info(f"Attempt {retry_count + 1}/{MAX_RETRIES}: Connection failed. Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)
    logging.info(f"Could not establish the database connection after {MAX_RETRIES} attempts.")
    return None