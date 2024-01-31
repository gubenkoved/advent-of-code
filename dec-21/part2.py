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

    visited = set()
    layer = [start]
    step = 0
    last_reachable = 0

    def at(r, c):
        return field[r % rows][c % cols]

    odd_dist_count, even_dist_count = 0, 0

    while True:
        next_layer = []
        for position in layer:
            if position in visited:
                continue
            visited.add(position)

            if step % 2 == 0:
                even_dist_count += 1
            else:
                odd_dist_count += 1

            row, col = position
            candidates = [
                (row - 1, col),
                (row + 1, col),
                (row, col - 1),
                (row, col + 1),
            ]
            for candidate in candidates:
                if at(*candidate) != '.':
                    continue
                if candidate not in visited:
                    next_layer.append(candidate)

        layer = next_layer
        diff = len(visited) - last_reachable
        print('step %6d reachable %8d [%-8d+%8d] %+6d from prev' % (
            step, len(visited), odd_dist_count, even_dist_count, diff))
        last_reachable = len(visited)
        step += 1
