from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lars
from sklearn.linear_model import RidgeCV
from sklearn.linear_model import LassoCV
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.gaussian_process import GaussianProcessRegressor
import json
import os
import pandas as pd
import numpy as np
import itertools

from sklearn.exceptions import ConvergenceWarning
from warnings import simplefilter

simplefilter("ignore", category=ConvergenceWarning)

def write_to_file(filename, data, correlate_to=[], model="lregression"):
    correlate_to = [x.split("/")[1] for x in correlate_to]
    filename = filename.split("/")[1]
    c_to_ng = "_".join(correlate_to)
    fname = filename if len(
        correlate_to) == 0 else f"correlation_{filename}_to_{c_to_ng}"
    fname = model + "_" + fname
    with open(f"{fname}.json", "w", encoding='UTF8') as f:
        jsob = json.dumps(data, ensure_ascii=False)
        f.write(jsob)

def correlate_by_one(dependent_file, independent_files, allow_same=False, model="lregression"):
    correlation = []
    headers = []
    filename = dependent_file.split(".")[0]
    process = 0
    file_count = 1

    print(independent_files)

    dependent_data = pd.read_csv(dependent_file, dtype=np.double)
    from_files_data = [pd.read_csv(f, dtype=np.double)
                    for f in independent_files]

    headers = [list(x.keys()) for x in from_files_data]
    dataset = pd.concat(from_files_data)
    i_files_product = set(itertools.product(*headers))
    i_fname = [x.split(".")[0] for x in independent_files]

    dependent_arr = dependent_data.shape[1]
    # param_coef_l = {}
    # produc_len = dependent_data.shape[0]

    try:
        for dep in range(dependent_arr):
            for prod_tuple in i_files_product:
                y = dependent_data.iloc[:, dep].values
                if len(set(y)) > 1 or allow_same:
                    dataf = pd.DataFrame()
                    #t_array = prod_tuple

                    for t_val in prod_tuple:
                        arr = np.array(dataset[t_val].values)
                        dataf.insert(0, t_val, arr[~np.isnan(arr)])

                    x = dataf
                    if len(set(x.values.flatten())) > len(x.columns) or allow_same:
                        x_train, x_test, y_train, y_test = train_test_split( x, y, test_size=0.2, random_state=0, shuffle=False)
                        if model == "lregression":
                            ml_model = LinearRegression()

                        if model == "ridge":
                            ml_model = RidgeCV()

                        if model == "lasso":
                            ml_model = LassoCV()


                        ml_model.fit(x_train, y_train)
                        y_pred = ml_model.predict(x_test)
                        score = r2_score(y_test, y_pred)

                        if score > 0 and score <= 0.95:
                            cor_d = {"dependent": dependent_data.columns[dep], "model": model, "independent_parameters": prod_tuple, "score": score}
                            correlation.append(cor_d)
                process += 1
            print(f"{dependent_data.columns[dep]} is done. Progress: {file_count} out of {dependent_arr }")
            file_count += 1
        write_to_file(filename, correlation, i_fname, model=model)
    except Exception as e:
        print(e)