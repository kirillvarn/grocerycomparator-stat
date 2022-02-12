import psycopg2.extensions
import psycopg2
from credentials import user_data


# CONSTANTS

INITIAL_TABLE_NAME = "initial_table"

# type aliases
connection = psycopg2.extensions.connection

# SETTING UP THE CONNECTION #

# products
conn = psycopg2.connect(dbname=user_data['dbname'], user=user_data['username'],
                        password=user_data['password'], host=user_data['host'], port=user_data['port'])

# naive products
conn_naive = psycopg2.connect(dbname=user_data['naive_dbname'], host=user_data['host'],
                              port=user_data['port'], user=user_data['username'], password=user_data['password'])


def get_tables(conn: connection) -> list[tuple]:
    query_st: str = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name ASC"
    cursor = conn.cursor()
    cursor.execute(query_st)
    return cursor.fetchall()


def get_product(conn: connection) -> list[dict]:
    tables = get_tables(conn)
    data = dict()
    query_st: str = 'SELECT * FROM "%s"'
    for table in tables:
        cursor = conn.cursor()
        table_key = table[0].replace("'", "")
        cursor.execute(query_st, (table_key,))
        fetched = cursor.fetchall()

        normalized_data = dict()
        for item in fetched:
            if item[3] == "selver":
                normalized_data[item[0]] = {
                    "id": item[0], "name": item[1], "price": item[2], "shop": item[3], "dicount": item[4]}
            else:
                normalized_data[item[1]] = {
                    "id": item[0], "name": item[1], "price": item[2], "shop": item[3], "dicount": item[4]}

        data[table_key] = normalized_data
    return data


def get_names_and_ids(data: list[tuple]) -> list:
    return list(map(lambda x: x[0] if x[3] == "selver" else x[1], data))


def get_prices(conn: connection) -> dict[dict]:

    products = get_product(conn)
    data_keys = list(products.keys())

    price_data = dict()

    for d_key in data_keys:
        for item in products[d_key]:
            if products[d_key][item]["shop"] == "selver":
                key = f"{item}, {products[d_key][item]['name']}"
            else:
                key = item
            try:
                price_data[key] += [products[d_key][item]['price']]
            except:
                price_data[key] = [products[d_key][item]['price']]

    return data_keys, price_data