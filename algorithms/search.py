import collections
import math


def check_no_collision(xm, ym, xh, yh, maze_data):
    if ym+1 == yh:
        if (maze_data[math.ceil(yh)][math.floor(xh)]):
            return True
        else:
            return False
    elif xm+1 == xh:
        if (maze_data[math.floor(yh)][math.ceil(xh)]):
            return True
        else:
            return False
    elif xm-1 == xh:
        if (maze_data[math.floor(yh)][math.floor(xh)]):
            return True
        else:
            return False
    elif ym-1 == yh:
        if (maze_data[math.floor(yh)][math.floor(xh)]):
            return True
        else:
            return False
    else:
        return False


def bfs(grid, start, goal):
    width = len(grid[0])
    height = len(grid)
    queue = collections.deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if grid[y][x] == goal:
            return path
        for x2, y2 in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            if 0 <= x2 < width and 0 <= y2 < height and check_no_collision(x, y, x2, y2, grid) and (x2, y2) not in seen:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))