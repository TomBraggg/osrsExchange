import sqlite3
from api_calls.ApiCalls import *
from database.Request import update_request_table

REQUEST_TYPE = "Mapping"

def create_mapping_table():
    conn = sqlite3.connect('osrs_exchange.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS item_mapping
                      (item_id INTEGER PRIMARY KEY,
                       request_id INTEGER,
                       examine TEXT, 
                       members TEXT, 
                       lowalch INTEGER, 
                       trade_limit INTEGER, 
                       value INTEGER, 
                       highalch INTEGER, 
                       icon TEXT, 
                       name TEXT)''')

    conn.close()


def update_mapping_table():
    conn = sqlite3.connect('osrs_exchange.db')
    cursor = conn.cursor()

    request_id = update_request_table(REQUEST_TYPE)
    data = get_item_mappings().json()

    for item in data:
        if 'limit' not in item:
            item['limit'] = 0
        if 'lowalch' not in item:
            item['lowalch'] = 0
        if 'highalch' not in item:
            item['highalch'] = 0

        cursor.execute('''INSERT OR REPLACE INTO item_mapping
                        (item_id, request_id, examine, members, lowalch, trade_limit, value, highalch, icon, name)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (item['id'], request_id, item['examine'], item['members'], item['lowalch'], item['limit'],
                        item['value'], item['highalch'], item['icon'], item['name']))

    conn.commit()
    conn.close()
