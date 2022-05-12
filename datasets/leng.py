import pandas as pd
import numpy as np


l = [["pizza.csv", "beef.csv"], ["cake.csv", "wheat.csv", "milk.csv"], ["pizza.csv", "wheat.csv", "pig meat.csv"], ["cake.csv", "wheat.csv", "pear.csv", "apple.csv"], ["cookies.csv", "sugar.csv", "milk.csv"], ["pizza.csv", "banana.csv", "tomatoes.csv", "chicken.csv"]]

total = []
for i in l:
    temp = list()
    for j in i:
        t_df = pd.read_csv(j)
        temp.append(len(t_df.columns))

    total.append(np.prod(temp))


print(sum(total))

