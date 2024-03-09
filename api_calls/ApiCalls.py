import requests

headers = {"User-Agent": "Learning to use python :)"}

def get_item_mappings():
    item_mapping = requests.get("https://prices.runescape.wiki/api/v1/osrs/mapping", headers=headers)
    return item_mapping

def get_latest_prices():
    price_response = requests.get("https://prices.runescape.wiki/api/v1/osrs/latest", headers=headers)
    return price_response

def get_latest_prices_by_id(item_id):
    item_response = requests.get(f'https://prices.runescape.wiki/api/v1/osrs/latest?id={item_id}', headers=headers)
    return item_response
