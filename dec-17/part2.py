import heapq

if __name__ == '__main__':
    field = []
    with open('data.txt', 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            field.append([int(c) for c in line.strip('\n')])

    rows, cols = len(field), len(field[0])
    target = (rows - 1, cols - 1)

    # directions:
    # 0 - up, 1 - right, 2 - down, 3 - left

    def step_to(row, col, direction):
        if direction == 0:
            return row - 1, col
        elif direction == 1:
            return row, col + 1
        elif direction == 2:
            return row + 1, col
        elif direction == 3:
            return row, col - 1


    # minheap of (heat_loss, (row, col), direction, steps_in_direction)
    active = [
        (0, (0, 0), 1, 0),
        (0, (0, 0), 2, 0),
    ]

    # set of ((row, col), direction, steps_in_direction)
    visited = set()

    while active:
        heat_loss, (row, col), direction, steps_in_direction = heapq.heappop(active)

        visit_key = (row, col), direction, steps_in_direction
        if visit_key in visited:
            continue
        visited.add(visit_key)

        if (row, col) == target:
            print('Heat loss to target: %d' % heat_loss)
            break

        # list of ((row, col), direction, steps_in_direction) of reachable cells
        neighbors = []

        # compute neighbors
        if steps_in_direction < 10:
            # can continue going in the same direction
            neighbors.append(
                (step_to(row, col, direction), direction, steps_in_direction + 1)
            )

        # can turn left or right only if we already went for 4 blocks in that direction!
        if steps_in_direction >= 4:
            neighbors.append(
                (step_to(row, col, (direction + 1) % 4), (direction + 1) % 4, 1)
             )
            neighbors.append(
                (step_to(row, col, (direction + 3) % 4), (direction + 3) % 4, 1)
            )

        for (neighbor_row, neighbor_col), neighbor_direction, neighbor_steps_in_direction in neighbors:
            if neighbor_row < 0 or neighbor_row >= rows or neighbor_col < 0 or neighbor_col >= cols:
                continue

            handle = (
                heat_loss + field[neighbor_row][neighbor_col],
                (neighbor_row, neighbor_col),
                neighbor_direction,
                neighbor_steps_in_direction,
            )
            heapq.heappush(active, handle)
