import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
import pickle
import csv
from sklearn.preprocessing import MultiLabelBinarizer

with open(r"features_youtube_dict.pkl", "rb") as input_file:
	features = pickle.load(input_file)

with open(r"ratings_dict.pkl", "rb") as input_file:
	ratings = pickle.load(input_file)

all_genres = []
all_cast = []
all_crew = []

for key, value in sorted(features.iteritems()):
	all_genres.append(set(value[2]))
	all_cast.append(set(value[3]))
	all_crew.append(set(value[4]))

mlbGenre = MultiLabelBinarizer()
genre = mlbGenre.fit_transform(all_genres)

mlbCast = MultiLabelBinarizer()
cast = mlbCast.fit_transform(all_cast)

mlbCrew = MultiLabelBinarizer()
crew = mlbCrew.fit_transform(all_crew)

features_writer = csv.writer(open('cleaned_features.csv', 'wb'), delimiter =' ')
index = 0
for key, value in sorted(features.iteritems()):
	all_features = []
	if key in ratings:
		print 'not missing'
		all_features.append(ratings[key])
		all_features.append(int(value[0]))
		all_features.append(int(value[1]))
		all_features.append(int(value[5]))
		all_features += list(genre[index])
		all_features += list(cast[index])
		all_features += list(crew[index])
		features_writer.writerow(all_features)
	else:
		print '-------->missing'
	print index
	index += 1
