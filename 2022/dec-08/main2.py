field = []

with open('data.txt', 'r') as file:
    while True:
        line = file.readline()

        if not line:
            break

        field.append(line.strip())


rows, cols = len(field), len(field[0])


def at(point):
    return field[point[0]][point[1]]


def add(point, delta):
    return point[0] + delta[0], point[1] + delta[1]


def is_valid(point):
    return point[0] >= 0 and point[0] < rows and point[1] >= 0 and point[1] < cols


def score(point):

    def trace(point, dir):
        start_val = at(point)
        count = 0
        while True:
            point = add(point, dir)
            if not is_valid(point):
                break
            count += 1
            if at(point) >= start_val:
                break
        return count

    result = 1

    directions = [
        (0, -1),
        (0, +1),
        (-1, 0),
        (+1, 0),
    ]

    for direction in directions:
        result *= trace(point, direction)

    return result


best_score = 0
for r in range(rows):
    for c in range(cols):
        best_score = max(best_score, score((r, c)))
print(best_score)
