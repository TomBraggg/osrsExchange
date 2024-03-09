import sqlite3
from api_calls.api_calls import *
from database.request import update_request_table

REQUEST_TYPE = "Latest"


def create_latest_table():
    conn = sqlite3.connect('osrs_exchange.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS latest
                      (request_id INTEGER,
                       item_id INTEGER, 
                       low_price INTEGER, 
                       high_price INTEGER, 
                       low_time INTEGER, 
                       high_time INTEGER)''')

    conn.close()


def update_latest_table():
    conn = sqlite3.connect('osrs_exchange.db')
    cursor = conn.cursor()

    request_id = update_request_table(REQUEST_TYPE)
    data = get_latest_prices().json()["data"]

    for item_id, item_data in data.items():

        insert_data = {'item_id': item_id, 'high': item_data.get("high"), 'low': item_data.get("low"),
                       'high_time': item_data.get("highTime"), 'low_time': item_data.get("lowTime")}

        cursor.execute('''INSERT OR REPLACE INTO latest
                        (request_id, item_id, high_price, low_price, high_time, low_time)
                        VALUES (?, ?, ?, ?, ?, ?)''',
                       (request_id, insert_data['item_id'], insert_data['high'],
                        insert_data['low'], insert_data['high_time'], insert_data['low_time']))

    conn.commit()
    conn.close()
