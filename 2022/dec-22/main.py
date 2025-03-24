import re
import functools

field = []

with open('data.txt', 'r') as f:
    while True:
        line = f.readline()

        if not line:
            break

        line = line.rstrip()

        if not line:
            break

        field.append(line)

    path = f.readline()

# pos and direction are (row, col)
pos = None
direction = (0, +1)

for col in range(len(field[0])):
    if field[0][col] != ' ':
        pos = (0, col)
        break


def add(pos, direction):
    return pos[0] + direction[0], pos[1] + direction[1]


def parse_path(path):
    # use capturing parenthesis so that delimiters are preserved as well
    return re.split('([LR])', path)

parsed_path = parse_path(path)

clockwise = {
    (+1, 0): (0, -1),
    (0, -1): (-1, 0),
    (-1, 0): (0, +1),
    (0, +1): (+1, 0),
}

counter_clockwise = {
    (+1, 0): (0, +1),
    (0, +1): (-1, 0),
    (-1, 0): (0, -1),
    (0, -1): (+1, 0),
}

def opposite(direction):
    return direction[0] * -1, direction[1] * -1

def is_in_field(pos):
    row, col = pos

    if row < 0 or row >= len(field):
        return False

    if col < 0 or col >= len(field[row]):
        return False

    if field[row][col] == ' ':
        return False

    return True


@functools.cache
def last_cell(pos, direction):
    while True:
        new_pos = add(pos, direction)
        if not is_in_field(new_pos):
            break
        pos = new_pos
    return pos

@functools.cache
def resolve(pos, direction):
    next_pos = add(pos, direction)

    if not is_in_field(next_pos):
        next_pos = last_cell(pos, opposite(direction))

    return next_pos

def at(pos):
    return field[pos[0]][pos[1]]


def step(pos, direction):
    next_pos = resolve(pos, direction)

    if at(next_pos) == '.':
        return next_pos
    elif at(next_pos) == '#':
        # unable to move
        return pos
    else:
        assert 'where the hell we are?'

for move in parsed_path:
    if move == 'L':
        direction = counter_clockwise[direction]
    elif move == 'R':
        direction = clockwise[direction]
    else:
        units = int(move)
        for _ in range(units):
            pos = step(pos, direction)

print(pos)
print(direction)

# Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^).
direction_cost = {
    (0, +1): 0,
    (+1, 0): 1,
    (0, -1): 2,
    (-1, 0): 3,
}

print((pos[0] + 1) * 1000 + ((1 + pos[1]) * 4) + direction_cost[direction])
