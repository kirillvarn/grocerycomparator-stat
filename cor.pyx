from sklearn.linear_model import LinearRegression
import json
import os
import pandas as pd
import numpy as np
cimport numpy as np
np.import_array()

# sklearn

# CONSTANTS
cdef bint wheat_kilos = 1
cdef dict query_to_parse = {
    "milk": "SELECT * FROM \"%s\" WHERE price != 0 AND discount = false AND (name ILIKE '%%1l%%' OR name ILIKE '%%1 l%%') AND (name ILIKE '%%piim %%' OR name ILIKE '%%piim,%%') AND name NOT ILIKE '%%juust%%' AND name NOT ILIKE '%%kohupiim%%' AND name NOT ILIKE '%%laktoos%%' AND name NOT ILIKE '%%täis%%' AND name NOT ILIKE '%%kookos%%' AND name NOT ILIKE '%%latte%%' AND (name ILIKE '%%2,5%%' OR name ILIKE '%%2.5%%')",
    "eggs": f"SELECT * FROM \"%s\" WHERE price != 0 AND discount = false AND name ILIKE '%%munad %%' OR name ILIKE '%%munad, %%' OR name ILIKE '%%muna,%%'",
    "wheat": f"SELECT * FROM \"%s\" WHERE price != 0 AND discount = false AND (name ILIKE '%%{wheat_kilos}kg%%' OR name ILIKE '%%{wheat_kilos} kg%%') AND (name ILIKE '%%nisujahu %%' OR name ILIKE '%%nisujahu,%%')",
    "tomatoes": "SELECT * FROM \"%s\" WHERE price != 0 AND discount = false AND (name ILIKE '%%tomat %%' OR name ILIKE '%%tomat, %%') AND name NOT ILIKE '%%pasta%%' AND name NOT ILIKE '%%0g%%' AND name NOT ILIKE '%%0 g%%' AND name NOT ILIKE '%%harilik%%' AND name NOT ILIKE '%%krõpsud%%' AND name NOT ILIKE '%%marinaad%%' AND name NOT ILIKE '%%eine%%'",
    "cucumber": "SELECT * FROM \"%s\" WHERE price != 0 AND discount = false AND name ILIKE '%%kg%%' AND (name ILIKE '%%kurk %%' OR name ILIKE '%%kurk,%%')",
    "banana": "SELECT * FROM \"%s\" WHERE price != 0 AND discount = false AND (name ILIKE '%%kg%%' OR name ILIKE '%%chiq%%') AND (name ILIKE '%%banaan %%' OR name ILIKE '%%banaan,%%')",
    "apple": "SELECT * FROM \"%s\" WHERE price != 0 AND discount = false AND name ILIKE '%%kg%%' AND (name ILIKE '%%õun %%' OR name ILIKE '%%õun,%%')",
    "pear": "SELECT * FROM \"%s\" WHERE price != 0 AND discount = false AND name ILIKE '%%kg%%' AND (name ILIKE '%%pirn %%' OR name ILIKE '%%pirn,%%')",
    "all": 'SELECT * FROM "%s" WHERE price != 0 AND discount = false',
}

try:
    os.remove("correlation_lower_half.json")
except FileNotFoundError:
    pass

try:
    os.remove("correlation_upper_half.json")
except FileNotFoundError:
    pass


cpdef list regression(bint onefile=True, onefilename=""):
    cdef list correlation = []

    if onefile == False:
        files = [f"{i}.csv" for i in query_to_parse]
        files.remove("all.csv")

        for file in files:
            correlation += linear(file)
    else:
        correlation = linear(onefilename)
    return correlation

cpdef void write_to_file(filename, dict data):
    filename = filename.split(".")[0]
    with open(f"correlation_{filename}.json", "w", encoding='UTF8') as f:
        jsob = json.dumps(data, ensure_ascii=False)
        f.write(jsob)

cpdef list linear(filename):
    data = pd.read_csv(filename, dtype=np.float16)

    cdef list correlation = []

    keys = data.keys()

    cdef unsigned short key_range = keys.size

    # VARIABLE DECLARATIONS
    cdef int key, j
    cdef np.float32_t r2
    cdef np.ndarray y, x

    for key in range(key_range):
        y = np.array(data.iloc[:, key])
        for j in range(key_range):
            if j != key:
                x = np.array(data.iloc[:, j])

                reg = LinearRegression()
                reg.fit(x.reshape(-1, 1), y)

                r2 = reg.score(x.reshape(-1, 1), y)

                if r2 > 0 and r2 <= 0.95:
                    correlation.append(
                        {"dependent": data.columns[key], "independent": data.columns[j], "score": r2})

    return correlation


def run(filename):
    cdef dict cor

    for cor in regression(onefile=True, onefilename=filename):
        write_to_file(filename, cor)
