import copy

if __name__ == '__main__':
    field = []

    with open('data.txt', 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            field.append(list(line.strip('\n')))

    rows, cols = len(field), len(field[0])

    # falling logic
    def fall(delta_row, delta_col):
        rows_iterable = range(rows) if delta_row <= 0 else range(rows - 1, -1, -1)
        cols_iterable = range(cols) if delta_col <= 0 else range(cols - 1, -1, -1)
        for col in cols_iterable:
            for row in rows_iterable:
                if field[row][col] == 'O':
                    # fall until we reach "#" or end of the board!
                    cur_row, cur_col = row, col
                    while True:
                        fall_row, fall_col = cur_row + delta_row, cur_col + delta_col
                        if fall_row < 0 or fall_row >= rows:
                            break
                        if fall_col < 0 or fall_col >= cols:
                            break
                        if field[fall_row][fall_col] != '.':
                            break
                        field[cur_row][cur_col] = '.'
                        field[fall_row][fall_col] = 'O'
                        cur_row, cur_col = fall_row, fall_col

    states = []
    round_idx = 0
    cycle_len = None

    def do_round():
        fall(delta_row=-1, delta_col=0)  # north
        fall(delta_row=0, delta_col=-1)  # west
        fall(delta_row=+1, delta_col=0)  # south
        fall(delta_row=0, delta_col=+1)  # east

    states.append(copy.deepcopy(field))

    while True:
        round_idx += 1

        print('Calculating round #%d...' % round_idx)
        do_round()

        if field in states:
            same_field_at = states.index(field)
            cycle_len = round_idx - same_field_at
            print('cycle found! len is %d' % cycle_len)
            break

        states.append(copy.deepcopy(field))

    target_cycle_count = 1000000000

    # subtract performed rounds
    target_cycle_count -= round_idx

    # fast-forward given cycle
    target_cycle_count = target_cycle_count % cycle_len

    print('calculating leftover %d rounds...' % target_cycle_count)

    # make leftover rounds
    for _ in range(target_cycle_count):
        do_round()

    # count load
    load = 0
    for row in range(rows):
        for col in range(cols):
            if field[row][col] == 'O':
                load += rows - row

    print(load)
