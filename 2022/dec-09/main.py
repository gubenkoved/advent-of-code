moves = []

with open('data.txt', 'r') as file:
    while True:
        line = file.readline()

        if not line:
            break

        d, c = line.strip().split(' ')
        moves.append((d, int(c)))


h = (0, 0)
t = h

visited = set()
visited.add(t)

def add(p, delta):
    return p[0] + delta[0], p[1] + delta[1]

m = {
    'U': (-1, 0),
    'D': (+1, 0),
    'L': (0, -1),
    'R': (0, +1),
}

for d, c in moves:
    for _ in range(c):
        hp = h  # record previous position
        h = add(h, m[d])

        # check if we need to move the tail
        if abs(h[0] - t[0]) > 1 or abs(h[1] - t[1]) > 1:
            t = hp
            visited.add(t)

print(len(visited))
