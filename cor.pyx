from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
import json
import os
import pandas as pd
import numpy as np
import itertools

# C imports
cimport numpy as np
np.import_array()

cpdef void write_to_file(str filename, data, list correlate_to=[]):
    cdef str c_to_string = "_".join(correlate_to)
    fname = filename if len(
        correlate_to) == 0 else f"correlation_{filename}_to_{c_to_string}"

    with open(f"{fname}.json", "w", encoding='UTF8') as f:
        jsob = json.dumps(data, ensure_ascii=False)
        f.write(jsob)


cpdef void correlate_by_one(str dependent_file, list independent_files):
    cdef list correlation = []
    cdef np.ndarray i_files_product
    cdef list i_fname
    cdef dict cor_d
    cdef str filename = dependent_file.split(".")[0]
    cdef int process = 0
    cdef Py_ssize_t dep, prod_tuple
    cdef unsigned short file_count = 1
    #cdef float[:] x_train, x_test, y_train, y_test, y_pred

    dependent_data = pd.read_csv(dependent_file, dtype=np.float32)
    from_files_data = [pd.read_csv(f, dtype=np.float32)
                       for f in independent_files]

    headers = [list(x.keys()) for x in from_files_data]

    dataset = pd.concat(from_files_data)
    i_files_product = np.array(tuple(itertools.product(*headers)))

    i_fname = [x.split(".")[0] for x in independent_files]

    cdef int completion_p = dependent_data.shape[1] * i_files_product.shape[0]

    cdef Py_ssize_t dependent_arr = dependent_data.shape[1]
    cdef Py_ssize_t tuple_array = i_files_product.shape[0]
    cdef float score
    cdef dict param_coef_l = {}
    cdef float[:] coeff

    print("")
    for dep in range(dependent_arr):
        for prod_tuple in range(tuple_array):
            param_coef_l = {}
            print ("\033[A                             \033[A")
            print(f"{process}/{completion_p} done.")
            y = dependent_data.iloc[:, dep]

            if len(set(y)) > 1:
                dataf = pd.DataFrame()
                t_array = i_files_product[prod_tuple]
                for t_val in t_array.tolist():
                    arr = np.array(dataset[t_val].values)
                    dataf.insert(0, t_val, arr[~np.isnan(arr)])

                x = dataf
                x_train, x_test, y_train, y_test = train_test_split( x, y, test_size=0.2, random_state=0)
                reg = LinearRegression()
                reg.fit(x_train, y_train)
                coeff = reg.coef_

                for cf in range(coeff.shape[0]):
                    param_coef_l[f"parameter {t_array.tolist()[cf]}"] = coeff[cf]

                y_pred = reg.predict(x_test)
                score = r2_score(y_test, y_pred)

                #if score > 0.1:
                #    if score <= 0.95:
                t_array = np.array(t_array)
                cor_d = {"dependent": dependent_data.columns[dep], "independent_parameters": param_coef_l, "score": score}
                correlation.append(cor_d)
            process += 1
        print ("\033[A                             \033[A")
        print(f"{dependent_data.columns[dep]} is done. Progress: {file_count} out of {dependent_arr }")
        file_count += 1
        print("")
    write_to_file(filename, correlation, i_fname)

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
