if __name__ == '__main__':

    field = []
    with open('data.txt', 'r') as f:
        while True:
            line = f.readline()

            if not line:
                break

            line = line.rstrip('\n')

            field.append(line)

    rows, cols = len(field), len(field[0])

    # indexes of empty rows and cols
    empty_rows = []
    empty_cols = []

    for row_idx in range(rows):
        is_empty = True
        for col_idx in range(cols):
            if field[row_idx][col_idx] != '.':
                is_empty = False
        if is_empty:
            empty_rows.append(row_idx)

    for col_idx in range(cols):
        is_empty = True
        for row_idx in range(rows):
            if field[row_idx][col_idx] != '.':
                is_empty = False
        if is_empty:
            empty_cols.append(col_idx)

    galaxies = []

    row_delta = 0
    col_delta = 0

    for row_idx in range(rows):
        if row_idx in empty_rows:
            row_delta += 1
        for col_idx in range(cols):
            col_delta = sum(1 for idx in empty_cols if idx < col_idx)
            if field[row_idx][col_idx] == '#':
                galaxies.append(
                    (row_idx + row_delta, col_idx + col_delta)
                )

    result = 0

    n = len(galaxies)
    for i in range(n - 1):
        for j in range(i + 1, n):
            p1 = galaxies[i]
            p2 = galaxies[j]

            result += abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    print(result)
