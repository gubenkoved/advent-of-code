import heapq

file = open('data.txt', 'r')
field = []

start = None
end = None

while True:
    line = file.readline()
    if not line:
        break
    field.append(list(line.strip()))

rows, cols = len(field), len(field[0])

for row in range(rows):
    for col in range(cols):
        if field[row][col] == 'S':
            start = (row, col)
        elif field[row][col] == 'E':
            end = (row, col)


def shortest():
    heap = [(0, start, None)]
    visited = set()
    parent = {}

    while heap:
        dist, (r, c), prev = heapq.heappop(heap)

        if (r, c) in visited:
            continue

        visited.add((r, c))
        parent[(r, c)] = prev

        if (r, c) == end:
            break

        neighbors = [
            (r - 1, c),
            (r + 1, c),
            (r, c - 1),
            (r, c + 1)
        ]

        for nr, nc in neighbors:
            if nr < 0 or nr >= rows:
                continue
            if nc < 0 or nc >= cols:
                continue
            if field[nr][nc] == '#':
                continue
            if (nr, nc) not in visited:
                heapq.heappush(heap, (dist + 1, (nr, nc), (r, c)))

    if end not in parent:
        return None

    # recover path
    path = []
    cur = end
    while cur != None:
        path.append(cur)
        cur = parent[cur]

    return len(path) - 1, list(reversed(path))


def path_contains(path: list[tuple[int, int]], cheat_start, cheat_end):
    for idx in range(len(path) - 1):
        if path[idx] == cheat_start and path[idx + 1] == cheat_end:
            return True
    return False


sd, _ = shortest()
print(sd)


directions = [
    (-1, 0),
    (+1, 0),
    (0, -1),
    (0, +1),
]


def rep(x):
    return '%r' % (x,)


count = 0
for cheat_start_row in range(rows):
    print('cheat start row:', cheat_start_row)
    for cheat_start_col in range(cols):
        if field[cheat_start_row][cheat_start_col] != '#':
            continue
        for dr, dc in directions:
            cheat_end_row = cheat_start_row + dr
            cheat_end_col = cheat_start_col + dc
            if cheat_end_row < 0 or cheat_end_row >= rows:
                continue
            if cheat_end_col < 0 or cheat_end_col >= cols:
                continue
            if field[cheat_end_row][cheat_end_col] == '#':
                continue
            field[cheat_start_row][cheat_start_col] = '.'
            cheat_dist, cheat_path = shortest()
            if sd - cheat_dist >= 100:
                if path_contains(cheat_path, (cheat_start_row, cheat_start_col), (cheat_end_row, cheat_end_col)):
                    count += 1
            field[cheat_start_row][cheat_start_col] = '#'
print(count)
