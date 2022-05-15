import pandas as pd
import numpy as np
import glob

jsons = glob.glob("*.json")
l = []
for json in jsons:
    df = pd.read_json(json)

    is_simple_reg = True if len(df["independent_parameters"][0]) == 1 else False

    model = df["model"]
    model = list(set(model))[0]

    score = df["score"]
    score = np.mean(score)

    if model == "gaussian":
        model_name =  "Gaussian Process Regression"
    elif model == "ridge":
        model_name = "Ridge Linear"
    elif model == "lasso":
        model_name = "LASSO Linear"
    elif is_simple_reg:
        model_name =  "Simple Regression"
    else:
        model_name =  "Multivariate Regression"

    l.append({"filename": json, "model": model_name, "score":score})

df = pd.DataFrame(l)
df.to_csv("scores.csv")