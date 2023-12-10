if __name__ == '__main__':
    field = []
    with open('data.txt', 'r') as f:
        while True:
            line = f.readline()

            if not line:
                break

            line = line.strip()

            field.append(list(line))

    rows, cols = len(field), len(field[0])

    # find the starting point
    start = None

    for row in range(rows):
        for col in range(cols):
            if field[row][col] == 'S':
                start = (row, col)

    assert start is not None

    # traverse from the start
    loop = []
    cur = start

    while True:
        # find adjacent pipes
        adjacent = []

        cur_cell = field[cur[0]][cur[1]]

        if cur_cell == '|':
            adjacent.append((cur[0] - 1, cur[1]))
            adjacent.append((cur[0] + 1, cur[1]))
        elif cur_cell == '-':
            adjacent.append((cur[0], cur[1] - 1))
            adjacent.append((cur[0], cur[1] + 1))
        elif cur_cell == 'L':
            adjacent.append((cur[0] - 1, cur[1]))
            adjacent.append((cur[0], cur[1] + 1))
        elif cur_cell == '7':
            adjacent.append((cur[0] + 1, cur[1]))
            adjacent.append((cur[0], cur[1] - 1))
        elif cur_cell == 'J':
            adjacent.append((cur[0] - 1, cur[1]))
            adjacent.append((cur[0], cur[1] - 1))
        elif cur_cell == 'F':
            adjacent.append((cur[0] + 1, cur[1]))
            adjacent.append((cur[0], cur[1] + 1))
        elif cur_cell == 'S':
            # start cell handling
            if field[cur[0]][cur[1] - 1] in ['-', 'F', 'L']:
                adjacent.append((cur[0], cur[1] - 1))
            if field[cur[0]][cur[1] + 1] in ['-', '7', 'J']:
                adjacent.append((cur[0], cur[1] + 1))
            if field[cur[0] - 1][cur[1]] in ['|', '7', 'F']:
                adjacent.append((cur[0] - 1, cur[1]))
            if field[cur[0] + 1][cur[1]] in ['|', 'L', 'J']:
                adjacent.append((cur[0] - 1, cur[1]))

        # pick not yet visited one
        for point in adjacent:
            if point not in loop:
                cur = point
                loop.append(point)
                break
        else:
            # assert False, 'stuck at %s' % (cur, )
            break

        if cur == start:
            break

    loop.insert(0, start)

    # print loop
    with open('data.out', 'w') as f:
        for row in range(rows):
            for col in range(cols):
                if (row, col) in loop:
                    print(field[row][col], end='', file=f)
                else:
                    print('.', end='', file=f)
            print(file=f)

    print('Loop len: %d, answer %d' % (len(loop), len(loop) // 2))
