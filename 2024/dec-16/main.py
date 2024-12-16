import heapq


file = open('data.txt', 'r')
field = []
for line in file:
    field.append(list(line.strip()))

rows, cols = len(field), len(field[0])

start = None
end = None
for row in range(rows):
    for col in range(cols):
        if field[row][col] == 'S':
            start = row + 1j * col
            field[row][col] = '.'
        elif field[row][col] == 'E':
            end = row + 1j * col
            field[row][col] = '.'


def monotonic_index():
    idx = 0
    while True:
        yield idx
        idx += 1

idx_gen = monotonic_index()
queue = []
heapq.heappush(queue, (0, next(idx_gen), start, 1j))
visited = set()


def at(pos):
    return field[int(pos.real)][int(pos.imag)]

# run regular Dijkstra
while queue:
    score, _, pos, direction = heapq.heappop(queue)

    if (pos, direction) in visited:
        continue

    visited.add((pos, direction))

    if pos == end:
        print('score: %d' % score)
        break

    neighbors = [
        # continue in the same direction
        (score + 1, next(idx_gen), pos + direction, direction),
        # rotate
        (score + 1000, next(idx_gen), pos, direction * 1j),
        (score + 1000, next(idx_gen), pos, direction * -1j)
    ]

    for neighbor in neighbors:
        n_score, n_idx, n_pos, n_dir = neighbor
        if at(n_pos) == '#':
            continue
        heapq.heappush(queue, neighbor)
