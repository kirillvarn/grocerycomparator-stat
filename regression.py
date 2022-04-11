import numpy as np
import pandas as pd
import math
import random
import matplotlib.pyplot as plt
import main
import datetime as dt
from matplotlib.ticker import FormatStrFormatter
from datetime import datetime
import export.excel as excel


dataset = main.get_prices(main.connect())[1]


def datetime_to_epoch(datetimes: list) -> list:
    epochs = []
    for dt in datetimes:
        if dt == "initial_products":
            dt = "2022-03-06"
        epoch = datetime.fromisoformat(dt).timestamp()
        epochs.append(epoch)
    return epochs


def get_data() -> dict:
    pass


def save_to_excel(dataset):
    tables = [i[0] for i in main.get_tables(main.connect())]
    tables.remove('initial_products')
    header = ['Product name', '2022-03-06'] + tables
    data = []

    for item in dataset:
        value = [item] + [dataset[item][value] for value in dataset[item]]
        data.append(value)
    excel.save(data, "data", header)


def plot():
    chosen_item = dataset["977184, Kihiline suitsukalasalat 500 g"]

    dates = [i for i in chosen_item]
    epochs = datetime_to_epoch(dates)

    values = [chosen_item[i] for i in chosen_item]

    plt.plot(epochs, values, 'o')
    plt.show()


save_to_excel(dataset)

# lenDict = dict()
# for item in dataset:
#     notNone = [value for value in dataset[item]
#                if dataset[item][value] != None]
#     if len(notNone) > 1:
#         lenDict[item] = len(notNone)


# df = pd.DataFrame(data=top_list, index=names)
# print(df)
