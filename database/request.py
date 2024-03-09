import sqlite3
import time
from api_calls.api_calls import *


def create_request_table():
    conn = sqlite3.connect('osrs_exchange.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS request
                      (request_id INTEGER PRIMARY KEY,
                       request_type TEXT, 
                       request_time TEXT)''')

    conn.close()


def update_request_table(request_type):
    conn = sqlite3.connect('osrs_exchange.db')
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO request
                    (request_type, request_time)
                    VALUES (?, ?)''',
                   (request_type, round(time.time())))

    request_id = cursor.execute('''SELECT request_id FROM request ORDER BY request_id DESC LIMIT 1''').fetchone()[0]

    conn.commit()
    conn.close()

    return request_id
