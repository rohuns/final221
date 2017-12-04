import random
import util
import collections
import copy
import pickle
from sklearn.ensemble import RandomForestRegressor
import numpy as np
from sklearn.externals import joblib
import csp

actors_map = pickle.load(open("actors.pickle", 'rb'))
directors_map = pickle.load(open("directors.pickle", "rb"))
actorBulletin, directorBulletin = util.ActorBulletin(actors_map), util.DirectorBulletin(directors_map) #load pickles
assignments = pickle.load(open("fileMapping.pickle", "rb")) #partial assignments to test

cspConstructor = csp.MovieCSPConstructor(actorBulletin, directorBulletin)
completed = []
for p in assignments:
	profile = util.Profile(actorBulletin, directorBulletin, p)
	copy.deepcopy(profile)
	csp_1 = cspConstructor.get_basic_csp()
	alg = csp.BacktrackingSearch()
	alg.solve(csp_1, mcv=True, ac3=True, budget=profile.budget)
	print alg.optimalAssignment