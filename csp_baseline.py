from random import *
import util
import pickle
import assignments_error

actors_map = pickle.load(open("actors.pickle", 'rb'))
directors_map = pickle.load(open("directors.pickle", 'rb'))
genres_map = pickle.load(open("genre.pickle", "rb"))
content_ratings_map = pickle.load(open("content_ratings.pickle", "rb"))

assignments = pickle.load(open("fileMapping.pickle", "rb"))
actorBulletin, directorBulletin = util.ActorBulletin(actors_map), util.DirectorBulletin(directors_map)


def fillProfiles():
	completed = []
	for part in assignments.keys()[0:100]:
		profile = util.Profile(actorBulletin, directorBulletin, "profiles/"+part)
		completed_prof = completeProfile(profile)
		truth = util.Profile(actorBulletin, directorBulletin, "profiles/" + assignments[part])
		completed.append((completed_prof, truth))
	return completed

def completeProfile(profile):
	#fill actors
	if len(profile.actors) < 3:
		while len(profile.actors) < 3:
			actor = util.Actor(choice(actors_map.keys()), 0)
			profile.actors.append(actor) #random right now, dont know a better way without counts, change to random of most commone
	#fill directors
	if profile.director == None:
		profile.director = util.Director(choice(directors_map.keys()), 0)
	#fill genre
	if profile.genre == None:
		profile.genre = choice(genres_map.keys())
	#fill content rating
	if profile.content_rating == None:
		profile.content_rating = choice(content_ratings_map.keys())

	return profile

def baseline():
	done = fillProfiles()
	print(assignments_error.error(done))

baseline()
print len(actors_map.keys())
