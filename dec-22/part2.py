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


# simulates block falling one step, returns True if anything has changed
def simulate_step(blocks):
    def is_inside_block(block, x, y, z):
        return (
                block[0][0] <= x <= block[1][0] and
                block[0][1] <= y <= block[1][1] and
                block[0][2] <= z <= block[1][2]
        )

    def is_free(x, y, z):
        # hugely not efficient, but should work for part 1 at least,
        # alternatively we can just precalculate 3D array marking all
        # occupied cells and updating as we go
        for block in blocks:
            if is_inside_block(block, x, y, z):
                return False
        return True

    moved_ids = set()
    for block_idx in range(len(blocks)):
        block = blocks[block_idx]
        can_move_down = True
        for x in range(block[0][0], block[1][0] + 1):
            for y in range(block[0][1], block[1][1] + 1):
                if block[0][2] == 1:
                    can_move_down = False
                    break
                if not is_free(x, y, block[0][2] - 1):
                    can_move_down = False
                    break
        if can_move_down:
            block[0][2] -= 1
            block[1][2] -= 1
            moved_ids.add(block_idx)

    return moved_ids

# order block so that "lower" ones are processed first
print('ordering blocks...')
blocks.sort(key=lambda block: block[1][2])

print('initial simulation...')
step = 0
while True:
    step += 1
    moved = simulate_step(blocks)
    print('.', end='')
    if not moved:
        break
print('\ninitial simulation took %d steps' % step)

# now try all blocks and see if there is any movement
print('simulating blocks removal...')
total_moved_count = 0
for block_idx in range(len(blocks)):
    print('checking block #%d' % block_idx)
    new_blocks = copy.deepcopy(blocks)
    new_blocks = new_blocks[:block_idx] + new_blocks[block_idx+1:]

    # we need to simulate up to two passes given block processing order is
    # by z axis from bottom plane upwards
    moved_block_ids = set()
    moved_block_ids.update(simulate_step(new_blocks))
    moved_block_ids.update(simulate_step(new_blocks))

    print('  moved %d blocks' % len(moved_block_ids))
    total_moved_count += len(moved_block_ids)

print('total moved count is %d blocks' % total_moved_count)
