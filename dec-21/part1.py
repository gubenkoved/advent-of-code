if __name__ == '__main__':
    field = []
    with open('data.txt', 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            field.append(list(line.strip()))

    rows, cols = len(field), len(field[0])
    start = None
    for row in range(rows):
        for col in range(cols):
            if field[row][col] == 'S':
                start = (row, col)
                break
    assert start

    field[start[0]][start[1]] = '.'
    reachable = {start}

    for _ in range(64):
        current, reachable = reachable, set()
        for row, col in current:
            candidates = [
                (row - 1, col),
                (row + 1, col),
                (row, col - 1),
                (row, col + 1),
            ]
            for candidate_row, candidate_col in candidates:
                if not (0 < candidate_row < rows and 0 <= candidate_col < cols):
                    continue
                if field[candidate_row][candidate_col] != '.':
                    continue
                reachable.add((candidate_row, candidate_col))

    print(len(reachable))
