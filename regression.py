import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import linear_model
import numpy as np
from sklearn.metrics import mean_squared_error
import math
import matplotlib.pyplot as plt
from sklearn import metrics


f = open("cleaned_features.csv")
data = np.loadtxt(f)

X = data[:, 1:]  # select columns 1 through end
y = data[:, 0]   # select column 0, what we're tryna predict

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)

regression_model = linear_model.LinearRegression()
regression_model.fit(X_train, y_train)

print('Coefficients: \n', regression_model.coef_)
print regression_model.score(X_test, y_test)

y_predict = regression_model.predict(X_test)
regression_model_mse = mean_squared_error(y_predict, y_test)
print 'MSE squareroot: {}'.format(math.sqrt(regression_model_mse))

plt.plot(y_predict, y_test,'ro')
plt.plot([0,10],[0,10], 'g-')
plt.xlabel('predicted rating')
plt.ylabel('real rating')
plt.show()