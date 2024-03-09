import sqlite3
from api_calls.api_calls import *
from database.request import update_request_table

REQUEST_TYPE = "OneHourHistory"


def create_one_hour_history_table():
    conn = sqlite3.connect('osrs_exchange.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS one_hour_history
                      (request_id INTEGER,
                       item_id INTEGER, 
                       one_h_low_price_avg INTEGER, 
                       one_h_high_price_avg INTEGER, 
                       one_h_low_price_vol INTEGER, 
                       one_h_high_price_vol INTEGER)''')

    conn.close()


def update_one_hour_history_table():
    conn = sqlite3.connect('osrs_exchange.db')
    cursor = conn.cursor()

    request_id = update_request_table(REQUEST_TYPE)
    data = get_item_one_h_history().json()["data"]

    for item_id, item_data in data.items():

        insert_data = {'item_id': item_id, 'one_h_low_price_avg': item_data.get("avgLowPrice"), 'one_h_high_price_avg': item_data.get("avgHighPrice"),
                       'one_h_low_price_vol': item_data.get("lowPriceVolume"), 'one_h_high_price_vol': item_data.get("highPriceVolume")}

        cursor.execute('''INSERT OR REPLACE INTO one_hour_history
                        (request_id, item_id, one_h_low_price_avg, one_h_high_price_avg, one_h_low_price_vol, one_h_high_price_vol)
                        VALUES (?, ?, ?, ?, ?, ?)''',
                       (request_id, insert_data['item_id'], insert_data['one_h_low_price_avg'],
                        insert_data['one_h_high_price_avg'], insert_data['one_h_low_price_vol'], insert_data['one_h_high_price_vol']))

    conn.commit()
    conn.close()
