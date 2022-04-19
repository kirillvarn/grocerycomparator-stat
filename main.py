import psycopg2.extensions
import psycopg2
from colorama import Fore, Style
import time
from credentials import user_data


# CONSTANTS

INITIAL_TABLE_NAME = "initial_table"
RETRY_LIMIT = 20

# type aliases
connection = psycopg2.extensions.connection

# SETTING UP THE CONNECTION #

# products
# conn = psycopg2.connect(dbname=user_data['dbname'], user=user_data['username'],
#                        password=user_data['password'], host=user_data['host'], port=user_data['port'])

# naive products
# conn_naive = psycopg2.connect(dbname=user_data['naive_dbname'], host=user_data['host'],
#                              port=user_data['port'], user=user_data['username'], password=user_data['password'])


def connect(retries=0, db='products'):
    try:
        CONNECTION = psycopg2.connect(dbname=db, user=user_data['username'],
                                      password=user_data['password'], host=user_data['host'], port=user_data['port'])
        retries = 0
        return CONNECTION
    except psycopg2.OperationalError as error:
        if retries >= RETRY_LIMIT:
            raise error
        else:
            retries += 1
            print(
                f"{Fore.YELLOW}[WARNING]\n {error} reconnecting to {db} {retries}...{Style.RESET_ALL}")
            time.sleep(5)
            return connect(retries=retries, db=db)
    except (Exception, psycopg2.Error) as error:
        raise error


def get_tables(conn: connection) -> list[str]:
    query_st: str = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name != 'updatedates' ORDER BY table_name ASC "
    cursor = conn.cursor()
    cursor.execute(query_st)
    fetched_data = cursor.fetchall()
    return fetched_data


def get_product(conn: connection, search_string: str = '', query: str = '') -> list[dict]:
    tables = get_tables(conn)
    data = dict()

    if len(search_string) != 0:
        like_pattern = f"%{search_string}%"
        like_pattern_comma = f"%{search_string.strip()},%"

        query: str = 'SELECT * FROM "%s" WHERE price != 0 AND name ILIKE %s or name ILIKE %s'

    for table in tables:
        cursor = conn.cursor()
        table_key = table[0].replace("'", "")

        if len(search_string) != 0:
            query_params = (table_key, like_pattern, like_pattern_comma)
        else:
            query_params = (table_key, )

        cursor.execute(query, query_params)

        normalized_data = {v[1]: {
            "id": v[0], "name": v[1], "price": v[2], "shop": v[3], "discount": v[4]} for v in cursor.fetchall()}

        data[table_key] = normalized_data
    cursor.close()
    return data


def get_names_and_ids(data: list[tuple]) -> list:
    return list(map(lambda x: x[0] if x[3] == "selver" else x[1], data))


def get_prices(conn: connection, search_string: str = "", query: str = "") -> dict[dict]:
    if len(search_string) != 0:
        products = get_product(conn, search_strin=search_string)
    else:
        products = get_product(conn, query=query)

    data_keys = list(products.keys())

    price_data = dict()

    for d_key in data_keys:
        create_flag = False
        for item in products[d_key]:
            key = item

            if not create_flag and key not in price_data:
                price_data[key] = {'prices': {}}
                price_data[key]['prices'] = {v: None for v in data_keys}
                create_flag != create_flag

            try:
                price_data[key]['prices'][d_key] = products[d_key][item]['price']
            except:
                price_data[key]['prices'][d_key] = None
            price_data[key]['shop'] = products[d_key][item]['shop']
    return data_keys, price_data
