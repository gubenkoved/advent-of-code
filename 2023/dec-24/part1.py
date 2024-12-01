data = []

with open('input.txt', 'r') as f:
    while True:
        line = f.readline()
        if not line:
            break
        pos, speed = line.strip().split('@')
        data.append((
            tuple(int(x) for x in pos.split(',')),
            tuple(int(x) for x in speed.split(',')),
        ))

n = len(data)
result = 0
min_, max_ = 200000000000000, 400000000000000


def check_same_side(center, a, b):
    vector_a = (a[0] - center[0], a[1] - center[1])
    vector_b = (b[0] - center[0], b[1] - center[1])
    dot_product = vector_a[0] * vector_b[0] + vector_a[1] * vector_b[1]
    return dot_product > 0


def find_intersection(l1, l2):
    (x1, y1, _), (vx1, vy1, _) = l1
    (x3, y3, _), (vx2, vy2, _) = l2

    # second points on the line
    x2, y2 = x1 + vx1, y1 + vy1
    x4, y4 = x3 + vx2, y3 + vy2

    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if denominator == 0:
        return None

    px = (x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)
    py = (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)

    rx, ry = px / denominator, py / denominator

    # check that intersection point is from the same side as the second point to
    # account for line starting at specific point
    if not check_same_side((x1, y1), (x2, y2), (rx, ry)):
        return None

    if not check_same_side((x3, y3), (x4, y4), (rx, ry)):
        return None

    return rx, ry


for idx1 in range(n):
    for idx2 in range(idx1 + 1, n):
        intersection = find_intersection(data[idx1], data[idx2])

        if not intersection:
            continue

        if (min_ <= intersection[0] <= max_ and
                min_ <= intersection[1] <= max_):
            result += 1
print(result)
