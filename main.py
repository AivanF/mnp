"""
My solutions of the following task.
Given n points on a 2D plane, find the maximum number of points
that lie on the same straight line.

Several algorithms were implemented:
- Aivan's rotational one with O(n) time complexity
- simple brute-force with O(n^3) complexity
- enhanced brute-force with O(n^2) complexity
"""

__author__ = 'AivanF.com, 28.05.2019'

import time
import random
import alg_rot
import alg_bf
import alg_bf2

samples = [
	([(1,1), (2,2), (3,3)], 3),
	# o--
	# -o-
	# --o

	([(1,1), (3,2), (5,3), (4,1), (2,3), (1,4)], 4),
	# o--o-
	# --o--
	# -o--o
	# o----

	([(1,1), (2,1), (3,2), (4,2), (1,3), (2,3)], 2),
	# oo--
	# --oo
	# oo--

	([(3,1), (1,2), (3,2), (2,3), (4,3), (1,4), (3,4), (5,4), (3,5)], 4),
	# --o--
	# o-o--
	# -o-o-
	# o-o-o
	# --o--

	([(8, 6), (3, 1), (4, 7), (3, 9), (7, 3), (1, 1), (4, 9), (0, 4), (2, 3)], 3),
	# 1,1 / 2,3 / 4,7

	([(7, 2), (1, 0), (17, 1), (3, 10), (10, 15), (5, 13), (18, 1), (5, 5), (8, 8), (17, 6), (10, 16), (13, 14), (7, 19), (15, 11), (11, 16), (18, 2), (14, 10), (20, 5), (18, 5), (11, 4), (19, 0), (5, 12), (10, 11), (1, 5), (16, 13), (7, 3), (3, 7), (15, 2), (16, 3), (13, 17), (20, 12), (19, 6), (12, 7), (3, 2), (9, 20), (9, 1), (9, 15), (1, 16), (10, 14)], 5),
	# This one is challenging for my rotational algorithm
]



def check_prepared(algorithm):
	"""Checks results of a given algorithm on prepared sample data."""
	print('Using ' + algorithm.__title__)
	done = 0
	for pair in samples:
		res = algorithm.mnp(pair[0])
		if res == pair[1]:
			done += 1
		else:
			print('Failed on {}\nGot: {}\nMust be: {}'.format(pair[0], res, pair[1]))
	print('Success: {} of {}'.format(done, len(samples)))


def compare_random(a1, a2, observations, point_number, square_size):
	"""Compares results of 2 given algorithms on random data."""

	def random_points():
		points = []
		for i in range(point_number):
			x = random.randint(0, square_size)
			y = random.randint(0, square_size)
			point = (x,y)
			# Prevent doubles
			if point not in points: 
				points.append(point)
		return points
	
	errors = 0
	t1 = 0
	t2 = 0
	for _ in range(observations):
		started = 0
		def tick():
			nonlocal started
			started = time.time()
		def tock():
			return time.time() - started
		
		points = random_points()
		
		tick()
		r1 = a1.mnp(points)
		t1 += tock()

		tick()
		r2 = a2.mnp(points)
		t2 += tock()

		if r1 != r2:
			# print('Mismatches:\n{}\nResults: {} vs {}'.format(points, r1, r2))
			errors += 1
	
	t1 /= observations
	t2 /= observations

	print('Random samples errors: {} of {} = {:.1f}%'.format(errors, observations, 100*errors/observations))
	print('Time: {:.4f} vs {:.4f}'.format(t1, t2))


if __name__ == '__main__':
	# check_prepared(alg_bf)
	check_prepared(alg_bf2)
	check_prepared(alg_rot)

	# alg_bf and alg_bf2 are always correct,
	# so this function call shows errors of alg_rot
	compare_random(alg_bf2, alg_rot, 100, 50, 15)
