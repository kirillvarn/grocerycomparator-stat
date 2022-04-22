import os
import seaborn as sns
import json
import matplotlib.pyplot as plt

from cor import correlate

# csv_files = [file for file in os.listdir("./") if file.endswith(".csv")]

# file = open("correlation_piggy.json")
# data = json.load(file)

# for item in data:
#     sns.regplot(item["predictor"], item["response"])
#     plt.ylabel(item["independent"])
#     plt.xlabel(item["dependent"])
#     plt.show()

correlate("piggy.csv", ["pizza.csv", "wheat.csv"])
