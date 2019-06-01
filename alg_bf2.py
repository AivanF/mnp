"""
Better implementation of the brute-force approach.
In contrast to the first one, it has time complexity O(n^2)
because of getting rid of the loop over parallel lines.
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


def get_delta(a, b):
	"""Returns "normalised" vector between given points."""
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


def describe_parallel(point, vector):
	"""Returns a value which is the same for parallel lines."""
	px = point[0]
	py = point[1]
	dx = vector[0]
	dy = vector[1]

	def shift(count):
		nonlocal px, py
		px += dx * count
		py += dy * count

	if px != 0 and dx > 0:
		shift(-int(px / dx))
	if px < 0:
		shift(1)
	if dx == 0:
		if py != 0 and dy > 0:
			shift(-int(py / dy))
		if py < 0:
			shift(1)
	if show_details:
		print(point, vector, (px,py))
	return (px, py)


def mnp(points):
	"""Returns Maximum Number of Points on the same line"""

	# It's structure: {slope<(int,int)>: {point<(int,int)>: count<int>}}
	# Must be: {slope<(int,int)>: {parallel_shift(int): count<int>}}
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

			# Transform parallel lines to some static value
			current_shift = describe_parallel(points[i], current_vector)

			if show_details:
				print(points[i], points[j], current_vector, current_shift)

			if current_vector in slopes:
				# Try to find the same line
				matched = False

				all_shifts = slopes[current_vector]
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
				slopes[current_vector] = {current_shift: 2}

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


if __name__ == '__main__':
	data = [
		[(1,0), (1,1)],
		[(-1,-2), (1,1)],
		[(1,-1), (1,1)],

		[(1,10), (0,1)],
		[(1,15), (0,1)],
		[(0,15), (0,1)],
	]
	for sample in data:
		value = describe_parallel(sample[0], sample[1])
		print(sample[0], sample[1], value)
