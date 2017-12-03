import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, median_absolute_error
import math
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor
from sklearn.externals import joblib
from yellowbrick.regressor import ResidualsPlot
from yellowbrick.regressor import PredictionError

movies = pd.read_csv('final_data.csv')

X = movies[['budget', 'content_rating', 'director_name', 'actor_3_name', 'actor_2_name', 'actor_1_name', 'genres']]
y = movies['imdb_score']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05, random_state=42)

regression_model = linear_model.LinearRegression()
regression_model.fit(X_train, y_train)

y_predict_lr = regression_model.predict(X_test)
print 'Linear Regression Mean squared error: {}'.format(math.sqrt(mean_squared_error(y_predict_lr, y_test)))
print 'Linear Regression Median absolute error: {}'.format(median_absolute_error(y_predict_lr, y_test))

model = ResidualsPlot(linear_model.LinearRegression())
model.fit(X_train, y_train)
model.score(X_test, y_test)
model.poof()

plt.plot(y_predict_lr, y_test,'ro')
plt.plot([y_predict_lr.min(),y_predict_lr.max()],[y_predict_lr.min(),y_predict_lr.max()], 'g-')
plt.xlabel('Linear Regression Predicted Rating')
plt.ylabel('Real Rating')
plt.show()

lasso = linear_model.Lasso()
lasso.fit(X_train, y_train)

y_predict_lasso = lasso.predict(X_test)
print 'Lasso Mean squared error: {}'.format(math.sqrt(mean_squared_error(y_predict_lasso, y_test)))
print 'Lasso Median absolute error: {}'.format(median_absolute_error(y_predict_lasso, y_test))

model = ResidualsPlot(linear_model.Lasso())
model.fit(X_train, y_train)
model.score(X_test, y_test)
model.poof()

plt.plot(y_predict_lasso, y_test,'ro')
plt.plot([y_predict_lasso.min(),y_predict_lasso.max()],[y_predict_lasso.min(),y_predict_lasso.max()], 'g-')
plt.xlabel('Lasso Predicted Rating')
plt.ylabel('Real Rating')
plt.show()

ridge = linear_model.Ridge()
ridge.fit(X_train, y_train)

y_predict_ridge = ridge.predict(X_test)
print 'Ridge Mean squared error: {}'.format(math.sqrt(mean_squared_error(y_predict_ridge, y_test)))
print 'Ridge Median absolute error: {}'.format(median_absolute_error(y_predict_ridge, y_test))

model = ResidualsPlot(linear_model.Ridge())
model.fit(X_train, y_train)
model.score(X_test, y_test)
model.poof()

plt.plot(y_predict_ridge, y_test,'ro')
plt.plot([y_predict_ridge.min(),y_predict_ridge.max()],[y_predict_ridge.min(),y_predict_ridge.max()], 'g-')
plt.xlabel('Ridge Predicted Rating')
plt.ylabel('Real Rating')
plt.show()

forest = RandomForestRegressor()
forest.fit(X_train, y_train)

y_predict_forest = forest.predict(X_test)
print 'Forest Mean squared error: {}'.format(math.sqrt(mean_squared_error(y_predict_forest, y_test)))
print 'Forest Median absolute error: {}'.format(median_absolute_error(y_predict_forest, y_test))

joblib.dump(forest, 'model.pkl') 

model = ResidualsPlot(RandomForestRegressor())
model.fit(X_train, y_train)
model.score(X_test, y_test)
model.poof()

plt.plot(y_predict_forest, y_test,'ro')
plt.plot([y_predict_forest.min(),y_predict_forest.max()],[y_predict_forest.min(),y_predict_forest.max()], 'g-')
plt.xlabel('Forest Predicted Rating')
plt.ylabel('Real Rating')
plt.show()



