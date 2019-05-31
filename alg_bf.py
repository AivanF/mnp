"""
Implementation of ordinary approach.
Two-tier iteration over all the points with lines saving.
Lines are stored as slope vectors and a point to distinguish parallel lines.
I made some normalisation of the vectors using GCD, ABS, and inverting.
"""

__author__ = 'AivanF.com, 28.05.2019'
__title__ = 'Brute-force algorithm'

show_details = False


def gcd(a, b):
	# Returns greatest common divider
	a,b = abs(a),abs(b)
	if a == 0 or b == 0:
		return max(a, b)
	if a == b:
		return a
	if b > a:
		a, b = b, a

	def inner(a, b):
		if b == 0:
			return a
		else:
			return gcd(b, a%b)
	return inner(a, b)


def get_delta(a, b):
	# Returns "normalised" vector between given points
	dx = a[0] - b[0]
	dy = a[1] - b[1]
	div = gcd(dx, dy)
	if div > 0:
		# Minify values using integer division
		dx, dy = dx // div, dy // div

	# Make the direction consistent
	if dx < 0:
		dx *= -1
		dy *= -1
	elif dx == 0:
		dy = abs(dy)

	return dx, dy


def mnp(points):
	"""Returns Maximum Number of Points on the same line"""

	# It's structure: {slope<(int,int)>: {point<(int,int)>: count<int>}}
	slopes = {}

	for i in range(len(points)):
		# Vectors that are already assigned to current point
		# must be skipped
		done_vectors = []
		for j in range(len(points)):
			if j >= i:
				break

			# Deterimine vector between 2 current point
			current_vector = get_delta(points[i], points[j])
			# Check if the vector was already processed at this point
			if current_vector in done_vectors:
				continue
			else:
				done_vectors.append(current_vector)

			if show_details:
				print(points[i], points[j], current_vector)

			if current_vector in slopes:
				# Try to find the same line
				matched = False
				other_points = slopes[current_vector]
				for other_point in other_points:
					# Check whether the line is the same or parallel
					other_vector = get_delta(points[i], other_point)
					if other_vector == current_vector:
						other_points[other_point] += 1
						matched = True
						if show_details:
							print('matched')
						break
				if not matched:
					if show_details:
						print('new parallel')
					other_points[points[i]] = 2
			else:
				if show_details:
					print('new slope')
				slopes[current_vector] = {points[i]: 2}

	if show_details:
		print(slopes)

	# Search for the longest line
	res = 0
	for slope in slopes:
		for point in slopes[slope]:
			res = max(res, slopes[slope][point])
	return res
