"""
Implementation of brute-force approach.
Two-tier iteration over all the points and parallel lines with lines saving.
Lines are stored as slope and a point to distinguish parallel lines.
I made some normalisation of the slopes using GCD, ABS, and inverting.
"""

__author__ = 'AivanF.com, 28.05.2019'
__title__ = 'Brute-force algorithm'

show_details = False


def gcd(a, b):
	"""Returns greatest common divider."""
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
	"""Returns "normalised" slope between given points."""
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
		# Slopes that are already assigned to current point
		# must be skipped. See Playfair's axiom.
		processed_slopes = []
		for j in range(len(points)):
			if j >= i:
				break

			# Deterimine slope between 2 current point
			current_slope = get_delta(points[i], points[j])
			# Check if the slope was already processed at this point
			if current_slope in processed_slopes:
				continue
			else:
				processed_slopes.append(current_slope)

			if show_details:
				print(points[i], points[j], current_slope)

			if current_slope in slopes:
				# Try to find the same line
				matched = False
				other_points = slopes[current_slope]
				for other_point in other_points:
					# -- This loop makes the complexity worse than O(n^2)! --
					# Check whether the line is the same or parallel
					other_slope = get_delta(points[i], other_point)
					if other_slope == current_slope:
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
				slopes[current_slope] = {points[i]: 2}

	if show_details:
		print(slopes)

	# Search for the longest line
	res = 0
	found = None
	for slope in slopes:
		for point in slopes[slope]:
			if slopes[slope][point] > res:
				res = slopes[slope][point]
				found = (point, slope,)
	if show_details:
		print('The result:', found)
	return res
