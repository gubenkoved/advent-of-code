import heapq

file = open('data.txt', 'r')

coordinates = []
for line in file:
    r, c = [int(x) for x in line.strip().split(',')]
    coordinates.append((r, c))


obstacles = set(coordinates[:1024])
rows = 71
cols = 71


def print_field():
    for row in range(rows):
        for col in range(cols):
            if (row, col) in obstacles:
                print('#', end='')
            else:
                print('.', end='')
        print()


print_field()


def shortest_distance(start, end):
    heap = [(0, start)]
    visited = set()

    while heap:
        dist, cur = heapq.heappop(heap)

        if cur in visited:
            continue

        visited.add(cur)

        if cur == end:
            return dist

        r, c = cur

        neighbors = [
            (r - 1, c),
            (r + 1, c),
            (r, c - 1),
            (r, c + 1),
        ]
        for nr, nc in neighbors:
            if nr < 0 or nr >= rows:
                continue
            if nc < 0 or nc >= cols:
                continue
            if (nr, nc) in obstacles:
                continue
            if (nr, nc) in visited:
                continue
            heapq.heappush(heap, (dist + 1, (nr, nc)))


for r, c in coordinates[1024:]:
    obstacles.add((r, c))
    if shortest_distance((0, 0), (rows - 1, cols - 1)) is None:
        print('(%s, %s)' % (r, c))
        break

