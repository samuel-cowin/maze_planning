import math

from generation.maze import Maze
from utils.sim_utils import *
from algorithms.search import bfs


test_maze = []

# size of maze
x = int(input('Provide x complexity (1-50): '))
y = int(input('Provide y complexity (1-50): '))

# Maze generation
maze = Maze()
test_maze = maze.make_maze(x, y)

# add host
x_host = 1.5
y_host = 0.5

# Find optimal path with all information
best_path = bfs(test_maze, (math.floor(x_host), math.floor(y_host)), 2)

# show path
execute_path(test_maze, best_path, x_host, y_host)
