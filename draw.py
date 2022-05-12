import seaborn as sns
import matplotlib.pyplot as plt
import json
import pandas as pd
import numpy as np
import csv
import warnings
from statsmodels.tools.sm_exceptions import ConvergenceWarning
warnings.simplefilter('ignore', ConvergenceWarning)


lower = 0
upper = 1

font = {'family': 'monospace',
        'weight': 'bold',
        'size': 20}


PLOT_MARGIN = 0.25
HEIGHT = 1920
WIDTH = 1200
'''
 filenname: .json file with correlation data
 csv_filename: list of .csv files with price data
 plottable: 2D array with topmost and lowermost dependent parameters
'''
def scatter_reg(filename: str, csv_filenames: list[str], plottable: list):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

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

    _, axes = plt.subplots(2, 3, figsize=(19, 11))
    for index_1, _ in enumerate(plottable):
        s_in = 0
        for p_df in plottable_df[index_1]:
            p_df = p_df.loc[:, ~p_df.columns.duplicated()]

            y_max, y_min = np.amax(p_df.iloc[:, 0]), np.amin(p_df.iloc[:, 0])
            x_max, x_min = np.amax(p_df.values), np.amin(p_df.values)

            for _, d in enumerate(p_df):
                if p_df.iloc[:, 0].name != d:
                    if len(set(p_df[d])) > 1:
                        s = sns.regplot(ax=axes[index_1, s_in], y=p_df.iloc[:, 0].name, x=d,
                                        data=p_df, ci=None, truncate=False, robust=True, line_kws={'linewidth': 0.6}, scatter_kws={'alpha': 0.5})

                        y_delta = 0.2
                        x_delta = 1.4

                        s.set_ylim((y_min - y_delta, y_max + y_delta))
                        s.set_xlim((x_min - x_delta, x_max + x_delta))

            name = p_df.iloc[:, 0].name
            name = (name[:40] + '..') if len(name) > 44 else name
            try:
                int(name.split(",")[0])
                name = "".join(name.split(",")[1:])
            except:
                name = name
            axes[index_1, s_in].set_title(
                name, fontdict={'fontsize': 21})
            s.set(xlabel=" ")
            s.set(ylabel=" ")
            s_in += 1

    png_fname = filename.split(".")[0] + ".png"
    plt.tight_layout()

    plt.savefig(f"plots/{png_fname}", format="png", bbox_inches='tight', dpi=300)

'''
    filename: .json file with correlation data
    csv_filenames: list of .csv files with independent parameters
    name_list: list of dependent parameters
'''
def scatter(filename: str, csv_filenames: list[str], name_list: list[str]):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    from_files_data = [pd.read_csv(f, dtype=np.float32) for f in csv_filenames]
    dataframe = pd.concat(from_files_data, axis=1)

    dataframe_rimi = from_files_data[0]

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

'''
    filename: .json filename with correlation data
    output: output .csv file
    allow_same: do you want to allow the same x and y values?
    get_top: return top 3 values
'''
def mean(filename: str, output: str, allow_same=False, get_top=False) -> dict:
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    dep_v = [i['dependent'] for i in data]
    dep_v = list(set((dep_v)))

    val_l = {}
    for i in dep_v:
        val_l[i] = []

    with open(f"mean/{output}_full_list.csv", encoding='utf-8', mode='w', newline='') as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(['Response variable', 'Predictor variable', 'R squared'])
        for item in data:
            writer.writerow([item["dependent"], item["independent_parameters"], item["score"]])


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

    mean_d = {k: v for k, v in sorted(mean_d.items(), reverse=True, key=lambda item: item[1])}
    with open(f"{output}.csv", encoding='utf-8', mode='w', newline='') as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(['Response variable', 'Mean R squared'])
        for i in mean_d:
            writer.writerow([i, mean_d[i]])

    if get_top:
        top = [i for i in mean_d if mean_d[i] != 0][:3]
        bot = [i for i in mean_d if mean_d[i] != 0][-3:]
        return [top, bot]

'''
    dependent: product name from the datasets
    csv_files: list of csv_files where your independent paramters are stored
    filename: output filename
'''
def plot_names(dependent: str, csv_files: list, filename: str):
    from_files_data = [pd.read_csv(f, dtype=np.float32) for f in csv_files]
    dataframe = pd.concat(from_files_data, axis=1)

    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)
    indep = [[j.lstrip("parameter ") for j in i["independent_parameters"]] for i in data if i['score'] != 1]
    indep = np.array(indep).flatten().tolist()
    indep = list(set(indep))

    # plt.tight_layout()
    for name in indep:
        truncate = True
        if len(set(dataframe[name])) > 1:
            truncate = False
        plt.figure(figsize = (10, 8))
        plt.xlim((-1.1, 16.5))
        plt.ylim((4.6, 8.3))
        s = sns.regplot(y=dependent, x=name, data=dataframe, ci=None, robust=True, truncate=truncate, line_kws={'linewidth': 1.0})

        xl = name.replace("%", "\%")
        s.set_xlabel(f"{xl} (€)", fontsize=26)
        s.set_ylabel(f"{dependent} (€)", fontsize=26)
        fig = s.get_figure()

        filename = f"{dependent}_{name}"
        filename = "".join(x for x in filename if x.isalnum()) + ".png"
        plt.tight_layout()
        try:
            fig.savefig(f"plot_t/{filename}", format="png", bbox_inches='tight', dpi=300)
        except:
            print(f"Could not save: {filename}")
        fig.clf()


def draw_line(csv_f):
    from_files_data = [pd.read_csv(f, dtype=np.float32) for f in csv_f]
    df = pd.concat(from_files_data, axis=1)

    for i in df.columns:
        sns.lineplot(data=df, x=df[i], y=df["498187, Šokolaadikook, ERIK ORGU, 325 g"])
        plt.show()
