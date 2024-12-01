# in this case part 2 is a task in of its own, I will run it against the
# output of the part 1 to decouple them
# NOTE: I replaced "S" manually to corresponding char

if __name__ == '__main__':
    field = []
    with open('data.out', 'r') as f:
        while True:
            line = f.readline()

            if not line:
                break

            field.append(list(line.strip('\n')))

    # for each empty cell calculate if it is inside or outside the loop
    # similarly how it is done in geometry we can start at some point and
    # make a virtual line in any direction (say to the right) and count how many
    # times we crossed the loop, if we crossed it odd number of times, we are inside!

    inside_count = 0
    rows, cols = len(field), len(field[0])

    insiders = set()

    for row in range(rows):
        for col in range(cols):
            if field[row][col] != '.':
                continue

            cross_count = 0
            for col2 in range(col + 1, cols):
                # refer to excalidraw picture -- it corresponds to
                # virtual ray sent above the point at the edge
                if field[row][col2] in {'|', 'L', 'J'}:
                    cross_count += 1

            if cross_count % 2 == 1:
                insiders.add((row, col))
                inside_count += 1

    # print the result
    with open('data.out2', 'w') as f:
        for row in range(rows):
            for col in range(cols):
                if field[row][col] == '.':
                    if (row, col) in insiders:
                        print('I', end='', file=f)
                    else:
                        print('.', end='', file=f)
                else:
                    print(field[row][col], end='', file=f)
            print(file=f)

    print('inside count: %d' % inside_count)
