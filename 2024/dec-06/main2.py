import copy

file = open('data.txt', 'r')
field = [list(line.strip()) for line in file.readlines()]

rows, cols = len(field), len(field[0])

start = None
for row in range(rows):
    for col in range(cols):
        if field[row][col] == '^':
            start = (row, col)

rot_map = {
    (-1, 0): (0, 1),
    (0, 1): (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
}


def rotate(direction):
    return rot_map[direction]


def is_loopy(field):
    visited = set()
    direction = (-1, 0)
    cur = start
    while True:
        if (cur, direction) in visited:
            return True  # loop
        visited.add((cur, direction))

        next = (cur[0] + direction[0], cur[1] + direction[1])

        if next[0] >= rows or next[0] < 0 or next[1] >= cols or next[1] < 0:
            return False  # no loop

        # rotate if necessary
        if field[next[0]][next[1]] == '#':
            while field[next[0]][next[1]] == '#':
                direction = rotate(direction)
                next = (cur[0] + direction[0], cur[1] + direction[1])
            assert field[next[0]][next[1]] != '#'
            cur = next
        else:
            # move forward
            cur = next

result = 0
for row in range(rows):
    print('checking line %s' % row)
    for col in range(cols):
        if field[row][col] in ('#', '^'):
            continue
        tmp = field[row][col]
        field[row][col] = '#'
        if is_loopy(field):
            print('new obstacle at %r' % ((row, col),))
            result += 1
        field[row][col] = tmp

print(result)

