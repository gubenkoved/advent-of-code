import collections

f = open('data.txt', 'r')
field = [line.strip() for line in f.readlines()]

rows, cols = len(field), len(field[0])

directions = []
for dx in range(-1, 2):
    for dy in range(-1, 2):
        directions.append((dx, dy))

def is_found(x, y, direction, word):
    if not word:
        return True

    if x < 0 or x >= rows:
        return False

    if y < 0 or y >= cols:
        return False

    if field[x][y] != word[0]:
        return False

    dx, dy = direction

    return is_found(x + dx, y + dy, direction, word[1:])

counter = 0
for x in range(rows):
    for y in range(cols):
        for direction in directions:
            if is_found(x, y, direction, 'XMAS'):
                counter += 1
print(counter)

# part 2
directions = []
for dx in [-1, 1]:
    for dy in [-1, 1]:
        directions.append((dx, dy))
centers_counter = collections.defaultdict(int)
for x in range(rows):
    for y in range(cols):
        for direction in directions:
            if is_found(x, y, direction, 'MAS'):
                dx, dy = direction
                center = x + dx, y + dy
                centers_counter[center] += 1
print(sum(1 for center in centers_counter if centers_counter[center] == 2))
