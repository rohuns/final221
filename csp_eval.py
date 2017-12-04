import random
import util
import collections
import copy
import pickle
from sklearn.ensemble import RandomForestRegressor
import numpy as np
from sklearn.externals import joblib
import csp
import assignments_error


class FakeProfile():
  	def __init__(self, actors, director, genre, content_rating):
	    self.actors = actors
	    self.director = director
	    self.genre = genre
	    self.content_rating = content_rating

def makeProfile(m):
	actors = [m["actor1"], m["actor2"], m["actor3"]]
	director = m["director"]
	genre = m["genre"]
	content_rating = m["content_rating"]
	return FakeProfile(actors, director, genre, content_rating)

actors_map = pickle.load(open("actors.pickle", 'rb'))
directors_map = pickle.load(open("directors.pickle", "rb"))
actorBulletin, directorBulletin = util.ActorBulletin(actors_map), util.DirectorBulletin(directors_map) #load pickles
assignments = pickle.load(open("fileMapping.pickle", "rb")) #partial assignments to test
#assignments = ["sample_profile.txt", "sample_profile_2.txt"]

completed = []
print assignments.keys()[0]
for p in [assignments.keys()[0]]:
	profile = util.Profile(actorBulletin, directorBulletin, "profiles/" + p)
	cspConstructor = csp.MovieCSPConstructor(actorBulletin, directorBulletin, profile)
	csp_1 = cspConstructor.get_basic_csp()
	alg = csp.BacktrackingSearch()
	if profile.budget == None:
		alg.solve(csp_1, mcv=True, ac3=True)
	else:
		alg.solve(csp_1, mcv=True, ac3=True, budget=profile.budget)
	completedProfile = makeProfile(alg.optimalAssignment)
	truth = util.Profile(actorBulletin, directorBulletin, "profiles/" + assignments[part])
	completed.append(completedProfile, truth)
	print alg.optimalAssignment
print(assignments_error.error(done))
