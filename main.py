from database.Mapping import create_mapping_table
from database.Mapping import update_mapping_table
from database.Request import create_request_table
from database.Latest import create_latest_table
from database.Latest import update_latest_table


def main():
    create_mapping_table()
    create_request_table()
    create_latest_table()
    update_mapping_table()
    update_latest_table()


if __name__ == "__main__":
    main()