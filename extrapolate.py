import numpy as np
import pandas as pd
import glob

def extrapolate_prices(inflation : int) -> list:
    csv_list = glob.glob("datasets/*.csv")
    from_files_data = [pd.read_csv(f) for f in csv_list]
    index = from_files_data[0].index
    for i in from_files_data:
        i.index=index

    dataset = pd.concat(from_files_data, axis=1)
    dataset = dataset.iloc[[-1]]
    dataset.reset_index(drop=True, inplace=True)
    inflation = inflation / 100
    e_dict = {}
    for year in range(0, 12):
        for col in dataset.columns:
            if year == 0:
                val : float = dataset[col].values[0]
                e_dict[col] = [val * (1 + inflation)]
            else:
                val : float = e_dict[col][year-1]
                e_dict[col].append(val * (1 + inflation))

    extr_dataset = pd.DataFrame.from_dict(e_dict)
    dataset = pd.concat([dataset, extr_dataset])
    return dataset.reset_index(drop=True)

dataset = extrapolate_prices(2.47)
dataset.to_csv("datasets/extrapolate/extrapolated_products.csv")