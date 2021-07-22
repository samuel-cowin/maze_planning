import math


def check_no_collision(xm, ym, xh, yh, maze_data, val=(1,2)):
    if ym+1 == yh:
        if (maze_data[math.ceil(yh)][math.floor(xh)] in val):
            return True
        else:
            return False
    elif xm+1 == xh:
        if (maze_data[math.floor(yh)][math.ceil(xh)] in val):
            return True
        else:
            return False
    elif xm-1 == xh:
        if (maze_data[math.floor(yh)][math.floor(xh)] in val):
            return True
        else:
            return False
    elif ym-1 == yh:
        if (maze_data[math.floor(yh)][math.floor(xh)] in val):
            return True
        else:
            return False
    else:
        return False