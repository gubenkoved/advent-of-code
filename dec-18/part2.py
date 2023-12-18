if __name__ == '__main__':
    instructions = []
    direction_translation_map = {
        '0': 'R',
        '1': 'D',
        '2': 'L',
        '3': 'U',
    }
    with open('data.txt', 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            raw = line.split(' ')[2]
            raw = raw.strip('#()\n')
            distance_hex = raw[:-1]
            direction_raw = raw[-1]
            instructions.append(
                (direction_translation_map[direction_raw], int(distance_hex, 16))
            )

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

    # list of points
    polygon = [
        (0, 0),
    ]

    def add_point(prev, cur):
        polygon.append(cur)

    trace((0, 0), add_point)

    # normalize so that all coordinates are positive
    min_row = min(p[0] for p in polygon)
    min_col = min(p[1] for p in polygon)

    polygon = [(p[0] - min_row, p[1] - min_col) for p in polygon]
    n = len(polygon)

    def perimeter(polygon):
        total = 0
        cur = polygon[0]
        for point in polygon[1:]:
            delta_row, delta_col = point[0] - cur[0], point[1] - cur[1]
            assert delta_row == 0 or delta_col == 0
            total += abs(delta_row + delta_col)
            cur = point
        return total

    print('Polygon with %d points' % n)
    print('Perimeter: %d' % perimeter(polygon))

    area = 0
    for ptr in range(1, n):
        area += polygon[ptr][0] * polygon[ptr - 1][1]
        area -= polygon[ptr - 1][0] * polygon[ptr][1]
    area = abs(area / 2)

    print('Area: %d' % area)
    print('Area with half-perimeter: %d' % (area + perimeter(polygon) / 2))

    # answer is above + 1!
    # it half-manually figured this one out w/o full understanding
