file = open('data.txt', 'r')
field = [[int(x) for x in l.strip()] for l in file.readlines()]
rows, cols = len(field), len(field[0])

def score(r, c):
    if field[r][c] != 0:
        return 0

    # main tracer function
    def heads(r, c, v):
        if r < 0 or r >= rows:
            return set()
        if c < 0 or c >= cols:
            return set()

        if field[r][c] != v:
            return set()

        if v == 9:
            return {(r, c)}

        neighbors = [
            (r-1, c),
            (r+1, c),
            (r, c-1),
            (r, c+1)
        ]
        result = set()
        for r2, c2 in neighbors:
            result.update(heads(r2, c2, v + 1))
        return result

    return len(heads(r, c, 0))


print(sum(score(r, c) for r in range(rows) for c in range(cols)))