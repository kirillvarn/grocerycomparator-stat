import os
from distutils import core
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import main
from datetime import datetime
import export.excel as excel
import export.csv as csv
from export.gdrive import save_to_drive
#import seaborn as sns
import json

# sklearn
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

# CONSTANTS
not_all = ["taldrik", "geel", "šampoo", "paber", "vahend", "colgate", "blend-a-", "jordan", "dušš", "tampoon", "mähkme", "Pesukaitsmed", "Hügieenisidemed", "dove", "katlakivi", "värskendaja", "wc-", "küünal", "koeratoit", "kassikonserv", "kasstoit", "kiisueine"]

not_all_string_list = [f"AND name not ILIKE '%%{st}%%'" for st in not_all]
joined_st = " ".join(not_all_string_list)

wheat_kilos = 1
query_to_parse: dict = {
    # "milk": "SELECT * FROM \"%s\" WHERE price != 0 AND discount = false AND (name ILIKE '%%1l%%' OR name ILIKE '%%1 l%%') AND (name ILIKE '%%piim %%' OR name ILIKE '%%piim,%%') AND name NOT ILIKE '%%juust%%' AND name NOT ILIKE '%%kohupiim%%' AND name NOT ILIKE '%%laktoos%%' AND name NOT ILIKE '%%täis%%' AND name NOT ILIKE '%%kookos%%' AND name NOT ILIKE '%%latte%%' AND (name ILIKE '%%2,5%%' OR name ILIKE '%%2.5%%')",
    # "eggs": f"SELECT * FROM \"%s\" WHERE price != 0 AND discount = false AND name ILIKE '%%munad %%' OR name ILIKE '%%munad, %%' OR name ILIKE '%%muna,%%'",
    # "wheat": f"SELECT * FROM \"%s\" WHERE price != 0 AND discount = false AND (name ILIKE '%%{wheat_kilos}kg%%' OR name ILIKE '%%{wheat_kilos} kg%%') AND (name ILIKE '%%nisujahu %%' OR name ILIKE '%%nisujahu,%%')",
    # "tomatoes": "SELECT * FROM \"%s\" WHERE price != 0 AND discount = false AND (name ILIKE '%%tomat %%' OR name ILIKE '%%tomat, %%') AND name NOT ILIKE '%%pasta%%' AND name NOT ILIKE '%%0g%%' AND name NOT ILIKE '%%0 g%%' AND name NOT ILIKE '%%harilik%%' AND name NOT ILIKE '%%krõpsud%%' AND name NOT ILIKE '%%marinaad%%' AND name NOT ILIKE '%%eine%%'",
    # "cucumber": "SELECT * FROM \"%s\" WHERE price != 0 AND discount = false AND name ILIKE '%%kg%%' AND (name ILIKE '%%kurk %%' OR name ILIKE '%%kurk,%%')",
    # "banana": "SELECT * FROM \"%s\" WHERE price != 0 AND discount = false AND (name ILIKE '%%kg%%' OR name ILIKE '%%chiq%%') AND (name ILIKE '%%banaan %%' OR name ILIKE '%%banaan,%%')",
    # "apple": "SELECT * FROM \"%s\" WHERE price != 0 AND discount = false AND name ILIKE '%%kg%%' AND (name ILIKE '%%õun %%' OR name ILIKE '%%õun,%%')",
    # "pear": "SELECT * FROM \"%s\" WHERE price != 0 AND discount = false AND name ILIKE '%%kg%%' AND (name ILIKE '%%pirn %%' OR name ILIKE '%%pirn,%%')",
    "all": f"SELECT * FROM \"%s\" WHERE price != 0 AND price < 50 AND discount = false {joined_st}",
}
'''
table = excel.Excel()
table.create_sheets(query_to_parse.keys(), addition_sheet_name="regression")
'''

try:
    os.remove("correlation_lower_half.json")
except FileNotFoundError:
    pass

try:
    os.remove("correlation_upper_half.json")
except FileNotFoundError:
    pass


def get_products():
    return main.get_prices(main.connect(db="naive_products"))[1]


def get_products_by_name(name: str = "", query: str = ""):
    if len(name) != 0:
        return main.get_prices(main.connect(db="naive_products"), search_string=name)[1]
    else:
        return main.get_prices(main.connect(db="naive_products"), query=query)[1]

def get_normalized_price(data: list) -> list:
    new_data = list()
    for index, item in enumerate(data):
        if index == 0 and item == None:
            new_data.append(next(item for item in data if item is not None))
        elif index != 0 and data[index] == None:
            new_data.append(new_data[index - 1])
        else:
            new_data.append(item)

    return new_data


def get_trend(data: list) -> list:
    new_data = list()
    for index, item in enumerate(data):
        if index != 0:
            trend = "still"
            if data[index - 1] != None:
                if item > data[index - 1]:
                    trend = "up"
                elif item < data[index - 1]:
                    trend = "down"
            new_data.append({"value": item, "trend": trend})
    return new_data


# def save_to_excel(dataset, sheet_name: str = "Sheet") -> None:
#     tables = [i[0] for i in main.get_tables(main.connect(db="naive_products"))]
#     # tables.remove("initial_products")
#     header = ["Product name", "Shop name"] + tables
#     data = []

#     for item in dataset:
#         prices = get_normalized_price(
#             [dataset[item]["prices"][value]
#                 for value in dataset[item]["prices"]]
#         )
#         prices = get_trend(prices)
#         value = [item, dataset[item]["shop"]] + prices
#         data.append(value)

#     table.append_header(header, sheet_name)
#     table.put_data(data, sheet_name)


def save_to_csv(filename, dataset) -> None:
    data = []
    for item in dataset:
        prices = get_normalized_price(
            [dataset[item]["prices"][value]
                for value in dataset[item]["prices"]]
        )
        value = [item] + prices
        data.append(value)

    csv.write_to_csv(f"{filename}.csv", zip(*data))


def save_files():
    for item in query_to_parse:
        products = get_products_by_name(query=query_to_parse[item])
        save_to_csv(item, products)

save_files()