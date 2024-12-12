file = open('data.txt', 'r')
field = [line.strip() for line in file.readlines()]

rows, cols = len(field), len(field[0])
visited = set()


def at(r, c):
    if r < 0 or r >= rows or c < 0 or c >= cols:
        return None
    return field[r][c]


def scan(cells, is_horizontal, delta):
    count = 0
    cell = next(iter(cells))
    cell_type = at(cell[0], cell[1])
    if is_horizontal:
        for row in range(rows):
            started = False
            for col in range(cols):
                if (row, col) not in cells:
                    started = False
                elif at(row + delta[0], col + delta[1]) != cell_type:
                    if not started:
                        count += 1
                    started = True
                else:
                    started = False
    else:
        for col in range(cols):
            started = False
            for row in range(rows):
                if (row, col) not in cells:
                    started = False
                elif at(row + delta[0], col + delta[1]) != cell_type:
                    if not started:
                        count += 1
                    started = True
                else:
                    started = False
    return count


def sides_count(cells):
    return (
        scan(cells, True, (-1, 0)) +
        scan(cells, True, (+1, 0)) +
        scan(cells, False, (0, -1)) +
        scan(cells, False, (0, +1))
    )


# returns tuple of area and perimeter
def calc(row, col):
    t = field[row][col]
    cells = set()

    def traverse(row, col):
        if (row, col) in cells:
            return
        cells.add((row, col))

        neig = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
        ]

        for r2, c2 in neig:
            if not (0 <= r2 < rows and 0 <= c2 < cols):
                continue
            if field[r2][c2] != t:
                continue
            if (r2, c2) in cells:
                continue
            traverse(r2, c2)

    traverse(row, col)
    visited.update(cells)

    return len(cells), sides_count(cells)


result = 0
for row in range(rows):
    for col in range(cols):
        if (row, col) not in visited:
            area, sc = calc(row, col)
            print('shape at %s of "%s", area: %s, sides count: %s' % ((row, col), at(row, col), area, sc))
            result += area * sc
print(result)