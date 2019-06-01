"""
Better implementation of the brute-force approach.
In contrast to the first one, it has time complexity O(n^2)
because of getting rid of the loop over parallel lines.

Two-tier iteration over all the points with lines saving.
Lines are stored as a slope and a shift to distinguish parallel lines.
"""

__author__ = 'AivanF.com, 31.05.2019'
__title__ = 'Brute-force algorithm 2'

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


def get_slope(a, b):
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


def get_shift(point, slope):
	"""Returns a value which is the same for parallel lines."""
	px = point[0]
	py = point[1]
	dx = slope[0]
	dy = slope[1]

	def move(count):
		nonlocal px, py
		px += dx * count
		py += dy * count

	if px != 0 and dx > 0:
		move(-int(px / dx))
	if px < 0:
		move(1)
	if dx == 0:
		if py != 0 and dy > 0:
			move(-int(py / dy))
		if py < 0:
			move(1)
	if show_details:
		print(point, slope, (px,py))
	return (px, py)


def mnp(points):
	"""Returns Maximum Number of Points on the same line"""

	# It's structure: {slope<(int,int)>: {shift<int,int>: count<int>}}
	slopes = {}

	for i in range(len(points)):
		# Slopes that are already assigned to current point
		# must be skipped. See Playfair's axiom.
		processed_slopes = set()
		for j in range(len(points)):
			if j >= i:
				break

			# Deterimine slope between 2 current point
			current_slope = get_slope(points[i], points[j])
			# Check if the slope was already processed at this point
			if current_slope in processed_slopes:
				continue
			else:
				processed_slopes.add(current_slope)

			# Transform parallel lines to some comparable value
			current_shift = get_shift(points[i], current_slope)

			if show_details:
				print(points[i], points[j], current_slope, current_shift)

			if current_slope in slopes:
				# Try to find the same line
				all_shifts = slopes[current_slope]
				if current_shift in all_shifts:
					if show_details:
						print('matched')
					all_shifts[current_shift] += 1
				else:
					if show_details:
						print('new parallel')
					all_shifts[current_shift] = 2

			else:
				if show_details:
					print('new slope')
				slopes[current_slope] = {current_shift: 2}

	if show_details:
		print(slopes)

	# Search for the "longest" line
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
