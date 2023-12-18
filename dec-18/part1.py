if __name__ == '__main__':
    instructions = []
    with open('data.txt', 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            instructions.append(line.split(' '))

    deltas = {
        'U': (-1, 0),
        'D': (+1, 0),
        'L': (0, -1),
        'R': (0, +1),
    }

    def trace(start, on_anchor_fn):
        cur = start
        for instruction in instructions:
            direction = instruction[0]
            distance = int(instruction[1])
            delta = deltas[direction]
            next = (cur[0] + delta[0] * distance, cur[1] + delta[1] * distance)
            on_anchor_fn(cur, next)
            cur = next

    # find max field size required
    max_row = 0
    max_col = 0
    min_row = 0
    min_col = 0

    def update_values(prev, cur):
        global max_row
        global max_col
        global min_row
        global min_col

        max_row = max(max_row, cur[0])
        max_col = max(max_col, cur[1])
        min_row = min(min_row, cur[0])
        min_col = min(min_col, cur[1])

    trace((0, 0), update_values)

    # real pass
    rows = max_row - min_row + 1
    cols = max_col - min_col + 1

    field = [[' ' for _ in range(cols)] for _ in range(rows)]

    def fill_line(prev, cur):
        delta_rows = cur[0] - prev[0]
        delta_cols = cur[1] - prev[1]

        row_step = 1 if delta_rows > 0 else -1 if delta_rows < 0 else 0
        col_step = 1 if delta_cols > 0 else -1 if delta_cols < 0 else 0

        tmp = prev
        field[tmp[0]][tmp[1]] = '#'

        while True:
            tmp = (tmp[0] + row_step, tmp[1] + col_step)
            field[tmp[0]][tmp[1]] = '#'
            if tmp == cur:
                break

    trace((-min_row, -min_col), fill_line)

    # save the field
    with open('data.out', 'w') as f:
        for row in field:
            f.write(''.join(row) + '\n')
        f.write('\n')

    # flood fill inside via BFS
    def flood_fill(start):
        visited = set()
        active = [start]

        while active:
            row, col = active.pop(-1)

            if (row, col) in visited:
                continue

            visited.add((row, col))
            field[row][col] = '.'

            neighbors = [
                (row - 1, col),
                (row + 1, col),
                (row, col - 1),
                (row, col + 1),
            ]
            for n_row, n_col in neighbors:
                if field[n_row][n_col] != ' ':
                    continue
                if (n_row, n_col) not in visited:
                    active.append((n_row, n_col))

    flood_fill((-min_row + 1, -min_col + 1))

    # save the field
    with open('data.out2', 'w') as f:
        for row in field:
            f.write(''.join(row) + '\n')
        f.write('\n')

    # count
    print(sum(
        sum(1 for col in range(cols) if field[row][col] in ('#', '.'))
        for row in range(rows)
    ))
