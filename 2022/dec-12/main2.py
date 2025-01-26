import heapq

field = []

with open('data.txt', 'r') as file:
    while True:
        line = file.readline()
        if not line:
            break
        field.append(list(line.strip()))


heap = []
visited = set()

rows, cols = len(field), len(field[0])

end = None

# start with marking all "a" nodes as possible start locations
for row in range(rows):
    for col in range(cols):
        if field[row][col] == 'S':
            heapq.heappush(heap, (0, (row, col)))
            field[row][col] = 'a'
        elif field[row][col] == 'E':
            field[row][col] = 'z'
            end = (row, col)

assert len(heap) == 1
assert end is not None

while heap:
    dist, (row, col) = heapq.heappop(heap)

    if (row, col) in visited:
        continue

    visited.add((row, col))

    if (row, col) == end:
        print(dist)
        break

    neighbors = [
        (row - 1, col),
        (row + 1, col),
        (row, col - 1),
        (row, col + 1),
    ]
    for nr, nc in neighbors:
        if nr < 0 or nr >= rows:
            continue
        if nc < 0 or nc >= cols:
            continue
        if ord(field[nr][nc]) - ord(field[row][col]) > 1:
            continue
        heapq.heappush(heap, (dist + 1, (nr, nc)))

