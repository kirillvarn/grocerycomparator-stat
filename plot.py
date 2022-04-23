import seaborn as sns
import matplotlib.pyplot as plt
import json
import pandas as pd
import numpy as np
from scipy import stats

sns.color_palette("flare", as_cmap=True)
sns.set_theme(style="darkgrid")
sns.set_context("paper")
plt.axis([-15, 30, -15, 30])

font = {'family' : 'monospace',
        'weight' : 'bold',
        'size'   : 20}

def scatter(filename, csv_filenames):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    dataset = dict()

    from_files_data = [pd.read_csv(f, dtype=np.float32) for f in csv_filenames]
    dataset = pd.concat(from_files_data, axis=1)

    high_r2 = [item for item in data if item['score'] >= 0.5 and item['score'] < 0.95]
    low_r2 = [item for item in data if item['score'] < 0.5 and item['score'] > 0.05]


    high_names = [{"dependent": item['dependent'], "independent": [par.lstrip(
        "parameter").strip() for par in item['independent_parameters']]} for item in high_r2]
    low_names = [{"dependent": item['dependent'], "independent": [par.lstrip(
        "parameter").strip() for par in item['independent_parameters']]} for item in low_r2]

    dep_values_h = {item['dependent']: np.array(
        dataset[item['dependent']]) for item in high_names}
    dep_values_l = {item['dependent']: np.array(
        dataset[item['dependent']]) for item in low_names}

    indep_values_h = np.array([item['independent']
                              for item in high_names]).flatten()
    indep_values_l = np.array([item['independent']
                              for item in low_names]).flatten()

    indep_values_h = {item: np.array(dataset[item]) for item in indep_values_h}
    indep_values_l = {item: np.array(dataset[item]) for item in indep_values_l}

    for name in high_names:
        for ind in name['independent']:
            try:
                slope, intercept, r_value, p_value, std_err = stats.linregress(
                    dataset[ind], dataset[name['dependent']])
                line_k = {
                    'label': "y={0:.1f}x+{1:.1f}".format(slope, intercept)}
            except:
                line_k = None


            if line_k == None:
                truncate = True
            else:
                truncate = False

            rp = sns.regplot(data=dataset, x=ind,
                             y=name['dependent'], ci=None, line_kws=line_k, truncate=truncate, color="#e36459")
            if line_k != None:
                rp.legend()

            plt.xlabel(ind, fontsize=16)
            plt.ylabel(name['dependent'],fontsize=16)

            plt.legend(fontsize=16)
            plt.show()

    for name in low_names:
        for ind in name['independent']:
            try:
                slope, intercept, r_value, p_value, std_err = stats.linregress(
                    dataset[ind], dataset[name['dependent']])
                line_k = {
                    'label': "y={0:.1f}x+{1:.1f}".format(slope, intercept)}
            except:
                line_k = None

            rp = sns.regplot(data=dataset, x=ind,
                             y=name['dependent'], ci=None, line_kws=line_k, truncate=False, color="#e36459")
            if line_k != None:
                rp.legend()
            plt.xlabel(ind, fontsize=16)
            plt.ylabel(name['dependent'], fontsize=16)
            plt.legend(fontsize=16)
            plt.rc('font', **font)
            plt.show()

def mean(filename):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    dep_v = [i['dependent'] for i in data]
    dep_v = list(set((dep_v)))
    print(dep_v)


mean("correlation_rimi milk_to_other shop milk.json")
# scatter("correlation_pizza_to_wheat_pig meat.json",
#         ["pizza.csv", "pig meat.csv", "wheat.csv"])
# scatter("correlation_rimi milk_to_other shop milk.json",
        # ["rimi milk.csv", "other shop milk.csv"])