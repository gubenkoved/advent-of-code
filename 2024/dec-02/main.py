f = open('data.txt', 'r')

levels = [[int(x) for x in line.split(' ')] for line in f.readlines()]

def is_safe(level):
    is_inc = (level[1] - level[0]) > 0
    for idx in range(1, len(level)):
        if is_inc:
            if level[idx] <= level[idx - 1]:
                return False
        else:
            if level[idx] >= level[idx - 1]:
                return False

        if abs(level[idx] - level[idx - 1]) > 3:
            return False

    return True

print(sum(1 for level in levels if is_safe(level)))


def is_safe2(level):
    for idx in range(len(level)):
        level2 = level[:idx] + level[idx + 1:]
        if is_safe(level2):
            return True
    return False

print(sum(1 for level in levels if is_safe2(level)))
