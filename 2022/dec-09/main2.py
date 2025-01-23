import os

moves = []

with open('data.txt', 'r') as file:
    while True:
        line = file.readline()

        if not line:
            break

        d, c = line.strip().split(' ')
        moves.append((d, int(c)))


rope = []

for _ in range(10):
    rope.append((0, 0))

visited = set()
visited.add(rope[-1])

def add(p, delta):
    return p[0] + delta[0], p[1] + delta[1]

m = {
    'U': (-1, 0),
    'D': (+1, 0),
    'L': (0, -1),
    'R': (0, +1),
}

frame_idx = 0

def save():
    global frame_idx

    path = 'out/step_%d.txt' % frame_idx
    frame_idx += 1

    min_row = min(p[0] for p in rope)
    max_row = max(p[0] for p in rope)
    min_col = min(p[1] for p in rope)
    max_col = max(p[1] for p in rope)

    os.makedirs('out', exist_ok=True)
    with open(path, 'w') as file:
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                for idx in range(len(rope)):
                    if rope[idx] == (r, c):
                        file.write(str(idx))
                        break
                else:
                    file.write('.')
            file.write('\n')

for d, c in moves:
    for _ in range(c):
        # move head of the rope in a given direction
        rope[0] = add(rope[0], m[d])

        # save()

        # ... and now move all other knots if needed
        for idx in range(1, len(rope)):
            cur_knot = rope[idx]
            prev_knot = rope[idx - 1]
            dr = prev_knot[0] - cur_knot[0]
            dc = prev_knot[1] - cur_knot[1]
            if abs(dr) > 1 or abs(dc) > 1:
                # move this knot as well
                cur_d = (dr // abs(dr) if dr else 0, dc // abs(dc) if dc else 0)
                rope[idx] = add(rope[idx], cur_d)
            else:
                # no further movement possible as well
                break

        visited.add(rope[-1])

    # save()

print(len(visited))
