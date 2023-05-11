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
# C imports
cimport numpy as np
np.import_array()

simplefilter("ignore", category=ConvergenceWarning)

cpdef void write_to_file(str filename, data, list correlate_to=[], model="lregression"):
    correlate_to = [x.split("/")[1] for x in correlate_to]
    filename = filename.split("/")[1]
    cdef str c_to_string = "_".join(correlate_to)
    fname = filename if len(
        correlate_to) == 0 else f"correlation_{filename}_to_{c_to_string}"
    fname = model + "_" + fname
    with open(f"{fname}.json", "w", encoding='UTF8') as f:
        jsob = json.dumps(data, ensure_ascii=False)
        f.write(jsob)

cpdef void correlate_by_one(str dependent_file, list independent_files, bint allow_same=False, str model="lregression"):
    cdef list correlation = []
    cdef list headers = []
    cdef set i_files_product
    cdef list i_fname
    cdef dict cor_d
    cdef str filename = dependent_file.split(".")[0]
    cdef int process = 0
    cdef Py_ssize_t dep
    cdef tuple prod_tuple
    cdef unsigned short file_count = 1

    print(independent_files)

    dependent_data = pd.read_csv(dependent_file, dtype=np.double)
    from_files_data = [pd.read_csv(f, dtype=np.double)
                    for f in independent_files]

    headers = [list(x.keys()) for x in from_files_data][0]
    print(headers)
    dataset = pd.concat(from_files_data)
    i_files_product = set(itertools.combinations(headers, r=len(independent_files)))
    i_fname = [x.split(".")[0] for x in independent_files]
    print(i_files_product)
    exit()

    cdef Py_ssize_t dependent_arr = dependent_data.shape[1]
    cdef float score
    cdef dict param_coef_l = {}
    cdef float[:] coeff
    cdef unsigned short produc_len = dependent_data.shape[0]
    cdef np.ndarray[np.double_t, ndim=1] y
    #cdef np.ndarray[np.str, ndim=1] t_array
    cdef str t_val
    cdef np.ndarray[double, ndim=1] arr, y_pred
    cdef unsigned short cf

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

# each dependent is being regressed to whole independent dataset
cpdef void correlate(str first_file, list other_files=[], bint each=False):
    cdef list correlation = []
    cdef dict cor_d
    cdef str y, x, file
    cdef np.ndarray resp, pred
    cdef float score
    cdef str filename = first_file.split(".")[0]
    cdef list other_fnames = [x.split(".")[0] for x in other_files]

    if len(other_files) > 0:
        dependent_data = pd.read_csv(first_file, dtype=np.float32)

        for file in other_files:
            independent_data = pd.read_csv(file, dtype=np.float32)

            for y in dependent_data:
                resp = dependent_data[y].values
                pred = independent_data.values

                predictor = [{"name": x, "values": independent_data[x].values.tolist()}
                             for x in independent_data]
                x_train, x_test, y_train, y_test = train_test_split(
                    pred, resp, test_size=0.33, random_state=0)

                reg = LinearRegression()
                reg.fit(x_train, y_train)
                y_pred = reg.predict(x_test)

                score = r2_score(y_test, y_pred)
                if score > 0.1 and score <= 0.95:
                    cor_d = {"dependent": y, "independent_file": file, "score": score,
                             "response": resp.flatten().tolist(), "predictor": predictor}
                    correlation.append(cor_d)
        write_to_file(filename, correlation, other_fnames)

    else:
        data = pd.read_csv(first_file, dtype=np.float32)

        for y in data:
            for x in data:
                if x != y:
                    resp = data[y].values.reshape(-1, 1)
                    pred = data[x].values.reshape(-1, 1)
                    x_train, x_test, y_train, y_test = train_test_split(
                        pred, resp, test_size=0.33, random_state=0)

                    reg = LinearRegression()
                    reg.fit(x_train, y_train)
                    y_pred = reg.predict(x_test)

                    score = r2_score(y_test, y_pred)

                    if score > 0.1 and score <= 0.95:
                        cor_d = {"dependent": y, "independent": x, "score": score, "response": resp.flatten(
                        ).tolist(), "predictor": pred.flatten().tolist()}
                        correlation.append(cor_d)
            data.drop(columns=[y])

        write_to_file(filename, correlation, other_fnames)
