import seaborn as sns
import matplotlib.pyplot as plt
import json
import pandas as pd
import numpy as np
import csv

# sns.color_palette("flare", as_cmap=True)
# sns.set_theme(style="darkgrid")
# sns.set_context("paper")
plt.style.use(['science'])

topmost = [
    "498187, Šokolaadikook, ERIK ORGU, 325 g",
    "31655, Erik Orgu kohupiimakook, ERIK ORGU, 325 g",
    "984488, Toorjuustukook sidrunimaitseline Farmi 250g"]


lowmost = [
    "Pasha kook 300 g, EESTI PAGAR",
    "Napoleoni kook EESTI PAGAR, 1.2kg",
    "Meekook EESTI PAGAR, 1kg"]

# topmost = [
# "5282, Pitsapõhjapulber, VILMA, 400 g",
# "4721, Õhukese pitsapõhja pulber, VILMA, 400 g",
# "30931, Kiviahjupizza Hawaii, GRANDIOSA, 350 g",
# "30390, Kiviahjupizza Superiore for Meat Lovers, GRANDIOSA, 350 g"
# ]

# lowmost = [
# "Külm. pitsa Supreme MEGA DI CATO,380g",
# "Pitsakate NÕO, 300g",
# "Külm.pitsa VICI suits.pepperoniga,300g",
# "Külm.pitsa VICI Neapoli tomat-oliiv.,300"
# ]

# topmost = ["200289, Piim Alma kile 2,5% 1l", "812489, Piim Rimi 2,5% 1l"]
# lowmost = []

# topmost = [
#     "30390, Kiviahjupizza Superiore for Meat Lovers, GRANDIOSA, 350 g",
#     "30931, Kiviahjupizza Hawaii, GRANDIOSA, 350 g",
#     "4721, Õhukese pitsapõhja pulber, VILMA, 400 g",
#     "5282, Pitsapõhjapulber, VILMA, 400 g"
# ]

# lowmost = [
#     "Külm. pitsa Supreme MEGA DI CATO,380g",
#     "Külm. pitsa Mafia MEGA DI CATO,380g",
#     "Pitsakate NÕO, 300g",
#     "812436, Pitsa Rimi Basic singi ja seente 325g"
# ]

plottable = [topmost, lowmost]


#lottable = ["32239, Šokolaadi-Napoleoni kook, EESTI PAGAR, 400 g", "Küpsisekook 280 g, EESTI PAGAR", "810062, Maasika-jogurtikook Rimi 350g", "32779, Mustasõstra-passionikook, PAGARINI, 300 g", "812238, Britta kook Rimi 300g"]

lower = 0
upper = 1

font = {'family': 'monospace',
        'weight': 'bold',
        'size': 20}


def scatter_reg(filename, csv_filenames):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    # dep_names = list(set([i['dependent'] for i in data]))
    dep_names = plottable

    pl_list = []
    for p_item in plottable:
        p_dict = {}

        for pl in p_item:
            p_dict[pl] = []

        for pl in p_item:
            in_v = [i['independent_parameters']
                    for i in data if i['dependent'] == pl]
            in_v = [list(i.keys()) for i in in_v]
            in_v = np.array(in_v).flatten().tolist()
            in_v = [w.lstrip('parameter').strip() for w in in_v]
            p_dict[pl] = in_v

        pl_list.append(p_dict)

    from_files_data = [pd.read_csv(f, dtype=np.float32) for f in csv_filenames]
    dataframe = pd.concat(from_files_data, axis=1)

    dataset = [item for item in data if item['score']
               >= lower and item['score'] <= upper]

    plottable_df = []
    for pl_v in pl_list:
        df_l_temp = []
        for df in pl_v:
            unduplicated = list(set(pl_v[df]))
            dep = dataframe[df]
            indep = dataframe[unduplicated]
            fin_df = pd.concat([dep, indep], axis=1)
            df_l_temp.append(fin_df)
        plottable_df.append(df_l_temp)

    # plt.axis([-15, 30, -15, 30])
    # plt.figure(figsize=(12, 8))
    fig, axes = plt.subplots(2, 3)
    for index_1, top in enumerate(plottable):
        s_in = 0
        for p_df in plottable_df[index_1]:
            p_df = p_df.loc[:, ~p_df.columns.duplicated()]
            for index_2, d in enumerate(p_df):
                if p_df.iloc[:, 0].name != d:
                    truncate = True
                    print(set(p_df[d]))
                    if len(set(p_df[d])) > 1:
                        truncate = False
                    s = sns.regplot(ax=axes[index_1, s_in], y=p_df.iloc[:, 0].name, x=d,
                                    data=p_df, ci=None, truncate=truncate,line_kws={'linewidth': 0.6}, scatter_kws={'alpha': 0.5})
                    s.set_ylim([-8, 32])
                    s.set_xlim([-8, 24])
            axes[index_1, s_in].set_title(
                p_df.iloc[:, 0].name, fontdict={'fontsize': 20})
            # axes[index_1, s_in].set_yticklabels([[0, 0.2, 0.4, 0.6, 0.8, 1.0]])
            # axes[index_1, s_in].set_xticklabels([0, 0.2, 0.4, 0.6, 0.8, 1.0])
            # s.set(xlabel=" ")
            # s.set(ylabel=" ")
            s.set_ylabel("€",horizontalalignment='right', y=1.0, labelpad=-8, fontsize=16)
            s.set_xlabel("€",horizontalalignment='right', x=1.0, labelpad=-8, fontsize=16)
            s_in += 1
    plt.show()


def scatter(filename, csv_filenames, name_list):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    from_files_data = [pd.read_csv(f, dtype=np.float32) for f in csv_filenames]
    dataframe = pd.concat(from_files_data, axis=1)

    dataframe_rimi = from_files_data[0]
    dataframe_other = from_files_data[1]

    for name in name_list:
        cols = dataframe_rimi.columns.to_list()
        cols.remove(name)
        data = dataframe.drop(columns=cols)
        plt.figure(figsize=(10, 8))
        for i in data:
            s = sns.scatterplot(y=name, x=i,  data=dataframe, style=i,
                                legend=None, s=92, alpha=0.6, linewidth=0.25)
        yl = name.replace("%", "\%")
        s.set_ylabel(f"{yl} (\u20ac)", fontsize=30)
        s.set_xlabel(f"Other milk (\u20ac)", fontsize=30)
        plt.show()


def mean(filename, output, allow_same=False):
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

        if score < 1:
            val_l[item['dependent']] += [score]

        if allow_same:
            val_l[item['dependent']] += [score]

    mean_d = {}
    for item in val_l:
        if allow_same:
            mean_d[item] = np.mean(val_l[item])
        elif len(val_l[item]) > 0:
            mean_d[item] = np.mean(val_l[item])
        else:
            mean_d[item] = "N/A"

    with open(f"{output}.csv", encoding='utf-8', mode='w') as f:
        writer = csv.writer(f)
        writer.writerow(['Response variable', 'Mean R squared'])
        for i in mean_d:
            writer.writerow([i, mean_d[i]])


# mean("correlation_rimi milk_to_other shop milk.json", "rimi_to_other_mean", True)
# scatter("correlation_pizza_to_wheat_beef.json",
#         ["pizza.csv", "beef.csv", "wheat.csv"])
scatter_reg("correlation_cake_to_wheat_milk.json", ["datasets/cake.csv", "datasets/milk.csv", "datasets/wheat.csv"])

# mean("correlation_pizza_to_wheat_beef.json", "pizza_to_wheat_beef_mean")
# mean("correlation_pizza_to_wheat_chicken.json", "pizza_to_wheat_chicken_mean")
# mean("correlation_pizza_to_wheat_pig meat.json", "pizza_to_wheat_pigmeat_mean")
# mean("correlation_cake_to_wheat_milk.json", "cake_to_wheat_milk_mean")
# scatter("correlation_rimi milk_to_other shop milk.json",
#         ["datasets/rimi milk.csv", "datasets/other shop milk.csv"], topmost)


# d = pd.read_csv("cake.csv")
# print(d[plottable])
# d = pd.read_csv("wheat.csv")
# print(d)
