import pandas as pd
import numpy as np
import sys
import math

inputfile = "final_data.csv"

data = pd.read_csv(inputfile, error_bad_lines=False, sep=',', low_memory=False, header=0)
data = np.array(data)

rating = {} #maps genre to [rating total, #movies]

genre_index = 12
rating_index = 0
for movie in data:
	genre = movie[genre_index]
	r = movie[rating_index]
	if genre in rating:
		curr_rating = rating[genre]
		update_rating = [curr_rating[0] + r, curr_rating[1] + 1]
		rating[genre] = update_rating
	else:
		rating[genre] = [r, 1.0]


#completed avgs

for g in rating:
	avg = rating[g][0]/rating[g][1]
	rating[g] = avg

print "The avg rating per genre: ", rating
# reclassify based on 
#rating = {'Mystery': 4.03366071428569, 'Romance': 3.8119480128463143, 'Family': 3.5657824933686912, 'Fantasy': 3.878147302312274, 'Horror': 3.293339432753918, 'Crime': 3.6865248759958043, 'Drama': 3.419008680670461, 'Science Fiction': 3.7594397222554545, 'Western': 2.4089320812404473, 'Animation': 3.3492775075773644, 'Music': 2.8686299965834876, 'Adventure': 3.705779859484767, 'Foreign': 4.4417491452222, 'Action': 3.790506756756837, 'TV Movie': 3.4349036899512684, 'Comedy': 3.4432962333670654, 'Documentary': 2.463664853903612, 'War': 3.601810912511748, 'Thriller': 4.01670719718535, 'History': 3.6014006179196487}

# per category and total error for each genre (can be broken down/refined to the per movie basis if we want) Need to figure out how we are dealing with multiple classifications
se = 0
n = 0

for movie in data:
	r = movie[rating_index]
	genre = movie[genre_index]
	#mean squared error
	se += (rating[genre]-r)**2
	n += 1

mse = se/float(n)
rmse = math.sqrt(mse)

print "\n\nRMSE error based on avg for genre: %f " %rmse



