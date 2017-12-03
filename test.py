import random

x = []

for i, x_i in enumerate(x):
	print "%d th element: %d" % (i, x_i)



def print_movie_allocation_solution(solution):
    """
    Print the movie resource allocaiton in a nice format based on a solution.

    @para solution: A list of (quarter, course, units). Units can be None, in which
        case it won't get printed.
    """

    if solution == None:
        print "No allocation found that satisfied all the constraints."
    else:
        print "Following is the best allocation:"
        # print "Quarter\t\tUnits\tCourse"
        print solution
        print len(solution)
        actors = solution[0]
        director = solution[1]
        genre = solution[2]
        content_rating = solution[3]
        budget = solution[4]
        for i, actor in enumerate(actors):
                print "actor %d: %s" % (i, actor)
        print "director: %s" % director
        print "genre: %s" % genre
        print "content rating: %s" % content_rating
        print "budget: $%d" % budget
        # for actors, director, genre, content_rating, budget in solution:
        #     for i, actor in enumerate(actors):
        #         print "actor %d: %s" % (i, actor)
        #     print "director: %s" % director
        #     print "genre: %s" % genre
        #     print "content rating: %s" % content_rating
        #     print "budget: %d" % budget   


solution = (["leo", "depp", "aniston"], "nolan", "comedy", "R", 100000)
print_movie_allocation_solution(solution)