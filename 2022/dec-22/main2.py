import re
import functools
import typing

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


Point2D = tuple[int, int]
Vector2D = Point2D
Point3D = tuple[int, int, int]
Edge2D = tuple[Point2D, Point2D]
Edge3D = tuple[Point3D, Point3D]


N = SQUARE_SIZE = 50


# pos and direction are (row, col)
pos = None
direction = (0, +1)

for col in range(len(field[0])):
    if field[0][col] != ' ':
        pos = (0, col)
        break


def add(pos: Point2D, direction: Vector2D):
    return pos[0] + direction[0], pos[1] + direction[1]


@typing.overload
def subtract(a: Point2D, b: Vector2D) -> Point2D:
    ...


def subtract(a: Point2D, b: Point2D) -> Vector2D:
    return a[0] - b[0], a[1] - b[1]


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


def is_in_field(pos: Point2D) -> bool:
    row, col = pos

    if row < 0 or row >= len(field):
        return False

    if col < 0 or col >= len(field[row]):
        return False

    if field[row][col] == ' ':
        return False

    return True


def to_minimap():
    field_rows, field_cols = len(field), max(len(field[r]) for r in range(len(field)))
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


def flip(point: Point3D, axis: int) -> Point3D:
    point = list(point)
    point[axis] = 1 if point[axis] == 0 else 0
    return tuple(point)

def find_plane_axis(vertices_3d: list[Point3D]) -> int:
    """
    Return axis (index) for which all the coordinates are the same for
    given points (specified in 2d)
    """
    for axis in range(3):
        if len(set(p[axis] for p in vertices_3d)) == 1:
            return axis
    assert False, 'unable to find plane for this points'

def edges_of(pos: Point2D) -> list[Edge2D]:
    r, c = pos
    return [
        ((r, c), (r, c + 1)),
        ((r, c), (r + 1, c)),
        ((r, c + 1), (r + 1, c + 1)),
        ((r + 1, c), (r + 1, c + 1)),
    ]

def vertices_of_square(pos: Point2D) -> list[Point2D]:
    r, c = pos
    return [
        (r, c),
        (r, c + 1),
        (r + 1, c),
        (r + 1, c + 1),
    ]


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

    to_3d_map = {}

    def plane_axis_for_square(pos: Point2D):
        points_2d = vertices_of_square(pos)
        points_3d = [to_3d_map[p2d] for p2d in points_2d]
        return find_plane_axis(points_3d)

    def is_on_minimap(pos: Point2D) -> bool:
        r, c = pos
        if r < 0 or r >= len(minimap):
            return False
        if c < 0 or c >= len(minimap[r]):
            return False
        return True

    r, c = first_pos

    to_3d_map[(r, c)] = (0, 0, 0)
    to_3d_map[(r, c + 1)] = (1, 0, 0)
    to_3d_map[(r + 1, c)] = (0, 1, 0)
    to_3d_map[(r + 1, c + 1)] = (1, 1, 0)

    # start with first square, and then traverse to all other ones, every time
    # resolving the position in 3d space for all the vertices;
    # on each jump there will be only two unresolved vertices if square was not
    # yet visited;
    queue = [
        # square position to handle, parent position
        (first_pos, None),
    ]

    visited = set()

    while queue:
        pos, parent_pos = queue.pop(0)

        if pos in visited:
            continue

        visited.add(pos)

        resolved_vertices = []
        unresolved_vertices = []
        for vr, vc in vertices_of_square(pos):
            if (vr, vc) in to_3d_map:
                resolved_vertices.append((vr, vc))
            else:
                unresolved_vertices.append((vr, vc))

        if unresolved_vertices:
            assert len(unresolved_vertices) == 2
            parent_axis = plane_axis_for_square(parent_pos)

            # copy 3d coordinates from the resolved edge, and flip the coordinate
            # which was axis plane for the parent square!
            from_parent_vector = subtract(pos, parent_pos)
            for to_resolve in unresolved_vertices:
                source_pos = subtract(to_resolve, from_parent_vector)
                assert source_pos in to_3d_map
                to_3d_map[to_resolve] = flip(to_3d_map[source_pos], parent_axis)

        # go to the neighbors
        r, c = pos
        neighbors = [
            (r - 1, c),
            (r + 1, c),
            (r, c - 1),
            (r, c + 1),
        ]
        for nr, nc in neighbors:
            if not is_on_minimap((nr, nc)):
                continue
            if minimap[nr][nc] != 'x':
                continue
            npos = (nr, nc)
            queue.append((npos, pos))

    # sanity check
    for x in range(2):
        for y in range(2):
            for z in range(2):
                assert (x, y, z) in to_3d_map.values()

    return to_3d_map


@typing.overload
def reversed_edge(edge: Edge3D) -> Edge3D:
    ...


def reversed_edge(edge: Edge2D) -> Edge2D:
    return edge[1], edge[0]


def edge_2d_to_3d(edge: Edge2D) -> Edge3D:
    p1, p2 = edge
    return minimap_to_3d_map[p1], minimap_to_3d_map[p2]


def find_corresponding_edge_with_matching_3d(edge: Edge2D) -> Edge2D:
    target_edge_3d: Edge3D = edge_2d_to_3d(edge)

    for r in range(len(minimap)):
        for c in range(len(minimap[r])):
            if minimap[r][c] != 'x':
                continue
            for cur_edge in edges_of((r, c)):
                # skip the original one
                if cur_edge == edge or cur_edge == reversed_edge(edge):
                    continue
                cur_edge_3d = edge_2d_to_3d(cur_edge)
                if cur_edge_3d == target_edge_3d:
                    return cur_edge
                elif cur_edge_3d == reversed_edge(target_edge_3d):
                    return reversed_edge(cur_edge)

    assert False, 'unable to find'


@functools.cache
def is_point_on_line(point: Point2D, start: Point2D, end: Point2D) -> bool:
    assert start[0] == end[0] or start[1] == end[1]

    cur = start
    unit = unit_vec(subtract(end, start))
    while True:
        if cur == point:
            return True
        if cur == end:
            break
        cur = add(cur, unit)
    return False


@functools.cache
def find_edge_on_minimap(pos: Point2D, direction: Vector2D) -> Edge2D:
    # note that direction is required otherwise there is uncertainty
    is_direction_horizontal = direction[0] == 0

    for r in range(len(minimap)):
        for c in range(len(minimap[r])):
            if minimap[r][c] != 'x':
                continue

            if not is_direction_horizontal:
                # top edge
                if is_point_on_line(pos, (r * N, c * N), (r * N, (c + 1) * N - 1)):
                    return (r, c), (r, c + 1)

                # bottom edge
                if is_point_on_line(pos, ((r + 1) * N - 1, c * N), ((r + 1) * N - 1, (c + 1) * N - 1)):
                    return (r + 1, c), (r + 1, c + 1)

            if is_direction_horizontal:
                # left
                if is_point_on_line(pos, (r * N, c * N), ((r + 1) * N - 1, c * N)):
                    return (r, c), (r + 1, c)

                # right
                if is_point_on_line(pos, (r * N, (c + 1) * N - 1), ((r + 1) * N - 1, (c + 1) * N - 1)):
                    return (r, c + 1), (r + 1, c + 1)

    assert False, 'unable to find'


def is_horizontal(edge: Edge2D) -> bool:
    p1, p2 = edge
    if p1[0] == p2[0]:
        return True
    elif p1[1] == p2[1]:
        return False
    else:
        assert 'bad'


def unit_vec(vector: Vector2D) -> Vector2D:
    a, b = vector
    a = int(a / abs(a)) if a else 0
    b = int(b / abs(b)) if b else 0
    return a, b


def multiply_vec(vec: Vector2D, k: int) -> Vector2D:
    return vec[0] * k, vec[1] * k


def interpolate(start: Point2D, end: Point2D, offset: int) -> Point2D:
    unit = unit_vec(subtract(end, start))
    return add(start, multiply_vec(unit, offset))


def edge_to_points(edge: Edge2D) -> (Point2D, Point2D):
    """
    Given the edge on the field resolves it into the two positions on the
    field that both are part of the field. Note how the same edge always have
    two such possible resolutions (from the two sides of that edge).
    """
    p1, p2 = edge

    # wow, it is nasty... is there something better?
    if is_horizontal(edge):
        offset = (-1, 0)
        if p2[1] > p1[1]:
            p2 = add(p2, (0, -1))
        else:
            p1 = add(p1, (0, -1))
    else:
        offset = (0, -1)
        if p2[0] > p1[0]:
            p2 = add(p2, (-1, 0))
        else:
            p1 = add(p1, (-1, 0))

    if is_in_field(p1) and is_in_field(p2):
        return p1, p2
    else:
        p1, p2 = add(p1, offset), add(p2, offset)
        assert is_in_field(p1)
        assert is_in_field(p2)
        return p1, p2


def scale_point(point: Point2D, scale: int) -> Point2D:
    return point[0] * scale, point[1] * scale


def scale_edge(edge: Edge2D, factor: int) -> Edge2D:
    p1, p2 = edge
    return scale_point(p1, factor), scale_point(p2, factor)


def interpolate_position(
        field_pos: Point2D, direction: Vector2D,
        target_edge_minimap: Edge2D) -> Point2D:

    if direction[0] != 0:
        # we are going up/down
        offset = field_pos[1] % SQUARE_SIZE
    else:
        assert direction[1] != 0
        offset = field_pos[0] % SQUARE_SIZE

    target_edge = scale_edge(target_edge_minimap, SQUARE_SIZE)
    start, end = edge_to_points(target_edge)

    assert is_in_field(start)
    assert is_in_field(end)

    return interpolate(start, end, offset)


def all_directions() -> list[Vector2D]:
    return [
        (-1, 0),
        (+1, 0),
        (0, -1),
        (0, +1),
    ]


@functools.cache
def resolve(pos: Point2D, direction: Vector2D) -> (Point2D, Vector2D):
    next_pos = add(pos, direction)
    next_direction = direction

    if not is_in_field(next_pos):
        cur_edge = find_edge_on_minimap(pos, direction)
        target_edge = find_corresponding_edge_with_matching_3d(cur_edge)

        next_pos = interpolate_position(
            pos, direction, target_edge
        )

        assert is_in_field(next_pos)

        for d in all_directions():
            if not is_in_field(add(next_pos, d)):
                next_direction = multiply_vec(d, -1)
                break
        else:
            assert 'unable to figure out direction'

    assert next_pos is not None
    assert next_direction is not None

    return next_pos, next_direction


def at(pos: Point2D) -> str:
    return field[pos[0]][pos[1]]


def step(pos: Point2D, direction: Vector2D) -> (Point2D, Vector2D):
    next_pos, next_direction = resolve(pos, direction)

    assert next_pos is not None
    assert next_direction is not None

    assert is_in_field(next_pos)

    if at(next_pos) == '.':
        return next_pos, next_direction
    elif at(next_pos) == '#':
        # unable to move
        return pos, direction
    else:
        assert False, 'where the hell we are?'


# 17515 WA! too low
# 36340 WA! too low
# solves the sample though...
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
                pos, direction = step(pos, direction)

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
