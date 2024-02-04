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
def simulate_step(blocks, detect_movement_only=False):
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

    moved = False
    for block in blocks:
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
            moved = True

            if detect_movement_only:
                return True

    return moved


print('initial simulation...')
step = 0
while True:
    step += 1
    moved = simulate_step(blocks)
    if not moved:
        print('.', end='')
        break
print('initial simulation took %d steps' % step)

# now try all blocks and see if there is any movement
print('simulating blocks removal...')
can_remove = 0
for block_idx in range(len(blocks)):
    print('checking block #%d' % block_idx)
    new_blocks = copy.deepcopy(blocks)
    new_blocks = new_blocks[:block_idx] + new_blocks[block_idx+1:]
    if not simulate_step(new_blocks, detect_movement_only=True):
        can_remove += 1

print('can remove %d blocks' % can_remove)
