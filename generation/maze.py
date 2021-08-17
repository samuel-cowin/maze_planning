from random import shuffle, randrange
from enum import Enum, IntEnum
import logging

import math
import numpy as np


class Cell(IntEnum):
    WALL = 0  
    OPEN = 1  


class Action(IntEnum):
    MOVE_LEFT = 0
    MOVE_RIGHT = 1
    MOVE_UP = 2
    MOVE_DOWN = 3


class Status(Enum):
    WIN = 0
    LOSE = 1
    PLAYING = 2


class Maze():

    actions = [Action.MOVE_LEFT, Action.MOVE_RIGHT, Action.MOVE_UP, Action.MOVE_DOWN]  # all possible actions

    reward_exit = 10.0  # reward for reaching the exit cell
    penalty_move = -0.05  # penalty for a move which did not result in finding the exit cell
    penalty_visited = -0.25  # penalty for returning to a cell which was visited earlier
    penalty_impossible_move = -0.75  # penalty for trying to enter an occupied cell or moving out of the maze


    def __init__(self, dim=4) -> None:
        self.reset_maze(dim, dim)
        self.visualize(self.maze)

        self.__minimum_reward = -0.5 * self.maze.size  # stop game if accumulated reward is below this threshold

        nrows, ncols = self.maze.shape
        self.cells = [(col, row) for col in range(ncols) for row in range(nrows)]
        self.empty = [(col, row) for col in range(ncols) for row in range(nrows) if self.maze[row, col] >= Cell.OPEN]
        self.__exit_cell = (ncols - 1, nrows - 1) if self.end_cell is None else self.end_cell
        self.empty.remove(self.__exit_cell)

        # Check for impossible maze layout
        if self.__exit_cell not in self.cells:
            raise Exception("Error: exit cell at {} is not inside maze".format(self.__exit_cell))
        if self.maze[self.__exit_cell[::-1]] == Cell.WALL:
            raise Exception("Error: exit cell at {} is not free".format(self.__exit_cell))

        self.reset()


    def reset_maze(self, x, y):
        self.maze = self.make_maze(x, y)
        self.x_host = 1.5
        self.y_host = 0.5
        self.start_cell = (math.floor(self.x_host), math.floor(self.y_host))
        self.end_cell = ((len(self.maze)-1,len(self.maze[0])-2))[::-1]


    def visualize(self, maze):
        print('')
        print('Maze:')
        print('')
        for t in maze:
            print(t)
        print('')

    def walk(self, x, y, vis, ver, hor):
        vis[y][x] = 1

        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]:
                continue
            if xx == x:
                hor[max(y, yy)][x] = "+ "
            if yy == y:
                ver[y][max(x, xx)] = "  "
            self.walk(xx, yy, vis, ver, hor)


    def make_maze(self, w, h):
        maze = []
        vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
        ver = [["| "] * w + ['|'] for _ in range(h)]
        hor = [["+-"] * w + ['+'] for _ in range(h + 1)]

        self.walk(randrange(w), randrange(h), vis, ver, hor)
        s = ""
        for (a, b) in zip(hor, ver):
            s += ''.join(a + ['\n'] + b + ['\n'])

        splits = s.splitlines()
        for lines in splits:
            row = []
            for c in lines:
                if (c == ' '):
                    row.append(1)  # spaces are 1s
                elif ((c == '|') or (c == '+') or (c == '-')):
                    row.append(0)  # walls are 0s
            maze.append(row)
        last_row = [0]*(len(maze)-1) + [2] + [0]
        maze.append(last_row)
        maze[0][1] = 1
        self.maze = np.array(maze)
        return self.maze


    def reset(self):
        start_cell=self.start_cell
        if start_cell not in self.cells:
            raise Exception("Error: start cell at {} is not inside maze".format(start_cell))
        if self.maze[start_cell[::-1]] == Cell.WALL:
            raise Exception("Error: start cell at {} is not free".format(start_cell))
        if start_cell == self.__exit_cell:
            raise Exception("Error: start- and exit cell cannot be the same {}".format(start_cell))
        self.__previous_cell = self.__current_cell = start_cell
        self.__total_reward = 0.0  # accumulated reward
        self.__visited = set()  # a set() only stores unique values

        return self.__observe()


    def step(self, action):
        reward = self.__execute(action)
        self.__total_reward += reward
        status = self.__status()
        state = self.__observe()
        logging.debug("action: {:10s} | reward: {: .2f} | status: {}".format(Action(action).name, reward, status))
        return state, reward, status


    def __execute(self, action):
        possible_actions = self.__possible_actions(self.__current_cell)

        if not possible_actions:
            reward = self.__minimum_reward - 1  # cannot move anywhere, force end of game
        elif action in possible_actions:
            col, row = self.__current_cell
            if action == Action.MOVE_LEFT:
                col -= 1
            elif action == Action.MOVE_UP:
                row -= 1
            if action == Action.MOVE_RIGHT:
                col += 1
            elif action == Action.MOVE_DOWN:
                row += 1

            self.__previous_cell = self.__current_cell
            self.__current_cell = (col, row)

            if self.__current_cell == self.__exit_cell:
                reward = Maze.reward_exit  # maximum reward when reaching the exit cell
            elif self.__current_cell in self.__visited:
                reward = Maze.penalty_visited  # penalty when returning to a cell which was visited earlier
            else:
                reward = Maze.penalty_move  # penalty for a move which did not result in finding the exit cell

            self.__visited.add(self.__current_cell)
        else:
            reward = Maze.penalty_impossible_move  # penalty for trying to enter an occupied cell or move out of the maze

        return reward


    def __possible_actions(self, cell=None):
        if cell is None:
            col, row = self.__current_cell
        else:
            col, row = cell

        possible_actions = Maze.actions.copy()  # initially allow all

        # now restrict the initial list by removing impossible actions
        nrows, ncols = self.maze.shape
        if row == 0 or (row > 0 and self.maze[row - 1, col] == Cell.WALL):
            possible_actions.remove(Action.MOVE_UP)
        if row == nrows - 1 or (row < nrows - 1 and self.maze[row + 1, col] == Cell.WALL):
            possible_actions.remove(Action.MOVE_DOWN)

        if col == 0 or (col > 0 and self.maze[row, col - 1] == Cell.WALL):
            possible_actions.remove(Action.MOVE_LEFT)
        if col == ncols - 1 or (col < ncols - 1 and self.maze[row, col + 1] == Cell.WALL):
            possible_actions.remove(Action.MOVE_RIGHT)

        return possible_actions


    def __status(self):
        if self.__current_cell == self.__exit_cell:
            return Status.WIN

        if self.__total_reward < self.__minimum_reward:  # force end of game after to much loss
            return Status.LOSE

        return Status.PLAYING


    def __observe(self):
        return np.array([[*self.__current_cell]])


    def play(self, model):
        self.reset()

        state = self.__observe()

        total = 0
        actions = []
        while True:
            action = model.predict(state=state)
            actions.append(action)
            state, reward, status = self.step(action)
            total += reward
            if status in (Status.WIN, Status.LOSE):
                print('Agent path of length {} resulted in a {} with reward of {}'\
                    .format(len(actions), status.name.lower(), total))
                return actions

    
    def invert_policy(self, state_actions):
        plot_policy = []
        curr = [math.floor(self.x_host), math.floor(self.y_host)]
        plot_policy = [curr]

        for sa in state_actions:
            # Left
            if sa == 0:
                curr = [curr[0]-1, curr[1]]
                plot_policy.append(curr)
            # Right
            if sa == 1:
                curr = [curr[0]+1, curr[1]]
                plot_policy.append(curr)
            # Up
            if sa == 2:
                curr = [curr[0], curr[1]-1]
                plot_policy.append(curr)
            # Down
            if sa == 3:
                curr = [curr[0], curr[1]+1]
                plot_policy.append(curr)
        return plot_policy