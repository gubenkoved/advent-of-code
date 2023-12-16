if __name__ == '__main__':
    field = []

    with open('data.txt', 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            field.append(line.rstrip('\n'))

    # compute light
    processed = set()
    current = [
        ((0, -1), 1),  # start condition
    ]
    energized_tiles = set()  # positions of energized tiles

    # piece of light we process is encoded by a tuple (location, direction)
    # where direction could be a number from 0 to 4
    # we do not want to process same piece of light flowing in the same direction
    # twice in order to be computationally efficient and avoid loops

    def get_next_position(cur_position, direction):
        if direction == 0:  # up
            return (cur_position[0] - 1, cur_position[1])
        elif direction == 1:  # right
            return (cur_position[0], cur_position[1] + 1)
        elif direction == 2:  # down
            return (cur_position[0] + 1, cur_position[1])
        elif direction == 3:  # left
            return (cur_position[0], cur_position[1] - 1)

    mirror_signs = ('-', '|', '/', '\\')
    rows, cols = len(field), len(field[0])
    horizontal_directions = (1, 3)
    vertical_directions = (0, 2)

    while current:
        position, direction = current.pop(-1)

        if (position, direction) in processed:
            continue

        next_position = get_next_position(position, direction)

        if (next_position[0] < 0 or next_position[0] >= rows or
                next_position[1] < 0 or next_position[1] >= cols):
            continue  # disappear

        energized_tiles.add(next_position)

        next_cell = field[next_position[0]][next_position[1]]

        if next_cell in mirror_signs:
            if next_cell == '|':
                if direction in horizontal_directions:
                    current.append((next_position, 0))
                    current.append((next_position, 2))
                else:
                    current.append((next_position, direction))
            elif next_cell == '-':
                if direction in vertical_directions:
                    current.append((next_position, 3))
                    current.append((next_position, 1))
                else:
                    current.append((next_position, direction))
            elif next_cell == '\\':
                next_direction = {
                    0: 3,  # if we were going up, then we will go left
                    1: 2,  # right -> down
                    2: 1,  # down -> right
                    3: 0,  # left -> up
                }[direction]
                current.append(((next_position[0], next_position[1]), next_direction))
            elif next_cell == '/':
                next_direction = {
                    0: 1,
                    1: 0,
                    2: 3,
                    3: 2,
                }[direction]
                current.append(((next_position[0], next_position[1]), next_direction))
            else:
                assert False, 'unhandled'
        else:  # no mirror
            # continue in the same direction
            current.append((next_position, direction))

        # mark as processed
        processed.add((position, direction))

    with open('data.out', 'w') as f:
        for row in range(rows):
            for col in range(cols):
                cell = field[row][col]
                if (row, col) in energized_tiles:
                    cell = '#'
                print(cell, end='', file=f)
            print(file=f)

    print(len(energized_tiles))
