import os

file = open('data.txt', 'r')
field = []

while True:
    line = file.readline()

    if line == '\n':
        break

    field.append(list(line.strip()))

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



def move_if_possible(pos, direction):
    if at(pos) == '#':
        return False
    elif at(pos) == '.':
        return True
    elif at(pos) == 'O':
        next_pos = pos_in_direction(pos, direction)
        if move_if_possible(next_pos, direction):
            assert at(next_pos) == '.'
            set(next_pos, 'O')
            set(pos, '.')
            return True
        else:
            return False


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


for idx, move in enumerate(moves):
    next_pos = pos_in_direction(robot_pos, move)
    if at(next_pos) == '.':
        robot_pos = next_pos
    elif at(next_pos) == '#':
        pass
    elif at(next_pos) == 'O':
        if move_if_possible(next_pos, move):
            robot_pos = next_pos
    # print_field('out/field_%d.txt' % idx)

result = 0
for row in range(rows):
    for col in range(cols):
        if at((row, col)) == 'O':
            result += gps((row, col))
print(result)
