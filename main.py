from database.request import create_request_table
from database.mapping import create_mapping_table, update_mapping_table
from database.latest import create_latest_table, update_latest_table
from database.five_min_history import create_five_min_history_table, update_five_min_history_table
from database.one_h_history import create_one_hour_history_table, update_one_hour_history_table
from item_margins.item_margins import get_item_margins


def main():
    create_mapping_table()
    create_request_table()
    create_latest_table()
    create_five_min_history_table()
    create_one_hour_history_table()

    update_mapping_table()
    update_latest_table()
    update_five_min_history_table()
    update_one_hour_history_table()

    get_item_margins()


if __name__ == "__main__":
    main()