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

profile = util.Profile(actorBulletin, directorBulletin, 'sample_profile.txt')
cspConstructor = csp.MovieCSPConstructor(actorBulletin, directorBulletin, copy.deepcopy(profile))
csp_1 = cspConstructor.get_basic_csp()
alg = csp.BacktrackingSearch()
alg.solve(csp_1, mcv=True, ac3=True)
print alg.numOptimalAssignments
print alg.optimalAssignment