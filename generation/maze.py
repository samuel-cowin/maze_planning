from random import shuffle, randrange


class Maze():

    def __init__(self) -> None:
        self.reset_maze()


    def reset_maze(self):
        self.maze = []
        self.x_host = 1.5
        self.y_host = 0.5


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
            self.maze.append(row)
        last_row = [0]*(len(self.maze)-1) + [2] + [0]
        self.maze.append(last_row)
        self.maze[0][1] = 1
        return self.maze
