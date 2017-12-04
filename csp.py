
import random

import util
import collections
import copy
import pickle
from sklearn.ensemble import RandomForestRegressor
import numpy as np
from sklearn.externals import joblib
from random import *
import math

# NOTE where profile and CSP need to be made
# movieSolver = submission.BacktrackingSearch()
# a = submission.create_movies_csp()
# movieSolver.solve(a)

forest = joblib.load('model.pkl')
content_ratings_map = pickle.load(open("content_ratings.pickle", "rb"))
actors_map = pickle.load(open("actors.pickle", 'rb'))
directors_map = pickle.load(open("directors.pickle", "rb"))
genres_map = pickle.load(open("genre.pickle", "rb"))
salaries_map = pickle.load(open("salaries.pickle", "rb"))

# '''
# -------------------------------------------------------------------------------------
# originally submission.py
# -------------------------------------------------------------------------------------
# '''
# # Problem 0
# def create_movies_csp():
#     csp = util.CSP()

#     actors = ['John', 'Sam', 'Eddie', 'Nick', 'David']
#     csp.add_variable("a1", actors)
#     csp.add_variable("a2", actors)
#     csp.add_variable("genre", ["Comedy", "Action"])
#     csp.add_variable("director", ['Tim', 'Mary'])

#     csp.add_binary_factor("a1", "a2", lambda x, y : x!=y )

#     return csp



# A backtracking algorithm that solves weighted CSP.
# Usage:
#   search = BacktrackingSearch()
#   search.solve(csp)
class BacktrackingSearch():

    def reset_results(self):
        """
        This function resets the statistics of the different aspects of the
        CSP solver. We will be using the values here for grading, so please
        do not make any modification to these variables.
        """
        # Keep track of the best assignment and weight found.
        self.optimalAssignment = {}
        self.optimalWeight = 0

        # Keep track of the number of optimal assignments and assignments. These
        # two values should be identical when the CSP is unweighted or only has binary
        # weights.
        self.numOptimalAssignments = 0
        self.numAssignments = 0

        # Keep track of the number of times backtrack() gets called.
        self.numOperations = 0

        # Keep track of the number of operations to get to the very first successful
        # assignment (doesn't have to be optimal).
        self.firstAssignmentNumOperations = 0

        # List of all solutions found.
        self.allAssignments = []

        # previously tried to implement a self.optimalAssignments attribute 

    def print_stats(self):
        """
        Prints a message summarizing the outcome of the solver.
        """
        if self.optimalAssignment:
            print "Found %d optimal assignments with weight %f in %d operations" % \
                (self.numOptimalAssignments, self.optimalWeight, self.numOperations)
            print "First assignment took %d operations" % self.firstAssignmentNumOperations
        else:
            print "No solution was found."

    def get_delta_weight(self, assignment, var, val):
        """
        Given a CSP, a partial assignment, and a proposed new value for a variable,
        return the change of weights after assigning the variable with the proposed
        value.

        @param assignment: A dictionary of current assignment. Unassigned variables
            do not have entries, while an assigned variable has the assigned value
            as value in dictionary. e.g. if the domain of the variable A is [5,6],
            and 6 was assigned to it, then assignment[A] == 6.
        @param var: name of an unassigned variable.
        @param val: the proposed value.

        @return w: Change in weights as a result of the proposed assignment. This
            will be used as a multiplier on the current weight.
        """
        assert var not in assignment
        totalCost = 0
        if 'actor1' in assignment:
            totalCost += salaries_map[assignment['actor1']]
        if 'actor2' in assignment:
            totalCost += salaries_map[assignment['actor2']]
        if 'actor3' in assignment:
            totalCost += salaries_map[assignment['actor3']]

        if var == 'actor1':
            totalCost += salaries_map[val]
        if var == 'actor2':
            totalCost += salaries_map[val]
        if var == 'actor3':
            totalCost += salaries_map[val]

        # print "total cost for %s with {%s: %s} is %s" %(assignment, var, val, totalCost)
        if totalCost > self.budget:
            print '--->pruning total cost for %s with {%s: %s} is %s' %(assignment, var, val, totalCost)
            return 0
        w = 1.0
        if self.csp.unaryFactors[var]:
            w *= self.csp.unaryFactors[var][val]
            if w == 0: return w
        for var2, factor in self.csp.binaryFactors[var].iteritems():
            if var2 not in assignment: continue  # Not assigned yet
            w *= factor[val][assignment[var2]]
            if w == 0: return w
        return w

    def solve(self, csp, mcv = False, ac3 = False, budget = 100000000):
        """
        Solves the given weighted CSP using heuristics as specified in the
        parameter. Note that unlike a typical unweighted CSP where the search
        terminates when one solution is found, we want this function to find
        all possible assignments. The results are stored in the variables
        described in reset_result().

        @param csp: A weighted CSP.
        @param mcv: When enabled, Most Constrained Variable heuristics is used.
        @param ac3: When enabled, AC-3 will be used after each assignment of an
            variable is made.
        """
        # CSP to be solved.
        print "It is attempting to solve"
        self.csp = csp

        # Set the search heuristics requested asked.
        self.mcv = mcv
        self.ac3 = ac3

        # Reset solutions from previous search.
        self.reset_results()
        self.budget = budget*0.5

        # The dictionary of domains of every variable in the CSP.
        self.domains = {var: list(self.csp.values[var]) for var in self.csp.variables}

        # Perform backtracking search.
        self.backtrack({}, 0, 1)
        # Print summary of solutions.
        self.print_stats()

    def backtrack(self, assignment, numAssigned, weight):
        self.numOperations += 1
        assert weight > 0
        if numAssigned == self.csp.numVars:
            # A satisfiable solution have been found. Update the statistics.
            self.numAssignments += 1
            newAssignment = {}
            for var in self.csp.variables:
                newAssignment[var] = assignment[var]
            self.allAssignments.append(newAssignment)

            if len(self.optimalAssignment) == 0 or weight >= self.optimalWeight:
                if weight == self.optimalWeight:
                    self.numOptimalAssignments += 1
                else:
                    self.numOptimalAssignments = 1
                self.optimalWeight = weight

                self.optimalAssignment = newAssignment
                if self.firstAssignmentNumOperations == 0:
                    self.firstAssignmentNumOperations = self.numOperations
            return

        # Select the next variable to be assigned.
        var = self.get_unassigned_variable(assignment)  
        # Get an ordering of the values.
        ordered_values = self.domains[var]

        # Continue the backtracking recursion using |var| and |ordered_values|.
        if not self.ac3:
            # When arc consistency check is not enabled.
            for val in ordered_values:
                deltaWeight = self.get_delta_weight(assignment, var, val)
                if deltaWeight > 0:
                    assignment[var] = val
                    self.backtrack(assignment, numAssigned + 1, weight * deltaWeight)
                    del assignment[var]
        else:
            # Arc consistency check is enabled.
            # Problem 1c: skeleton code for AC-3
            # You need to implement arc_consistency_check().
            for val in ordered_values:
                deltaWeight = self.get_delta_weight(assignment, var, val)
                if deltaWeight > 0:
                    assignment[var] = val
                    # create a deep copy of domains as we are going to look
                    # ahead and change domain values
                    localCopy = copy.deepcopy(self.domains)
                    # fix value for the selected variable so that hopefully we
                    # can eliminate values for other variables
                    self.domains[var] = [val]

                    rating = 1
                    # hard coded searching for a tree branch where John and David were actors a1 and a2
                    # weren't able to search for branch where i.e. John was in a Comedy b/c of partial assignment
                    # content_r = content_ratings_map[assignment["contentrating"]] if "contentrating" in assignment and assignment["contentrating"] != 'None' else 0
                    # d_name = directors_map[assignment["director"]] if "director" in assignment and assignment["director"] != None else 0
                    # a3_name = actors_map[assignment["actor3"]] if "actor3" in assignment and assignment["actor3"] != None else 0
                    # a2_name = actors_map[assignment["actor2"]] if "actor2" in assignment  and assignment["actor2"] != None else 0
                    # a1_name = actors_map[assignment["actor1"]] if "actor1" in assignment and assignment["actor1"] != None else 0
                    # g = genres_map[assignment["genre"]] if "genre" in assignment and assignment["genre"] != None else 0


                    content_r = 0
                    if 'content_rating' in assignment: 
                        content_r = content_ratings_map[assignment["content_rating"]]

                    d_name = 0
                    if 'director' in assignment:
                        d_name = directors_map[assignment["director"]]

                    a3_name = 0
                    if 'actor3' in assignment:
                        a3_name = actors_map[assignment["actor3"]]

                    a2_name = 0
                    if 'actor2' in assignment:
                        a2_name = actors_map[assignment["actor2"]]

                    a1_name = 0
                    if 'actor1' in assignment:
                        a1_name = actors_map[assignment["actor1"]]

                    g = 15
                    if 'genre' in assignment:
                        g = genres_map[assignment['genre']]

                    rating = forest.predict([[randint(30000000, 40000000),content_r,d_name,a3_name,a2_name,a1_name,g]])[0]
                    print assignment
                    print rating
                    self.backtrack(assignment, numAssigned + 1, rating * weight * deltaWeight)
                    # restore the previous domains
                    self.domains = localCopy
                    del assignment[var]

    def get_unassigned_variable(self, assignment):
        """
        Given a partial assignment, return a currently unassigned variable.

        @param assignment: A dictionary of current assignment. This is the same as
            what you've seen so far.

        @return var: a currently unassigned variable.
        """

        if not self.mcv:
            # Select a variable without any heuristics.
            for var in self.csp.variables:
                if var not in assignment: return var
        else:
  
            min_valid_domains = float('inf')
            min_var = None

            for var in self.csp.variables:
                if var not in assignment:
                    possible_domains = self.domains[var]
                    valid_domains = 0
                    for possible_value in possible_domains:
                        if self.get_delta_weight(assignment, var, possible_value) > 0:
                            valid_domains += 1
                    if valid_domains < min_valid_domains:
                        min_valid_domains = valid_domains
                        min_var = var
            return min_var
            # END_YOUR_CODE

    def arc_consistency_check(self, var):
        """
        Perform the AC-3 algorithm. The goal is to reduce the size of the
        domain values for the unassigned variables based on arc consistency.

        @param var: The variable whose value has just been set.
        """
        def enforce_consistency(var, neighbor):
            domain_of_var = self.domains[var]
            domain_of_neighbor = self.domains[neighbor]

            to_remove = []
            for i in domain_of_neighbor:
                has_possibility = 0
                for j in domain_of_var:
                    if self.csp.binaryFactors[var][neighbor][j][i] != 0:
                        has_possibility = 1
                if has_possibility == 0:
                    to_remove.append(i)

            if len(to_remove) > 0:
                for removals in to_remove:
                    self.domains[neighbor].remove(removals)
                return True
            else:
                return False

        vars_to_check = set()
        vars_to_check.add(var)

        while len(vars_to_check) != 0:
            var = vars_to_check.pop()
            neighbors = self.csp.get_neighbor_vars(var)
            for neighbor in neighbors:
                domain_changed = enforce_consistency(var, neighbor)
                if domain_changed:
                    vars_to_check.add(neighbor)
        # END_YOUR_CODE

class MovieCSPConstructor():

    def __init__(self, actorBulletin, directorBulletin, profile):
        """
        Saves the necessary data.

        @param bulletin: Stanford Bulletin that provides a list of courses
        @param profile: A student's profile and requests
        """
        self.actorBulletin = actorBulletin
        self.directorBulletin = directorBulletin
        self.profile = profile

    def add_variables(self, csp):
        """
        Adding the variables into the CSP. Each variable, (request, quarter),
        can take on the value of one of the courses requested in request or None.
        For instance, for quarter='Aut2013', and a request object, request, generated
        from 'CS221 or CS246', then (request, quarter) should have the domain values
        ['CS221', 'CS246', None]. Conceptually, if var is assigned 'CS221'
        then it means we are taking 'CS221' in 'Aut2013'. If it's None, then
        we not taking either of them in 'Aut2013'.

        @param csp: The CSP where the additional constraints will be added to.
        """

        genres_map = pickle.load(open("genre.pickle", "rb"))
        content_ratings_map = pickle.load(open("content_ratings.pickle", "rb"))

        csp.add_variable("actor1", self.actorBulletin.actors_map.keys())
        csp.add_variable("actor2", self.actorBulletin.actors_map.keys())
        # csp.add_variable("a3", self.actorBulletin.actors_map.keys())
        #csp.add_variable("genre", genres_map.keys())
        # csp.add_variable("director", self.directorBulletin.directors_map.keys())
        # csp.add_variable("contentrating", content_ratings_map.keys())
        # csp.add_variable("actor1", ['Tyra Banks'])
        #csp.add_variable("actor2", ['John','Adam'])
        csp.add_variable("actor3", self.actorBulletin.actors_map.keys())
        csp.add_variable("genre", ['Comedy','Action','Romance'])
        csp.add_variable("director", self.directorBulletin.directors_map.keys())
        csp.add_variable("content_rating", ['PG','PG-13'])

        #csp.add_variable("budget", ) #NOTE add the budget

    # def add_norepeating_constraints(self, csp):
    #     """
    #     No course can be repeated. Coupling with our problem's constraint that
    #     only one of a group of requested course can be taken, this implies that
    #     every request can only be satisfied in at most one quarter.

    #     @param csp: The CSP where the additional constraints will be added to.
    #     """
    #     for request in self.profile.requests:
    #         for quarter1 in self.profile.quarters:
    #             for quarter2 in self.profile.quarters:
    #                 if quarter1 == quarter2: continue
    #                 csp.add_binary_factor((request, quarter1), (request, quarter2), \
    #                     lambda cid1, cid2: cid1 is None or cid2 is None)

    def get_basic_csp(self):
        """
        Return a CSP that only enforces the basic constraints that a course can
        only be taken when it's offered and that a request can only be satisfied
        in at most one quarter.

        @return csp: A CSP where basic variables and constraints are added.
        """
        csp = util.CSP()
        self.add_variables(csp)
        self.add_constraints(csp)
        self.add_specific_constraints(csp) #NOTE try to separate these out
        return csp

    def add_specific_constraints(self, csp):
        count = 1
        for a in self.profile.actors:
            v = "actor%d" %count
            csp.add_unary_factor(v, lambda x: x == a.name)
            count += 1
        if self.profile.director:
            csp.add_unary_factor("director", lambda x: x==self.profile.director.name)
        if self.profile.content_rating:
            csp.add_unary_factor("content_rating", lambda x: x==self.profile.content_rating)
        if self.profile.genre:
            csp.add_unary_factor("genre", lambda x: x==self.profile.genre)

   

    def add_constraints(self, csp):
        csp.add_binary_factor("actor1", "actor2", lambda x, y : x!=y)
        csp.add_binary_factor("actor3", "actor2", lambda x, y : x!=y)
        csp.add_binary_factor("actor1", "actor3", lambda x, y : x!=y)




    # def add_request_weights(self, csp):
    #     """
    #     Incorporate weights into the CSP. By default, a request has a weight
    #     value of 1 (already configured in Request). You should only use the
    #     weight when one of the requested course is in the solution. A
    #     unsatisfied request should also have a weight value of 1.

    #     @param csp: The CSP where the additional constraints will be added to.
    #     """
    #     count = 0
    #     for a in self.profile.actors:
    #         csp.add_unary_factor((""))


    #     for request in self.profile.requests:
    #         for quarter in self.profile.quarters:
    #             csp.add_unary_factor((request, quarter), \
    #                 lambda cid: request.weight if cid != None else 1.0)



