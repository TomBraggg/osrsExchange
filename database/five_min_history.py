import sqlite3
from api_calls.api_calls import *
from database.request import update_request_table

REQUEST_TYPE = "FiveMinHistory"


def create_five_min_history_table():
    conn = sqlite3.connect('osrs_exchange.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS five_min_history
                      (request_id INTEGER,
                       item_id INTEGER, 
                       five_min_low_price_avg INTEGER, 
                       five_min_high_price_avg INTEGER, 
                       five_min_low_price_vol INTEGER, 
                       five_min_high_price_vol INTEGER)''')

    conn.close()


def update_five_min_history_table():
    conn = sqlite3.connect('osrs_exchange.db')
    cursor = conn.cursor()

    request_id = update_request_table(REQUEST_TYPE)
    data = get_item_five_min_history().json()["data"]

    for item_id, item_data in data.items():

        insert_data = {'item_id': item_id, 'five_min_low_price_avg': item_data.get("avgLowPrice"), 'five_min_high_price_avg': item_data.get("avgHighPrice"),
                       'five_min_low_price_vol': item_data.get("lowPriceVolume"), 'five_min_high_price_vol': item_data.get("highPriceVolume")}

        cursor.execute('''INSERT OR REPLACE INTO five_min_history
                        (request_id, item_id, five_min_low_price_avg, five_min_high_price_avg, five_min_low_price_vol, five_min_high_price_vol)
                        VALUES (?, ?, ?, ?, ?, ?)''',
                       (request_id, insert_data['item_id'], insert_data['five_min_low_price_avg'],
                        insert_data['five_min_high_price_avg'], insert_data['five_min_low_price_vol'], insert_data['five_min_high_price_vol']))

    conn.commit()
    conn.close()
