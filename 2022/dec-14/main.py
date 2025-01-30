traces = []

with open('data.txt', 'r') as file:
    while True:
        line = file.readline()

        if not line:
            break

        points = [x.split(',') for x in line.split(' -> ')]
        points = [(int(p[0]), int(p[1])) for p in points]

        traces.append(points)


max_row = 0
max_col = 0

for trace in traces:
    for col, row in trace:
        max_col = max(max_col, col)
        max_row = max(max_row, row)

field = [
    ['.'] * (max_col + 1)
    for _ in range(max_row + 1)
]

# fill the field
for trace in traces:
    for idx in range(1, len(trace)):
        p_prev = trace[idx - 1]
        p = trace[idx]
        delta_col = p[0] - p_prev[0]
        delta_row = p[1] - p_prev[1]

        if delta_col != 0:
            delta_col = delta_col // abs(delta_col)

        if delta_row != 0:
            delta_row = delta_row // abs(delta_row)

        cur = p_prev
        while True:
            field[cur[1]][cur[0]] = '#'
            if cur == p:
                break
            cur = cur[0] + delta_col, cur[1] + delta_row

def save(path):
    with open(path, 'w') as file:
        for row in field:
            for char in row:
                file.write(char)
            file.write('\n')

save('start.out')


def is_valid(pos):
    col, row = pos
    return row >= 0 and row < len(field) and col >= 0 and col < len(field[0])


def simulate_one(start) -> tuple[int, int] | None:
    cur = start
    while True:
        col, row = cur

        candidates = [
            (col, row + 1),
            (col - 1, row + 1),
            (col + 1, row + 1)
        ]

        for candidate in candidates:
            if not is_valid(candidate):
                # fell on sides
                return None

            candidate_col, candidate_row = candidate

            if field[candidate_row][candidate_col] == '.':
                cur = (candidate_col, candidate_row)
                break
        else:
            # final destination reached
            return cur

count = 0

while True:
    pos = simulate_one((500, 0))
    if pos is None:
        break
    field[pos[1]][pos[0]] = 'o'
    count += 1

save('finish.out')
print(count)
