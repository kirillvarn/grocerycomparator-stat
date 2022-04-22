from sklearn.linear_model import LinearRegression
import json
import os
import pandas as pd
import numpy as np

# C imports
cimport numpy as np
np.import_array()

cpdef void write_to_file(str filename, data):
    with open(f"correlation_{filename}.json", "w", encoding='UTF8') as f:
        jsob = json.dumps(data, ensure_ascii=False)
        f.write(jsob)

# each dependent is being regressed to whole independent dataset
cpdef void correlate(str first_file, list other_files, bint each=False):
    cdef list correlation = []
    cdef dict cor_d
    cdef str y, x, file
    cdef np.ndarray resp, pred
    cdef float score
    cdef str filename = first_file.split(".")[0]

    if len(other_files) > 0:
        dependent_data = pd.read_csv(first_file, dtype=np.float32)

        for file in other_files:
            independent_data = pd.read_csv(file, dtype=np.float32)

            for y in dependent_data:
                resp = dependent_data[y].values.reshape(-1, 1)
                pred = independent_data.values

                predictor = [{"name": x , "values": independent_data[x].values.tolist()} for x in independent_data]

                reg = LinearRegression()
                reg.fit(resp, pred)

                score = reg.score(resp, pred)
                if score > 0.1 and score <= 0.95:
                    cor_d = { "dependent": y, "independent_file": file, "score": score, "response": resp.flatten().tolist(), "predictor": predictor}
                    correlation.append(cor_d)
        write_to_file(filename, correlation)

    else:
        data = pd.read_csv(first_file, dtype=np.float32)

        for y in data:
            for x in data:
                if x != y:
                    resp = data[y].values.reshape(-1, 1)
                    pred = data[x].values.reshape(-1, 1)

                    reg = LinearRegression()
                    reg.fit(resp, pred)

                    score = reg.score(resp, pred)
                    if score > 0.1 and score <= 0.95:
                        cor_d = { "dependent": y, "independent": x, "score": score, "response": resp.flatten().tolist(), "predictor": pred.tolist()}
                        correlation.append(cor_d)
            data.drop(columns=[y])

        write_to_file(filename, correlation)