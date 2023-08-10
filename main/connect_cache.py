import sqlite3


def return_sqlite_conn():
    try:
        sqlite_conn = sqlite3.connect("./data/sqlite3/events.db")
    except:
        sqlite_conn = sqlite3.connect("/Users/wonkyungkim/Documents/pythondev/crawl/data/sqlite3/events.db")

    sqlite_conn.cursor().execute('''
            CREATE TABLE IF NOT EXISTS events (
                title VARCHAR(255) NOT NULL PRIMARY KEY,
                event_time TIMESTAMP NOT NULL)
        ''')

    return sqlite_conn