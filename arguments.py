from argparse import ArgumentParser
from search import ALGORITHMS

def parse_arguments():
	parser = ArgumentParser(description='N-puzzle solver')
	parser.add_argument(
		'file', type=str, nargs='?',
		default='/dev/fd/0',
		help='initial board')
	parser.add_argument(
		'--search', '-s', type=str,
		default='greedy',
		choices=ALGORITHMS.keys(),
		help='specify a search algorithm')
	parser.add_argument(
		'--heuristic', type=str,
		default='hamming',
		choices=['manhattan', 'euclidian', 'hamming'],
		help='specify an heuristic')
	parser.add_argument(
		'--visualize', '-v',
		action='store_true',
		help='visualize transitions')
	return parser.parse_args()
