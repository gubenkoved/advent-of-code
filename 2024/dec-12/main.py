file = open('data.txt', 'r')
field = [line.strip() for line in file.readlines()]

rows, cols = len(field), len(field[0])
visited = set()


# returns tuple of area and perimeter
def calc(row, col):
    t = field[row][col]
    area = 0
    perimiter = 0

    def traverse(row, col):
        nonlocal area
        nonlocal perimiter

        if (row, col) in visited:
            return
        visited.add((row, col))
        area += 1

        neig = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
        ]

        for r2, c2 in neig:
            if not (0 <= r2 < rows and 0 <= c2 < cols):
                perimiter += 1
                continue
            if field[r2][c2] != t:
                perimiter += 1
                continue
            if (r2, c2) in visited:
                continue
            traverse(r2, c2)

    traverse(row, col)

    return area, perimiter


result = 0
for row in range(rows):
    for col in range(cols):
        if (row, col) not in visited:
            a, p = calc(row, col)
            result += a * p
print(result)