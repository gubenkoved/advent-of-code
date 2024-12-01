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
    for col in range(cols):
        # process whole column
        fall_to_row = 0
        stone_count = 0
        for row in range(rows):
            if field[row][col] == 'O':
                stone_count += 1
                field[row][col] = '.'  # will fall
            if field[row][col] == '#' or row == rows - 1:
                # falling logic
                for row2 in range(fall_to_row, fall_to_row + stone_count):
                    field[row2][col] = 'O'
                stone_count = 0
                fall_to_row = row + 1

    with open('data.out', 'w') as f:
        for row in range(rows):
            f.write(''.join(field[row]) + '\n')

    # count
    load = 0
    for row in range(rows):
        for col in range(cols):
            if field[row][col] == 'O':
                load += rows - row

    print(load)
