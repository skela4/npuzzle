from arguments import parse_arguments

import search as sh
import numpy as np
import visuals
import math

def gen_solved_board(board: np.ndarray) -> np.ndarray:
	values = np.roll(np.sort(board, axis=None), -1).tolist()
	solved = np.empty_like(board)
	directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
	x, y = (0, 0)
	offset = 0
	solved[x, y] = values.pop(0)
	for count in range(board.shape[0] + board.shape[1]):
		for _ in range(1, board.shape[0] - offset):
			x = x + directions[count % 4][0]
			y = y + directions[count % 4][1]
			solved[x, y] = values.pop(0)
		if count and not count % 2:
			offset = offset + 1
	return solved

def read_board_from_file(filename: str) -> np.ndarray:
	with open(filename, mode='r') as fd:
		lines = [item.strip() for item in fd.readlines()]
	func = lambda x: x[:x.find('#')] if '#' in x else x
	lines = [item for item in lines if item and not item.startswith('#')]
	lines = [func(item).split() for item in lines]
	if any([x for item in lines for x in item if not x.isdecimal()]):
		raise ValueError('board has non-digits entries')
	return np.array(lines[1:], dtype=np.float32)

def inversions(state: np.ndarray) -> bool:
	inverse = 0
	zeropos = -1
	size = state.size - 1
	i = 0
	while i < size:
		j = i + 1
		while j < state.size:
			if state[i] == 0:
				zeropos = i
			if (state[i] != 0 and state[j] != 0) and (state[i] > state[j]):
				inverse += 1
			j += 1
		i += 1
	if state.size % 2 == 1:
		return inverse % 2 == 0
	if (int((math.sqrt(state.size) - (zeropos // math.sqrt(state.size)))) % 2 == 0):
		return inverse % 2 == 1
	return inverse % 2 == 0

def solvable(initial_state: np.ndarray, final_state: np.ndarray) -> bool:
	return inversions(initial_state.flatten()) == inversions(final_state.flatten())

def main() -> None:
	arguments = parse_arguments()
	try:
		board = read_board_from_file(arguments.file)
		assert board.size > 0, 'board is invalid'
		assert np.min(board) == 0, 'empty tile must have 0 value'
		assert np.unique(board).size == board.size, 'repetitions in board'
	except Exception as ex:
		raise SystemExit(f'error: {str(ex)}')
	solved = np.pad(gen_solved_board(board), 1, constant_values=math.nan)
	board = np.pad(board, 1, constant_values=math.nan)
	if not solvable(board, solved):
		raise SystemExit('error: n-puzzle is not solvable')
	sh.set_search_parameters(arguments.search, arguments.heuristic)
	print(f'Using: {arguments.search} search [{arguments.heuristic}]')
	transitions = sh.search(board, solved)
	print(f'\nTransitions to final state: {len(transitions) - 1}')
	if arguments.visualize is True:
		visuals.visualize_steps(transitions)
	else:
		visuals.print_steps(transitions)

if __name__ == '__main__':
	main()
