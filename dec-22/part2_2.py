import copy

blocks = []


def parse_block(s):
    start, end = s.split('~')
    return [
        [int(x) for x in start.split(',')],
        [int(x) for x in end.split(',')],
    ]


with open('data.txt', 'r') as f:
    while True:
        line = f.readline()
        if not line:
            break
        blocks.append(parse_block(line.strip()))


def simulate(blocks):
    def compute_fill_index():
        max_x, max_y, max_z = 0, 0, 0
        for block in blocks:
            max_x = max(max_x, block[1][0])
            max_y = max(max_y, block[1][1])
            max_z = max(max_z, block[1][2])
        index = [
            [
                [
                    0 for _ in range(max_z + 1)
                ] for _ in range(max_y + 1)
            ] for _ in range(max_x + 1)
        ]
        for block in blocks:
            for x in range(block[0][0], block[1][0] + 1):
                for y in range(block[0][1], block[1][1] + 1):
                    for z in range(block[0][2], block[1][2] + 1):
                        index[x][y][z] = 1
        return index

    fill_index = compute_fill_index()
    moved_ids = set()
    round_idx = 0

    while True:
        round_idx += 1
        should_continue = False

        for block_idx in range(len(blocks)):
            block = blocks[block_idx]
            can_move_down = True
            for x in range(block[0][0], block[1][0] + 1):
                for y in range(block[0][1], block[1][1] + 1):
                    if block[0][2] == 1:
                        can_move_down = False
                        break
                    if fill_index[x][y][block[0][2] - 1] != 0:
                        can_move_down = False
                        break

            if can_move_down:
                should_continue = True  # continue calculations as block moved
                moved_ids.add(block_idx)

                # update fill idx
                for x in range(block[0][0], block[1][0] + 1):
                    for y in range(block[0][1], block[1][1] + 1):
                        # lower layer
                        assert fill_index[x][y][block[0][2] - 1] == 0
                        fill_index[x][y][block[0][2] - 1] = 1
                        # top layer
                        assert fill_index[x][y][block[0][2]] == 1
                        fill_index[x][y][block[1][2]] = 0

                # update block z-coordinates
                block[0][2] -= 1
                block[1][2] -= 1

        if not should_continue:
            break

    return moved_ids

# order block so that "lower" ones are processed first
print('ordering blocks...')
blocks.sort(key=lambda block: block[1][2])

print('initial simulation...')
simulate(blocks)

# no further movement!
print('check no movement')
moved_block_ids = simulate(blocks)
assert not moved_block_ids

# now try all blocks and see if there is any movement
print('simulating blocks removal...')
total_moved_count = 0
for block_idx in range(len(blocks)):
    new_blocks = copy.deepcopy(blocks)
    new_blocks = new_blocks[:block_idx] + new_blocks[block_idx+1:]

    # we need to simulate up to two passes given block processing order is
    # by z axis from bottom plane upwards
    moved_block_ids = simulate(new_blocks)

    print('checked block %d -> moved %d blocks after removal' % (
        block_idx, len(moved_block_ids)))
    total_moved_count += len(moved_block_ids)

print('total moved count is %d blocks' % total_moved_count)
