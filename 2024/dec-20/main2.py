import functools
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


@functools.lru_cache(maxsize=None)
def shortest(start, end):
    heap = [(0, start)]
    visited = set()

    while heap:
        dist, (r, c) = heapq.heappop(heap)

        if (r, c) in visited:
            continue

        visited.add((r, c))

        if (r, c) == end:
            return dist

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

            heapq.heappush(heap, (dist + 1, (nr, nc)))

    return None


sd = shortest(start, end)
print(sd)


max_cheat_distance = 20
count = 0
for cheat_start_row in range(rows):
    print('cheat start row: %d (cur count %d)' % (cheat_start_row, count))
    for cheat_start_col in range(cols):
        if field[cheat_start_row][cheat_start_col] == '#':
            continue
        for cheat_end_row in range(cheat_start_row - max_cheat_distance, cheat_start_row + max_cheat_distance + 1):
            for cheat_end_col in range(cheat_start_col - max_cheat_distance, cheat_start_col + max_cheat_distance + 1):
                cheat_dist = abs(cheat_end_row - cheat_start_row) + abs(cheat_end_col - cheat_start_col)
                if cheat_dist > max_cheat_distance:
                    continue
                if cheat_dist == 0:
                    continue
                if cheat_end_row < 0 or cheat_end_row >= rows:
                    continue
                if cheat_end_col < 0 or cheat_end_col >= cols:
                    continue
                if field[cheat_end_row][cheat_end_col] == '#':
                    continue
                cheat_start = (cheat_start_row, cheat_start_col)
                cheat_end = (cheat_end_row, cheat_end_col)
                dist_to_cheat_start = shortest(
                    start, cheat_start
                )
                if dist_to_cheat_start is None:
                    continue
                dist_from_cheat_end = shortest(cheat_end, end)
                if dist_from_cheat_end is None:
                    continue
                path_with_cheat_dist = dist_to_cheat_start + cheat_dist + dist_from_cheat_end
                if sd - path_with_cheat_dist >= 100:
                    # print('cheat %r -> %r saves %d' % (cheat_start, cheat_end, sd - path_with_cheat_dist))
                    count += 1
print(count)
