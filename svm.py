import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import linear_model
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.svm import SVR
import math
import matplotlib.pyplot as plt
from sklearn import metrics


f = open("cleaned_features.csv")
data = np.loadtxt(f)

X = data[:, 1:]  # select columns 1 through end
y = data[:, 0]   # select column 0, what we're tryna predict

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)

svr_model = SVR()
svr_model.fit(X_train, y_train)

print svr_model.score(X_test, y_test)

y_predict = svr_model.predict(X_test)
svr_model_mse = mean_squared_error(y_predict, y_test)
print 'MSE squareroot: {}'.format(math.sqrt(svr_model_mse))
