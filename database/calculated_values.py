import sqlite3
import math


tax_rate = 0.01


def create_calculated_value_table():
    conn = sqlite3.connect('osrs_exchange.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS calculated_value
                      (request_id INTEGER,
                       item_name TEXT,
                       item_id INTEGER, 
                       pre_tax_margin INTEGER, 
                       tax INTEGER, 
                       post_tax_margin INTEGER,
                       flip_roi INTEGER,
                       highalch_margin INTEGER,
                       highalch_roi INTEGER)''')

    conn.close()


def update_calculated_value_table():
    conn = sqlite3.connect('osrs_exchange.db')
    cursor = conn.cursor()

    for item in _get_latest_item_data():
        item_data = {'item_name': item[0], 'highalch': item[1], 'request_id': item[2], 'item_id': item[3], 'low_price': item[4],
                     'high_price': item[5], 'low_time': item[6], 'high_time': item[7]}

        insert_data = _get_calculated_values(item)

        cursor.execute('''INSERT OR REPLACE INTO calculated_value
                        (request_id, item_name, item_id, pre_tax_margin, tax, post_tax_margin, flip_roi, highalch_margin, highalch_roi)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (insert_data['request_id'], insert_data['item_name'], insert_data['item_id'],
                        insert_data['pre_tax_margin'], insert_data['tax'], insert_data['post_tax_margin'], insert_data['flip_roi'],
                        insert_data['highalch_margin'], insert_data['highalch_roi']))

    conn.commit()
    conn.close()


def _get_latest_item_data():
    conn = sqlite3.connect('osrs_exchange.db')
    cursor = conn.cursor()

    latest_data_list = cursor.execute('''SELECT a.name, a.highalch, b.* FROM
                                    item_mapping a, (SELECT * FROM latest WHERE request_id IN (SELECT MAX(request_id) FROM latest)) b
                                    WHERE a.item_id = b.item_id''').fetchall()

    return latest_data_list


def _get_nature_rune_price():
    conn = sqlite3.connect('osrs_exchange.db')
    cursor = conn.cursor()

    latest_nature_rune_price = cursor.execute('''SELECT low_price FROM latest WHERE item_id = 561''').fetchone()
    conn.close()

    return latest_nature_rune_price[0]


def _get_calculated_values(item):
    calculated_values = {'request_id': _get_request_id(item),
                         'item_name': _get_item_name(item),
                         'item_id': _get_item_id(item),
                         'pre_tax_margin': _get_pre_tax_margin(item),
                         'tax': _get_tax(item),
                         'post_tax_margin': _get_post_tax_margin(item),
                         'flip_roi': _get_flip_roi(item),
                         'highalch_margin': _get_highalch_margin(item),
                         'highalch_roi': _get_highalch_roi(item)}
    return calculated_values


def _get_item_name(item):
    return item[0]


def _get_request_id(item):
    return item[2]


def _get_item_id(item):
    return item[3]


def _get_pre_tax_margin(item):
    pre_tax_margin = item[5] - item[4]
    return pre_tax_margin


def _get_tax(item):
    item_tax = item[5] * tax_rate
    return math.floor(item_tax)


def _get_post_tax_margin(item):
    post_tax_margin = (item[5] - _get_tax(item)) - item[4]
    return round(post_tax_margin)


def _get_flip_roi(item):
    flip_roi = (_get_post_tax_margin(item) / item[4]) * 100
    return round(flip_roi)


def _get_highalch_margin(item):
    highalch_margin = item[1] - item[4] - _get_nature_rune_price()
    return round(highalch_margin)


def _get_highalch_roi(item):
    highalch_roi = (_get_highalch_margin(item) / item[4]) * 100
    return round(highalch_roi)
