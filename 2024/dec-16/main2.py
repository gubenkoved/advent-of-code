import heapq
from collections import defaultdict
import time

started_at = time.time()
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
heapq.heappush(queue, (0, next(idx_gen), start, 1j, None))
visited = set()
parent = defaultdict(set)  # node -> parent nodes
best = None


def at(pos):
    return field[int(pos.real)][int(pos.imag)]

# run regular Dijkstra
while queue:
    score, _, pos, direction, prev_state = heapq.heappop(queue)

    state = (pos, direction, score)
    parent[state].add(prev_state)

    if (pos, direction) in visited:
        continue

    # capture the shortest path to the end
    if pos == end and best is None:
        best = state

    visited.add((pos, direction))

    neighbors = [
        # continue in the same direction
        (score + 1, next(idx_gen), pos + direction, direction, state),
        # rotate
        (score + 1000, next(idx_gen), pos, direction * 1j, state),
        (score + 1000, next(idx_gen), pos, direction * -1j, state)
    ]

    for neighbor in neighbors:
        n_score, n_idx, n_pos, n_dir, n_prev_state = neighbor
        if at(n_pos) == '#':
            continue
        heapq.heappush(queue, neighbor)

best_states = set()

def trace(state):
    best_states.add(state)
    for parent_state in parent.get(state, []):
        if parent_state is not None:
            trace(parent_state)

# trace back from the start
trace(best)

# how many cells?
best_positions = set()
for pos, direction, score in best_states:
    best_positions.add(pos)

print(len(best_positions))
print('elapsed: %.3fs' % (time.time() - started_at))
