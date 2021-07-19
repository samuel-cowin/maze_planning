import matplotlib.pyplot as plt
from matplotlib import colors


def go_down(x, y):
    y = y + 1
    return x, y


def go_right(x, y):
    x = x + 1
    return x, y


def go_left(x, y):
    x = x - 1
    return x, y


def go_up(x, y):
    y = y - 1
    return x, y
    

def plot_maze(maze_animation, x, y):
    plt.ion()
    cMap = colors.ListedColormap(['k', 'w'])
    plt.xticks([])
    plt.yticks([])
    plt.gca().invert_yaxis()
    plt.pcolormesh(maze_animation, cmap=cMap)
    plt.plot(x, y, 'go')
    plt.show()
    plt.pause(0.1)
    plt.clf()


def execute_path(test_maze, moves, x1, y1):
    if moves is not None:
        for i in range(len(moves)-1):
            plot_maze(test_maze, x1, y1)
            if moves[i][1]+1 == moves[i+1][1]:
                x1, y1 = go_down(x1, y1)
            elif moves[i][0]+1 == moves[i+1][0]:
                x1, y1 = go_right(x1, y1)
            elif moves[i][0]-1 == moves[i+1][0]:
                x1, y1 = go_left(x1, y1)
            elif moves[i][1]-1 == moves[i+1][1]:
                x1, y1 = go_up(x1, y1)