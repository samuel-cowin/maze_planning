from generation.maze import Maze, Status
from utils.sim_utils import *
from algorithms.search import bfs
from algorithms.planning import AStar
from algorithms.reinforcement import QTableModel


# Maze generation
difficulty = int(input('Maze difficulty (1-30)? '))
maze = Maze(dim=difficulty)

# Starting and ending points
print('Start: {} and End: {}'.format(maze.start_cell,maze.end_cell))
print('')

# Find optimal path with BFS
best_path_bfs = bfs(maze.maze, maze.start_cell, maze.end_cell[::-1])
execute_path(maze.maze, best_path_bfs, maze.x_host, maze.y_host)

# Find optimal path with A*
a = AStar()
a.init_grid(maze.maze, maze.start_cell[::-1], maze.end_cell[::-1])
best_path_astar = reverse2D(a.solve())
execute_path(maze.maze, best_path_astar, maze.x_host, maze.y_host)

# Find optimal path with Q-Learning
status = Status
model = QTableModel(maze, status, name="QTableModel")
h, w, _, _ = model.train(discount=0.90, exploration_rate=0.10, learning_rate=0.10, episodes=200,
                            stop_at_convergence=True)
best_path_qlearning = maze.play(model)
execute_path(maze.maze, maze.invert_policy(best_path_qlearning), maze.x_host, maze.y_host)