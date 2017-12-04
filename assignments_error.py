import util
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
	return error**2


def error(vals):
	e = 0
	skipped = 0
	for pair in vals:
		test = pair[0]
		truth = pair[1]
		if not truth.director:
			skipped += 1
			continue
		e += sample_error(test, truth)
	mse = (float(e)/(len(vals) - skipped))
	print skipped

	return "The MSE with 0-1 loss is %f" %mse
