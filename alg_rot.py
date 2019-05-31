"""
I wanted to find a solution with better complexity than usual brute force.
I discovered that it's simple to estimate vertical or horizontal lines only
(I mean, with linear time complexity).
But why?? Because it's possible to represent each line as a single number
X or Y, and it's easy to convert any point to such a line.
And what prevents me from doing the same for other lines? Some slopes?..
So, let's fix it! And I decided to rotate the coordinates
looking for the longest horizontal line in the new coordinate system.
In addition, this solution can easily deal with float numbers.
And the time complexity is O(n*k) where k is a customizable constant.
However, usual execution time is longer for small number of points (<150).
So, let me introduce Aivan's Rotational Algorithm :)
"""

__author__ = 'AivanF.com, 28.05.2019'
__title__ = 'Rotational algorithm'

import math

# *** Constants ***

# Count of rotations
# Rotation amount = 180/ROT_COUNT degrees
# It should be at least 12, use 180*4 for good quality (6% of errors),
# and 180*20 to achieve the best results (0% of errors).
# Larger values increase execution speed.
# Smaller values lead to false negative results.
ROT_COUNT = 180*12

# Precision / bias sensitivity
# Higher values make less bias acceptable.
# It should be any number from 4 and larger.
# Higher MULT_COEF values require higher ROT_COUNT.
# Smaller values lead to false positive results.
# Larger values lead to false negative results.
MULT_COEF = 2 ** 3

angles = list(map(lambda x: x*180.0/ROT_COUNT, range(ROT_COUNT)))
show_details = False

# This line can help to understand or repair the algorithm
# angles = [33.69] ; show_details = True


def mnp_rotated(points, angle):
	"""Returns Maximum Number of Points on the same line with given rotation"""
	# Calculate transformation
	rad = math.radians(angle)
	co = math.cos(rad)
	si = math.sin(rad)
	# Number of points at different Xs
	counts = {}

	if show_details:
		print(angle, co, si)

	for pair in points:
		# Calculate new coordinate
		nx = pair[0]*co - pair[1]*si

		if show_details:
			print(pair, nx)

		# To use a dict properly, the number must be integer
		# Multiplying by a coefficient prevents
		# uniting too distant values after rounding
		nx = int(nx * MULT_COEF)

		# Add the point
		if nx in counts:
			counts[nx] += 1
		else:
			counts[nx] = 1

	# Pick the biggest value
	return max(counts.values())


def mnp(points):
	"""Returns Maximum Number of Points on the same line"""
	res = 0
	best_angle = 0
	for i in angles:
		current = mnp_rotated(points, i)
		
		# Save it the previous value is smaller
		if current > res:
			res = current
			best_angle = i
	
	if show_details:
		print('- best angle:', best_angle)

	return res
