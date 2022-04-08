import numpy as np
import pandas as pd
import math
import random
import matplotlib.pyplot as plt
import main
import datetime as dt
from matplotlib.ticker import FormatStrFormatter
from datetime import datetime


def datetime_to_epoch(datetimes: list) -> list:
    epochs = []
    for dt in datetimes:
        if dt == "initial_products":
            dt = "2022-03-06"
        epoch = datetime.fromisoformat(dt).timestamp()
        epochs.append(epoch)
    return epochs


dataset = main.get_prices(main.connect())[1]

lenDict = dict()
for item in dataset:
    notNone = [value for value in dataset[item]
               if dataset[item][value] != None]
    if len(notNone) > 1:
        lenDict[item] = len(notNone)

sorted_tuple_desc = sorted(lenDict.items(), key=lambda item: item[1])
names = [item[0] for item in sorted_tuple_desc if item[1] < 8][-10:]

top_list = list()
for i in names:
    top_list.append(dataset[i])

chosen_item = dataset["977184, Kihiline suitsukalasalat 500 g"]
dates = [i for i in chosen_item]
epochs = datetime_to_epoch(dates)

values = [chosen_item[i] for i in chosen_item]

plt.plot(epochs, values, 'o')
plt.show()
# df = pd.DataFrame(data=top_list, index=names)
# print(df)
