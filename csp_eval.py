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
#assignments = pickle.load(open("fileMapping.pickle", "rb")) #partial assignments to test
assignments = ["sample_profile.txt", "sample_profile_2.txt"]

cspConstructor = csp.MovieCSPConstructor(actorBulletin, directorBulletin)
csp_1 = cspConstructor.get_basic_csp()

completed = []
for p in assignments:
	profile = util.Profile(actorBulletin, directorBulletin, p)
	print "deepcopy -start"
	csp_new = copy.deepcopy(csp_1)
	print "deepcopy - end"
	csp_new.profile = copy.deepcopy(profile)
	cspConstructor.profile = csp_new.profile
	csp_new = cspConstructor.add_specific_constraints(copy.deepcopy(csp_new)) #add the specifics specified by the text file
	alg = csp.BacktrackingSearch()
	alg.solve(csp_new, mcv=True, ac3=True, budget=profile.budget)
	print alg.optimalAssignment