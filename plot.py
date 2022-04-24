import seaborn as sns
import matplotlib.pyplot as plt
import json
import pandas as pd
import numpy as np
import csv

sns.color_palette("flare", as_cmap=True)
sns.set_theme(style="darkgrid")
sns.set_context("paper")

# topmost = ["30245, Mustsõstra-pavlova rullkook, GOURMET CLUB, 540 g",
#            "Napoleoni kook, 1,2 kg, EESTI PAGAR",
#            "Coop Kokad Kass Arturi kook 160g",
#            "Hiiumaa Pagar Porgandikook 360g"]


# lowmost = [
#     "Biskviitkook KINDER Milk Slice, 28g",
#     "Britta kook EESTI PAGAR, 900g",
#     "Teekook MK, 460g",
#     "Biskviitkook KINDER Pingui kakao 4x30g"]

topmost = [
"5282, Pitsapõhjapulber, VILMA, 400 g",
"4721, Õhukese pitsapõhja pulber, VILMA, 400 g",
"30931, Kiviahjupizza Hawaii, GRANDIOSA, 350 g",
"30390, Kiviahjupizza Superiore for Meat Lovers, GRANDIOSA, 350 g"
]

lowmost = [
"Külm. pitsa Supreme MEGA DI CATO,380g",
"Pitsakate NÕO, 300g",
"Külm.pitsa VICI suits.pepperoniga,300g",
"Külm.pitsa VICI Neapoli tomat-oliiv.,300"
]


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


def scatter(filename, csv_filenames):
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
    fig, axes = plt.subplots(2, 4)
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
                                    data=p_df, ci=None, truncate=truncate, line_kws={'linewidth': 1}, scatter_kws={'alpha': 0.3})
            axes[index_1, s_in].set_title(p_df.iloc[:, 0].name, fontdict = {'fontsize' : 12})
            axes[index_1, s_in].set_yticklabels([])
            axes[index_1, s_in].set_xticklabels([])
            s.set(xlabel=" ")
            s.set(ylabel=" ")
            s_in += 1
    plt.show()


def mean(filename, output):
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
    mean_d = {}
    for item in val_l:
        if len(val_l[item]) > 0:
            mean_d[item] = np.mean(val_l[item])
        else:
            mean_d[item] = "N/A"

    with open(f"{output}.csv", encoding='utf-8', mode='w') as f:
        writer = csv.writer(f)
        writer.writerow(['Response variable', 'Mean R squared'])
        for i in mean_d:
            writer.writerow([i, mean_d[i]])


# mean("correlation_rimi milk_to_other shop milk.json")
scatter("correlation_pizza_to_wheat_beef.json",
        ["pizza.csv", "beef.csv", "wheat.csv"])
# scatter("correlation_cake_to_wheat_milk.json", ["cake.csv", "milk.csv", "wheat.csv"])

# mean("correlation_pizza_to_wheat_beef.json", "pizza_to_wheat_beef_mean")
#mean("correlation_cake_to_wheat_milk.json", "cake_to_wheat_milk_mean")
# scatter("correlation_rimi milk_to_other shop milk.json",
#         ["rimi milk.csv", "other shop milk.csv"])


# d = pd.read_csv("cake.csv")
# print(d[plottable])
# d = pd.read_csv("wheat.csv")
# print(d)
