import os

file = open('data.txt', 'r')
field = []

while True:
    line = file.readline()

    if line == '\n':
        break

    row = []

    for c in line.strip():
        if c == 'O':
            row.append('[')
            row.append(']')
        elif c == '#':
            row.append('#')
            row.append('#')
        elif c == '.':
            row.append('.')
            row.append('.')
        elif c == '@':
            row.append('@')
            row.append('.')
        else:
            assert False

    field.append(row)

moves = []

while True:
    line = file.readline()
    if not line:
        break
    moves.extend(list(line.strip()))


rows, cols = len(field), len(field[0])

robot_pos = None

# find the robot position
for row in range(rows):
    for col in range(cols):
        if field[row][col] == '@':
            robot_pos = (row, col)


def at(pos):
    return field[pos[0]][pos[1]]

def set(pos, value):
    field[pos[0]][pos[1]] = value


assert robot_pos is not None
# erase robot from the field
set(robot_pos, '.')


def pos_in_direction(pos, direction):
    if direction == '<':
        return pos[0], pos[1] - 1
    elif direction == '>':
        return pos[0], pos[1] + 1
    elif direction == '^':
        return pos[0] - 1, pos[1]
    elif direction == 'v':
        return pos[0] + 1, pos[1]
    else:
        assert False, 'what?'


def can_move(pos, direction):
    if at(pos) == '#':
        return False
    elif at(pos) == '.':
        return True
    elif at(pos) in ('[', ']'):
        if direction in ('^', 'v'):
            if at(pos) == '[':
                left_pos = pos
                right_pos = (pos[0], pos[1] + 1)
            elif at(pos) == ']':
                left_pos = (pos[0], pos[1] - 1)
                right_pos = pos
            assert at(left_pos) == '['
            assert at(right_pos) == ']'
            next_pos_left = pos_in_direction(left_pos, direction)
            next_pos_right = pos_in_direction(right_pos, direction)
            if can_move(next_pos_left, direction) and can_move(next_pos_right, direction):
                return True
            else:
                return False
        else:
            # left/right there is no binding
            next_pos = pos_in_direction(pos, direction)
            if can_move(next_pos, direction):
                return True
            else:
                return False
    else:
        assert False, 'what?'


def do_move(pos, direction):
    if at(pos) == '#':
        assert False, 'can not!'
    elif at(pos) == '.':
        pass
    elif at(pos) in ('[', ']'):
        if direction in ('^', 'v'):
            if at(pos) == '[':
                left_pos = pos
                right_pos = (pos[0], pos[1] + 1)
            elif at(pos) == ']':
                left_pos = (pos[0], pos[1] - 1)
                right_pos = pos
            next_pos_left = pos_in_direction(left_pos, direction)
            next_pos_right = pos_in_direction(right_pos, direction)
            do_move(next_pos_left, direction)
            do_move(next_pos_right, direction)
            set(next_pos_left, '[')
            set(next_pos_right, ']')
            set(left_pos, '.')
            set(right_pos, '.')
        else:
            # left/right there is no binding
            next_pos = pos_in_direction(pos, direction)
            do_move(next_pos, direction)
            assert at(next_pos) == '.'
            set(next_pos, at(pos))
            set(pos, '.')
    else:
        assert False, 'what?'



def move_if_possible(pos, direction):
    ok = can_move(pos, direction)
    if ok:
        do_move(pos, direction)
    return ok


def print_field(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        for row in range(rows):
            for col in range(cols):
                if (row, col) == robot_pos:
                    assert at((row, col)) == '.'
                    f.write('@')
                else:
                    f.write(at((row, col)))
            f.write('\n')


def gps(pos):
    return pos[0] * 100 + pos[1]

print_field('out/__field_start.txt')
for idx, move in enumerate(moves):
    next_pos = pos_in_direction(robot_pos, move)
    if at(next_pos) == '.':
        robot_pos = next_pos
    elif at(next_pos) == '#':
        pass
    elif at(next_pos) in ('[', ']'):
        if move_if_possible(next_pos, move):
            robot_pos = next_pos
    else:
        assert False, 'what?'
    # print_field('out/field_%d.txt' % idx)

result = 0
for row in range(rows):
    for col in range(cols):
        if at((row, col)) == '[':
            result += gps((row, col))
print(result)
