import re
import functools

field = []

with open('data.txt', 'r') as f:
    while True:
        line = f.readline()

        if not line:
            break

        line = line.rstrip()

        if not line:
            break

        field.append(line)

    path = f.readline()

# pos and direction are (row, col)
pos = None
direction = (0, +1)

for col in range(len(field[0])):
    if field[0][col] != ' ':
        pos = (0, col)
        break


def add(pos, direction):
    return pos[0] + direction[0], pos[1] + direction[1]


def parse_path(path):
    # use capturing parenthesis so that delimiters are preserved as well
    return re.split('([LR])', path)

parsed_path = parse_path(path)

clockwise = {
    (+1, 0): (0, -1),
    (0, -1): (-1, 0),
    (-1, 0): (0, +1),
    (0, +1): (+1, 0),
}

counter_clockwise = {
    (+1, 0): (0, +1),
    (0, +1): (-1, 0),
    (-1, 0): (0, -1),
    (0, -1): (+1, 0),
}

def opposite(direction):
    return direction[0] * -1, direction[1] * -1

def is_in_field(pos):
    row, col = pos

    if row < 0 or row >= len(field):
        return False

    if col < 0 or col >= len(field[row]):
        return False

    if field[row][col] == ' ':
        return False

    return True


@functools.cache
def last_cell(pos, direction):
    while True:
        new_pos = add(pos, direction)
        if not is_in_field(new_pos):
            break
        pos = new_pos
    return pos


SQUARE_SIZE = 50


def to_square_coordinate(row, col):
    return row // SQUARE_SIZE, col // SQUARE_SIZE

def to_minimap():
    field_rows, field_cols = len(field), len(field[0])
    minimap = [
        [' ' for _ in range(field_cols // SQUARE_SIZE)]
        for _ in range(field_rows // SQUARE_SIZE)
    ]

    for mr in range(len(minimap)):
        for mc in range(len(minimap[mr])):
            row, col = mr * SQUARE_SIZE, mc * SQUARE_SIZE
            if is_in_field((row, col)):
                minimap[mr][mc] = 'x'

    return minimap


minimap = to_minimap()

print('minimap: ')
for row in minimap:
    print(''.join(row))

# each "edge" of the cube on the 2D can be encoded by two coordinates
# which correspond to the two edge points encoded as a coordinates of
# top left corner of the point
# for example, here is the one of the cube representation in 2D
# 012
#  x  0
# xxx 1
#  x  2
#  x  3
#     4
# first edge is the top one has coordinates ((0,1), (0, 2))
# the left edge of that same cell is ((0, 1), (1, 1))
# the right edge is ((0, 2), (1, 2))


# a map from a 2d coordinate on a minimap to the 3d coordinate on the
# corresponding cube



def solve_for_3d():
    # find _some_ square we start from, and we will pretend that it lies at
    # some plane, we will use the top left populated cell and z=0 plane, just
    # to pick something (it should not really matter)
    first_pos = None

    for r in range(len(minimap)):
        for c in range(len(minimap[r])):
            if minimap[r][c] == 'x':
                first_pos = (r, c)
                break
        if first_pos is not None:
            break

    assert first_pos is not None

    r, c = first_pos

    to_3d_map = {}

    to_3d_map[(r, c)] = (0, 0, 0)
    to_3d_map[(r, c + 1)] = (1, 0, 0)
    to_3d_map[(r + 1, c)] = (0, 1, 0)
    to_3d_map[(r + 1, c + 1)] = (1, 1, 0)

    def flip(point, axis):
        point = list(point)
        point[axis] = 1 if point[axis] == 0 else 0
        return tuple(point)

    def find_axis(edge1, edge2):
        points_2d = edge1 + edge2
        points_3d = [to_3d_map[p2d] for p2d in points_2d]
        for axis in range(3):
            if len(set(p[axis] for p in points_3d)) == 1:
                return axis
        assert False, 'bad'

    def gen_all_edges():
        edges = []
        for r in range(len(minimap)):
            for c in range(len(minimap[r])):
                if minimap[r][c] == 'x':
                    edges.append(((r, c), (r, c + 1)))
                    edges.append(((r, c), (r + 1, c)))
                    edges.append(((r, c + 1), (r + 1, c + 1)))
                    edges.append(((r + 1, c), (r + 1, c + 1)))
        return edges

    def edge_on_map(edge):
        return edge in gen_all_edges()

    def translate_edge(edge, delta):
        p1, p2 = edge
        return add(p1, delta), add(p2, delta)

    # FIXME: instead of jumping by edges, jump by squares resolving all
    #  unresolved edges in each square, trace previous square top level point
    #  and axis

    r, c = first_pos
    first_right_edge = (r, c + 1), (r + 1, c + 1)
    first_down_edge = (r + 1, c), (r + 1, c + 1)

    # (parent_edge, edge, parent_axis) tuples
    queue = [
        (first_right_edge, translate_edge(first_right_edge, (0, +1)), 2),
        (first_down_edge, translate_edge(first_down_edge, (+1, 0)), 2),
    ]

    visited = set([
        first_right_edge,
        first_down_edge,
    ])

    while queue:
        parent_edge, edge, parent_axis = queue.pop(0)

        if edge in visited:
            continue

        visited.add(edge)

        # solve for current values
        p1, p2 = edge
        p1_parent, p2_parent = parent_edge

        p1_3d = flip(to_3d_map[p1_parent], parent_axis)
        p2_3d = flip(to_3d_map[p2_parent], parent_axis)

        if p1 in to_3d_map:
            assert p1_3d == to_3d_map[p1]

        if p2 in to_3d_map:
            assert p2_3d == to_3d_map[p2]

        to_3d_map[p1] = p1_3d
        to_3d_map[p2] = p2_3d

        # find axis in which new plane sits
        axis = find_axis(edge, parent_edge)

        neighbor_edges = [
            translate_edge(edge, (+1, 0)),  # down
            translate_edge(edge, (0, -1)),  # left
            translate_edge(edge, (0, +1)),  # right
            # there should neven be need to go up consider valid cube representations
            # but still, for symmetry
            translate_edge(edge, (-1, 0)),  # up
        ]

        for neighbor_edge in neighbor_edges:
            if not edge_on_map(neighbor_edge):
                continue

            queue.append(
                (edge, neighbor_edge, axis)
            )

    # sanity check
    for x in range(2):
        for y in range(2):
            for z in range(2):
                assert (x, y, z) in to_3d_map.values()

    return to_3d_map


# TODO: given 3d mapping find the edge we arriving to using the equality of
#  3d coordinates, there should be exactly one such edge;
#  then interpolate the position on it using the source position
#  calculate 2D direction always being from the outside to inside in 2D
@functools.cache
def resolve(pos, direction):
    next_pos = add(pos, direction)

    if not is_in_field(next_pos):
        next_pos = last_cell(pos, opposite(direction))

    return next_pos

def at(pos):
    return field[pos[0]][pos[1]]


def step(pos, direction):
    next_pos = resolve(pos, direction)

    if at(next_pos) == '.':
        return next_pos
    elif at(next_pos) == '#':
        # unable to move
        return pos
    else:
        assert 'where the hell we are?'


if __name__ == '__main__':
    minimap_to_3d_map = solve_for_3d()

    for move in parsed_path:
        if move == 'L':
            direction = counter_clockwise[direction]
        elif move == 'R':
            direction = clockwise[direction]
        else:
            units = int(move)
            for _ in range(units):
                pos = step(pos, direction)

    print(pos)
    print(direction)

    # Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^).
    direction_cost = {
        (0, +1): 0,
        (+1, 0): 1,
        (0, -1): 2,
        (-1, 0): 3,
    }

    print((pos[0] + 1) * 1000 + ((1 + pos[1]) * 4) + direction_cost[direction])
