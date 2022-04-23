import seaborn as sns
import matplotlib.pyplot as plt
import json
import pandas as pd
import numpy as np
import csv
from scipy import stats

sns.color_palette("flare", as_cmap=True)
sns.set_theme(style="darkgrid")
sns.set_context("paper")
plt.axis([-15, 30, -15, 30])


plottable = ["200289, Piim Alma kile 2,5% 1l", "812489, Piim Rimi 2,5% 1l"]

lower = 0
upper = 1

font = {'family' : 'monospace',
        'weight' : 'bold',
        'size'   : 20}

def scatter(filename, csv_filenames):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    dep_names = list(set([i['dependent'] for i in data]))

    p_dict = {}
    for p_item in plottable:
        p_dict[p_item] = []

    for p_item in plottable:
        in_v = [i['independent_parameters'] for i in data if i['dependent'] == p_item]
        in_v = [list(i.keys()) for i in in_v]
        in_v = np.array(in_v).flatten().tolist()
        in_v = [w.lstrip('parameter').strip() for w in in_v]
        p_dict[p_item] = in_v


    dep_indep_dict = {i: [] for i in dep_names}
    dataset = dict()

    from_files_data = [pd.read_csv(f, dtype=np.float32) for f in csv_filenames]
    dataframe = pd.concat(from_files_data, axis=1)

    dataset = [item for item in data if item['score'] >= lower and item['score'] <= upper]

    plottable_df = []

    for df in p_dict:
        dep = dataframe[df]
        indep = dataframe[p_dict[df]]
        fin_df = pd.concat([dep, indep], axis=1)
        plottable_df.append(fin_df)
    for p_df in plottable_df:
        for index, d in enumerate(p_df):
            if p_df.iloc[:,0].name != d:
                s = sns.scatterplot( y=p_df.iloc[:,0].name, x=d, data=p_df, s=48, style=d, legend=False, alpha=0.5)
                s.set(xlabel="Milk")
        plt.show()


def mean(filename):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    dep_v = [i['dependent'] for i in data]
    dep_v = list(set((dep_v)))

    val_l = {}
    for i in dep_v:
        val_l[i] = []

    for item in data:
        score = item['score']
        if score < 0:
            score = 0
        val_l[item['dependent']] += [score]

    mean_d = {}
    print(val_l)
    for item in val_l:
        mean_d[item] = np.mean(val_l[item])

    with open(f"mean_milk.csv", encoding='utf-8', mode='w') as f:
        writer = csv.writer(f)
        writer.writerow(['Response variable', 'Mean R squared'])
        for i in mean_d:
            writer.writerow([i, mean_d[i]])



# mean("correlation_rimi milk_to_other shop milk.json")
# scatter("correlation_pizza_to_wheat_pig meat.json",
#         ["pizza.csv", "pig meat.csv", "wheat.csv"])
# scatter("correlation_cake_to_wheat_milk.json",
#         ["pizza.csv", "cake.csv", "wheat.csv"])
scatter("correlation_rimi milk_to_other shop milk.json",
        ["rimi milk.csv", "other shop milk.csv"])