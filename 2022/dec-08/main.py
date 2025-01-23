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


def get_visible(point, direction):
    result = set()
    result.add(point)  # first point is always visible
    dr, dc = direction
    val = at(point)

    while True:
        # go next
        point = (point[0] + dr, point[1] + dc)
        if point[0] >= rows or point[0] < 0:
            break
        if point[1] >= cols or point[1] < 0:
            break

        if at(point) > val:
            result.add(point)
            val = at(point)

    return result


visible = set()


# handle left and right visibility
for r in range(rows):
    visible.update(get_visible((r, 0), (0, +1)))
    visible.update(get_visible((r, cols - 1), (0, -1)))

# handle up and down visibility
for c in range(cols):
    visible.update(get_visible((0, c), (+1, 0)))
    visible.update(get_visible((rows - 1, c), (-1, 0)))

print(len(visible))
