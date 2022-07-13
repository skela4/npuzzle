from matplotlib import animation as animation
from matplotlib import pyplot as plt
from matplotlib import rcParams
from typing import Iterable

import numpy as np

rcParams['toolbar'] = 'None'

def create_frames(ax, transitions: Iterable) -> Iterable:
	visuals = list()
	for item in reversed(transitions):
		item = item[1:-1, 1:-1].astype(int)
		frame = list([ax.imshow(item, animated=True)])
		for (x, y), label in np.ndenumerate(item):
			frame.append(ax.text(y, x, label, ha='center', va='center', fontsize='x-large', animated=True))
		visuals.append(frame)
	return visuals

def visualize_steps(transitions: Iterable) -> None:
	fig, ax = plt.subplots(figsize=(4, 4))
	fig.canvas.manager.set_window_title('N-puzzle')
	ax.axis('off')
	frames = create_frames(ax, transitions)
	anim = animation.ArtistAnimation(fig, frames, interval=min(120, 8000 / len(frames)), blit=True, repeat=False)
	plt.show()

def print_steps(transitions: Iterable) -> None:
	for item in reversed(transitions):
		print(item[1:-1, 1:-1].astype(int), end='\n\n')
