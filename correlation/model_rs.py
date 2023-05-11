import pandas as pd
import numpy as np
import glob

import seaborn as sn
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


# sklearn, statsmodel
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

# plt.style.use(['science', 'no-latex', 'grid'])
def evaluate():
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

def get_dataset():
    csv = [pd.read_csv(json) for json in  glob.glob("../datasets/*.csv")]
    index = csv[0].index
    for i in csv:
        i.index=index
    df = pd.concat(csv, axis=1)
    return df

def get_top(n=10):
    jsons = [pd.read_json(json) for json in  glob.glob("*.json")]
    df = pd.concat(jsons)
    df = df.sort_values(by=['score'], ascending=False)
    dataset = get_dataset()
    top_records = df.head(n)
    top_records.to_csv(f"top_{n}.csv")

    # csv_list = []

    # figure(figsize=(6, 5), dpi=300)
    # # print(top_records)
    # for index, item in top_records.iterrows():
    #     m_name = item['model']
    #     y_name = item['dependent']
    #     x_name = item['independent_parameters']

    #     score = item['score']

    #     y_values = dataset[y_name]
    #     x_values = dataset[x_name]

    #     x_train, x_test, y_train, y_test = train_test_split( x_values, y_values, test_size=0.2, random_state=0, shuffle=False)
    #     # print(y_values)
    #     if m_name == 'lregression':
    #         model = LinearRegression()
    #     elif m_name == 'ridge':
    #         model = Ridge(alpha=0.01)
    #     else:
    #         model = Lasso(alpha=0.01)

    #     model.fit(x_train, y_train)
    #     y_pred = model.predict(x_test)

    #     temp = {"dependent": y_name, "independent": x_name, "score": score, "coef": model.coef_, "intercept": model.intercept_}

    #     csv_list.append(temp)

    #     # print(f"Real values: {y_test.tolist()}")
    #     # print(f"Predicted values: {y_pred.tolist()}")

    #     c = [i for i in range (1,len(y_test)+1,1)]
    #     plt.clf()
    #     sn.lineplot(y=y_test, x=c, ci=None)
    #     sn.lineplot(y=y_pred, x=c, ci=None)
    #     # plt.plot(c,y_test,color='r',linestyle='-')
    #     # plt.plot(c,y_pred,color='b',linestyle='-')
    #     plt.legend(labels=["Actual", "Predicted"])
    #     plt.ylabel('Price')
    #     plt.xlabel('Index')
    #     plt.title(y_name)
    #     plt.tight_layout()
    #     # plt.savefig(f"{index}_{score}.png")

    #     # plt.show()
    # csv_df = pd.DataFrame(csv_list)
    # csv_df.to_csv("model_data.csv")
get_top()