from typing import Callable

import numpy as np
import math
import sys

man = lambda a, b: math.fabs(a[0] - b[0]) + math.fabs(a[1] - b[1])
euc = lambda a, b: math.sqrt(math.pow((a[0] - b[0]), 2) + math.pow((a[1] - b[1]), 2))

def manhattan(state: np.ndarray, final: np.ndarray) -> float:
	return sum([man(pos, np.where(final == value)) for pos, value in np.ndenumerate(state[1:-1, 1:-1])])

def euclidian(state: np.ndarray, final: np.ndarray) -> float:
	return sum([euc(pos, np.where(final == value)) for pos, value in np.ndenumerate(state[1:-1, 1:-1])])

def hamming(state: np.ndarray, final: np.ndarray) -> float:
	return np.sum(state[1:-1, 1:-1] != final[1:-1, 1:-1])

def get(identifier: str) -> Callable:
	return sys.modules[__name__].__dict__.get(identifier)
