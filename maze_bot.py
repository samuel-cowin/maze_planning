import math

from generation.maze import Maze
from utils.sim_utils import *
from algorithms.search import bfs
from algorithms.planning import AStar


test_maze = []

# size of maze
x = y = int(input('Provide complexity (1-50): '))
assert 1 <= x <= 40
assert 1 <= y <= 40
print('')

# Maze generation
maze = Maze()
test_maze = maze.make_maze(x, y)
print('Maze:')
for t in test_maze:
    print(t)
print('')

# Starting and ending points
start = (math.floor(maze.x_host), math.floor(maze.y_host))
end = ((len(test_maze)-1,len(test_maze[0])-2))
print('Start: {} and End: {}'.format(start,end[::-1]))
print('')

# Find optimal path with BFS
best_path_bfs = bfs(test_maze, start, end)
execute_path(test_maze, best_path_bfs, maze.x_host, maze.y_host)

# Find optimal path with A*
a = AStar()
a.init_grid(test_maze, start[::-1], end)
best_path_astar = reverse2D(a.solve())
execute_path(test_maze, best_path_astar, maze.x_host, maze.y_host)