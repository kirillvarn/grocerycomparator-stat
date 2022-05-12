from tkinter import Y
import pandas as pd
import numpy as np
import json
import glob
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

pd.options.display.float_format = "{:20,.2f}".format

score_list = glob.glob("*full_list.csv")
csv_list = glob.glob("../datasets/*.csv")

from_files_data = [pd.read_csv(f, delimiter=";", header=0) for f in score_list]
rscore_dataset = pd.concat(from_files_data, axis=0)


from_files_data = [pd.read_csv(f, delimiter=",", header=0) for f in csv_list]
index = from_files_data[0].index
for i in from_files_data:
    i.index = index


extrapolated = pd.read_csv("../datasets/extrapolate/extrapolated_products.csv")
dataset = pd.concat(from_files_data, axis=1)
rscore_dataset = rscore_dataset[rscore_dataset["R squared"].between(0.25, 0.90)]

pred_list = list()
progress = 0
total = len(rscore_dataset)
print("")

for index, row in rscore_dataset.iterrows():
    if '32969, Pruun roosuhkur (rafineerimata), SOL "MARRON, 500 g' in row["Predictor variable"].replace("\'", "\""):
        name = row["Predictor variable"].replace("\'", "\"").replace('SOL "MARRON', "SOL 'MARRON")
    else:
        name = row["Predictor variable"].replace("\'", "\"")
    r_d = json.loads(name)

    y_name = row["Response variable"]
    x_names = [n for n in r_d]

    inf_predict = extrapolated[x_names]

    y = dataset[y_name]
    x = dataset[x_names]

    x_train, x_test, y_train, y_test = train_test_split( x, y, test_size=0.2, random_state=0)

    reg = LinearRegression()
    reg.fit(x_train, y_train)
    y_pred = reg.predict(inf_predict)
    pred_list.append({"dependent": y_name, "parameters": x_names, "predicted": y_pred.tolist(), "values": inf_predict.to_json()})
    progress += 1
    print("\033[A                             \033[A")
    print(f"{progress}/{total} done.")

json_object = json.dumps(pred_list, indent = 4)

# Writing to sample.json
with open("predicted_output.json", "w", encoding='UTF8') as outfile:
    outfile.write(json_object)


"""
pd.options.display.float_format = '{:20,.2f}'.format
df = pd.read_csv(filename, delimiter=";", header=0).sort_values(by=["R squared"], ascending=False)
df3 = df[df['R squared'].between(0, 0.90)]
print(df3.head(n=5))
"""
