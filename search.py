from collections import namedtuple
from itertools import count
from typing import Callable, Iterable

import numpy as np
import heuristics
import heapq
import math
import time

Coords = namedtuple('coords', ['x', 'y'])
Node = namedtuple('node', ['cost', 'id', 'state'])

class __SearchParameters(object):
	search: Callable
	heuristic: Callable

CONFIG = __SearchParameters()
ALGORITHMS = dict({
	'ast': lambda h, g: h + g,
	'greedy': lambda h, g: h,
	'uniform': lambda h, g: g + 1})

def set_search_parameters(search: Callable = None, heuristic: Callable = None) -> None:
	if search is not None:
		CONFIG.search = ALGORITHMS.get(search)
	if heuristic is not None:
		CONFIG.heuristic = heuristics.get(heuristic)

def neighbors(state: np.ndarray) -> Iterable[Coords]:
	x, y = np.where(state == 0)
	for offset in ((1, 0), (-1, 0), (0, 1), (0, -1)):
		index = (x.item() + offset[0], y.item() + offset[1])
		if not math.isnan(state[index]):
			yield Coords(*index)

def permute(board: np.ndarray, index: Coords) -> np.ndarray:
	state = np.copy(board)
	state[np.where(state == 0)], state[index] = state[index], 0
	return state

def backtrack_to_initial_state(nodes, initial_state, final_state):
	item = final_state
	states = [item]
	while item.tobytes() != initial_state.tobytes():
		item = np.frombuffer(nodes[item.tobytes()], dtype=item.dtype).reshape(item.shape)
		states.append(item)
	return states

def search(initial_state: np.ndarray, final_state: np.ndarray) -> Iterable:
	ids, prev, explored = count(), dict(), set()
	start = time.time()
	nodes = [Node(0, next(ids), initial_state)]
	heapq.heapify(nodes)
	while len(nodes) > 0:
		print(f'\r{time.time() - start:.3f}s -- States opened:{len(nodes):<7d} closed:{len(explored):<7d}', end='')
		node = heapq.heappop(nodes)
		if np.array_equal(node.state, final_state, equal_nan=True):
			return backtrack_to_initial_state(prev, initial_state, final_state)
		explored.add(node.state.tobytes())
		for item in neighbors(node.state):
			state = permute(node.state, item)
			if state.tobytes() not in explored:
				cost = CONFIG.search(CONFIG.heuristic(state, final_state), node.cost)
				heapq.heappush(nodes, Node(cost, next(ids), state))
				prev[state.tobytes()] = node.state.tobytes()
	return [initial_state]
