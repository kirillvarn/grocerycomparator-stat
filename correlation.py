import os
import seaborn as sns
import json
import matplotlib.pyplot as plt

from cor import correlate, correlate_by_one

# csv_files = [file for file in os.listdir("./") if file.endswith(".csv")]

# file = open("correlation_piggy.json")
# data = json.load(file)

# for item in data:
#     sns.regplot(item["predictor"], item["response"])
#     plt.ylabel(item["independent"])
#     plt.xlabel(item["dependent"])
#     plt.show()

# pizza dependent
# correlate("pizza.csv", ["pig meat.csv", "wheat.csv"])

# cake dependent
# correlate("cake.csv", ["wheat.csv", "milk.csv", "eggs.csv"])


# correlate_by_one("cake.csv", ["wheat.csv", "milk.csv"])
# correlate_by_one("pizza.csv", ["wheat.csv", "pig meat.csv"])
correlate_by_one("rimi milk.csv", ["other shop milk.csv"])
