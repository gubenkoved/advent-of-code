import plotly.express as px


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
    layer = [start]
    step = 0

    def at(r, c):
        return field[r % rows][c % cols]

    odd_dist_count, even_dist_count = 0, 0
    reachable = []

    while step < 1000:
        next_layer = []
        for position in layer:
            if position in visited:
                continue
            visited.add(position)

            if step % 2 == 0:
                even_dist_count += 1
            else:
                odd_dist_count += 1

            row, col = position
            candidates = [
                (row - 1, col),
                (row + 1, col),
                (row, col - 1),
                (row, col + 1),
            ]
            for candidate in candidates:
                if at(*candidate) != '.':
                    continue
                if candidate not in visited:
                    next_layer.append(candidate)

        layer = next_layer
        if step % 65 == 0:
            print('step %6d visited %10d [%-10d+%10d]' % (
                step, len(visited), odd_dist_count, even_dist_count))

        if step % 2 == 0:
            reachable.append({
                'step': step,
                'count': even_dist_count
            })
        else:
            reachable.append({
                'step': step,
                'count': odd_dist_count
            })
        step += 1

    fig = px.line(
        y=[p['count'] for p in reachable],
        x=[p['step'] for p in reachable],
        markers=False,
    )
    # fig.write_html('vis.html')
    fig.show()
