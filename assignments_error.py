import util
import math
#calculate the mean-squared error
def sample_error(test, truth):
	error = 0
	truth_actors = [a.name for a in truth.actors]

	for a in test.actors:
		if a.name not in truth_actors:
			error += 1
	if test.director.name != truth.director.name:
		error +=1
	if test.genre != truth.genre:
		error += 1
	if truth.content_rating != test.content_rating:
		error += 1

	if error <= 1:
		print test

	print error
	return error**2


def error(vals):
	e = 0
	other = 0
	skipped = 0
	for pair in vals:
		test = pair[0]
		truth = pair[1]
		if not truth.director:
			skipped += 1
			continue
		val = sample_error(test, truth)
		e +=  val
		other += math.sqrt(val)
	mse = (float(e)/(len(vals) - skipped))
	rmse = math.sqrt(mse)

	answer = other/float(81)

	print "here is this fucking shit %s" %answer
	return "The RMSE with 0-1 loss is %f" %rmse

