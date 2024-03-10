import sqlite3

conn = sqlite3.connect('osrs_exchange.db')
cursor = conn.cursor()


def get_item_margins():

    latest_data = cursor.execute('''SELECT a.name, b.* FROM
                                    item_mapping a, (SELECT * FROM latest WHERE request_id IN (SELECT MAX(request_id) FROM latest)) b
                                    WHERE a.item_id = b.item_id''').fetchall()

    for item in latest_data:
        item_data = {'item_name': item[0], 'item_id': item[2], 'low_price': item[3],
                     'high_price': item[4], 'low_time': item[5], 'high_time': item[6]}

        item_margin = {'item_name': item[0], 'item_margin': item[4] - item[3]}

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(item_data)
        print(item_margin)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
