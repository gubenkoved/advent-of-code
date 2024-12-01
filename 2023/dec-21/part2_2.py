import collections

if __name__ == '__main__':
    field = []
    with open('data.txt', 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            field.append(list(line.strip()))

    rows, cols = len(field), len(field[0])
    start = None
    for row in range(rows):
        for col in range(cols):
            if field[row][col] == 'S':
                start = (row, col)
                break
    assert start

    field[start[0]][start[1]] = '.'
    visited = set()
    queue = collections.deque()
    queue.append((start, 0))
    distances = [[None for _ in range(cols)] for _ in range(rows)]

    # find distances from center to all the cells inside single grid
    while queue:
        position, distance = queue.popleft()

        if position in visited:
            continue

        visited.add(position)
        row, col = position
        distances[row][col] = distance

        candidates = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
        ]
        for candidate in candidates:
            if candidate[0] < 0 or candidate[0] >= rows:
                continue
            if candidate[1] < 0 or candidate[1] >= cols:
                continue
            if field[candidate[0]][candidate[1]] != '.':
                continue
            if candidate not in visited:
                queue.append((candidate, distance + 1))

    def count(predicate):
        result = 0
        for row in range(rows):
            for col in range(cols):
                if distances[row][col] is None:
                    continue
                if predicate(distances[row][col]):
                    result += 1
        return result

    # total steps count is 26501365
    # which is 65 + 202300 * 131
    odd = count(lambda d: d % 2 == 1)
    even = count(lambda d: d % 2 == 0)

    odd_corners = count(lambda d: d > 65 and d % 2 == 1)
    even_corners = count(lambda d: d > 65 and d % 2 == 0)

    k = 202300
    print((k + 1) ** 2 * odd + k ** 2 * even - (k + 1) * odd_corners + k * even_corners)
