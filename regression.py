import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import main
import datetime as dt

# DATA AND VARIABLES
data = main.get_prices(main.conn_naive)
X = data[0]
Y = data[1]['Grilljuust E-Piim 330g']

# CONVERTING DATETIME INTO INTEGER VALUES
X = pd.to_datetime(X)
X = X.map(dt.datetime.toordinal)

# MEANS
x_mean = np.mean(X)
y_mean = np.mean(Y)


numer = 0
denom = 0

for i in range(len(X)):
    numer += (X[i] - x_mean) * (Y[i] - y_mean)
    denom += (X[i] - x_mean) ** 2

# y = mx - c
b1 = numer/denom # m
b0 = y_mean - (b1 * x_mean) # c

min_x = np.min(X) - 100
max_x = np.max(X) + 100
x = np.linspace(min_x, max_x, 1000)
y = b0 + b1 * x

plt.plot(x, y, color="#666666", label="Regression line")
plt.scatter(X, Y, color="#ff1122", label="Scatter plot")
plt.legend()
plt.show()