file = open('data.txt', 'r')
field = [line.strip() for line in file.readlines()]

rows, cols = len(field), len(field[0])

cur = None
direction = (-1, 0)
for row in range(rows):
    for col in range(cols):
        if field[row][col] == '^':
            cur = (row, col)

rot_map = {
    (-1, 0): (0, 1),
    (0, 1): (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
}


def rotate(direction):
    return rot_map[direction]


visited = set()
while True:
    if (cur, direction) in visited:
        break
    visited.add((cur, direction))

    next = (cur[0] + direction[0], cur[1] + direction[1])

    if next[0] >= rows or next[0] < 0 or next[1] >= cols or next[1] < 0:
        break

    if field[next[0]][next[1]] == '#':
        direction = rotate(direction)
        next = (cur[0] + direction[0], cur[1] + direction[1])
        cur = next
    else:
        # move forward
        cur = next

visited_cells = set()
for pos, direction in visited:
    visited_cells.add(pos)

print(len(visited_cells))

with open('out.txt', 'w') as f:
    for row in range(rows):
        for col in range(cols):
            if (row, col) in visited_cells:
                f.write('x')
            else:
                f.write(field[row][col])
        f.write('\n')

