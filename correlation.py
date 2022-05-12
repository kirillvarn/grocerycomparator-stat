import os
import seaborn as sns
import json
import matplotlib.pyplot as plt

from cormodule.cor import correlate_by_one

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


# correlate_by_one("datasets/rimi milk.csv", ["datasets/apple.csv", "datasets/eggs.csv", "datasets/beef.csv"])

# correlate_by_one("datasets/pizza.csv", ["datasets/beef.csv"])

# correlate_by_one("datasets/cake.csv", ["datasets/wheat.csv", "datasets/milk.csv"])
# correlate_by_one("datasets/pizza.csv", ["datasets/wheat.csv", "datasets/pig meat.csv"])

# correlate_by_one("datasets/cake.csv", ["datasets/wheat.csv", "datasets/pear.csv", "datasets/apple.csv"])
#correlate_by_one("datasets/cookies.csv", ["datasets/sugar.csv", "datasets/milk.csv"])
#correlate_by_one("datasets/pizza.csv", ["datasets/banana.csv", "datasets/tomatoes.csv", "datasets/chicken.csv"])


# correlate_by_one("datasets/rimi milk.csv", ["datasets/other shop milk.csv"], allow_same=True)