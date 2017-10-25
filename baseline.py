import pandas as pd
import numpy as np
import sys
import math

inputfile = "AllMoviesDetailsCleaned.csv"

data = pd.read_csv(inputfile, error_bad_lines=False, sep=';', low_memory=False)

data = np.array(data)

genre = 2
score = 17

rating = {} #maps genre to [rating total, #movies]

for movie in data:
	genres = movie[genre]
	if type(genres) == float:
		continue
	genres = genres.split('|')
	s = float(movie[score])
	if s == 0:
		continue
	for g in genres:
		if g in rating:
			curr_rating = rating[g]
			update_rating = [curr_rating[0] + s, curr_rating[1] + 1]
			rating[g] = update_rating
		else:
			rating[g] = [s, 1.0]


#completed avgs

for g in rating:
	avg = rating[g][0]/rating[g][1]
	rating[g] = avg

print "The avg rating per genre: ", rating
# reclassify based on 
#rating = {'Mystery': 4.03366071428569, 'Romance': 3.8119480128463143, 'Family': 3.5657824933686912, 'Fantasy': 3.878147302312274, 'Horror': 3.293339432753918, 'Crime': 3.6865248759958043, 'Drama': 3.419008680670461, 'Science Fiction': 3.7594397222554545, 'Western': 2.4089320812404473, 'Animation': 3.3492775075773644, 'Music': 2.8686299965834876, 'Adventure': 3.705779859484767, 'Foreign': 4.4417491452222, 'Action': 3.790506756756837, 'TV Movie': 3.4349036899512684, 'Comedy': 3.4432962333670654, 'Documentary': 2.463664853903612, 'War': 3.601810912511748, 'Thriller': 4.01670719718535, 'History': 3.6014006179196487}

# per category and total error for each genre (can be broken down/refined to the per movie basis if we want) Need to figure out how we are dealing with multiple classifications
genre_error = {'Total': (0.0, 0.0)}

for movie in data:
	s = float(movie[score])
	if s == 0:  #may need to clean out the movies with no rating
		continue
	genres = movie[genre]
	if type(genres) == float: # need to clean the data at some point for this data
		continue
	genres = genres.split('|')
	for g in genres:
		#percent error((observed-expected)/expected)
		error = abs(((rating[g]-s)/s))
		#update the error
		if g in genre_error:
			curr_error = genre_error[g]
			update_error = [curr_error[0] + error, curr_error[1] + 1]
			genre_error[g] = update_error
		else:
			genre_error[g] = [error, 1]
		# update the total (do we want to double count the movies that were double listed, this does right now but can be written to just do an avg per movie)
		total_curr = genre_error["Total"]
		update_total = [total_curr[0] + error, total_curr[1] + 1]
		genre_error["Total"] = update_total

avg_errors = [100*(genre_error[x][0]/genre_error[x][1]) for x in genre_error]

print "Average % error for each genre: ", avg_errors



