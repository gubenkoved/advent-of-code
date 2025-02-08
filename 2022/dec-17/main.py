import typing
from typing import Tuple, List

with open('data.txt', 'r') as file:
    arrows = file.readline().strip()

rocks = [
    [
        '####',
    ],
    [
        ' # ',
        '###',
        ' # ',
    ],
    [
        '  #',
        '  #',
        '###',
    ],
    [
        '#',
        '#',
        '#',
        '#',
    ],
    [
        '##',
        '##',
    ]
]

# rows of chamber starting from the bottom
width = 7
chamber = []
highest_rock_row = -1

Rock: typing.TypeAlias = List[str]
Vector: typing.TypeAlias = Tuple[int, int]


# each rock appears so that its left edge is two units away from the left
# wall and its bottom edge is three units above the highest rock in the room
# (or the floor, if there isn't one).
def new_rock(rock_num) -> Tuple[Rock, Vector]:
    rock = rocks[rock_num]

    chamber_height = highest_rock_row + 4 + len(rock)

    # extend the chamber
    while len(chamber) < chamber_height:
        chamber.append([' ' for _ in range(width)])

    return rock, (chamber_height - 1, 2)


# moves given rock with given position of the top left corner in a given
# direction (position delta), returns new position;
# new position can be equal to the source position if the rock is stuck
def move(rock, pos: Vector, direction: Vector) -> Vector:
    offset_row, offset_col = pos
    dir_row, dir_col = direction

    stuck = False
    for r in range(len(rock)):
        for c in range(len(rock[0])):
            if rock[r][c] != '#':
                continue
            chamber_row = offset_row + dir_row - r
            chamber_col = offset_col + dir_col + c

            if chamber_row < 0:
                stuck = True
            elif chamber_col < 0 or chamber_col >= width:
                stuck = True
            elif chamber[chamber_row][chamber_col] == '#':
                stuck = True

    if stuck:
        return pos

    # not stuck -> return updated position
    return pos[0] + dir_row, pos[1] + dir_col


def put_rock(rock, pos: Vector):
    offset_row, offset_col = pos
    for r in range(len(rock)):
        for c in range(len(rock[0])):
            if rock[r][c] != '#':
                continue
            chamber_row = offset_row - r
            chamber_col = offset_col + c
            assert chamber[chamber_row][chamber_col] == ' '
            chamber[chamber_row][chamber_col] = '#'


def print_chamber():
    for row in range(len(chamber) - 1, -1, -1):
        for col in range(len(chamber[row])):
            print(chamber[row][col], end='')
        print()


arrows_to_direction = {
    '<': (0, -1),
    '>': (0, +1),
}

rock_idx = 0
arrow_idx = 0


for _ in range(2022):
    rock, rock_pos = new_rock(rock_idx % len(rocks))
    rock_idx += 1

    rock_stuck = False
    while True:
        arrow = arrows[arrow_idx % len(arrows)]
        arrow_idx += 1
        rock_pos = move(rock, rock_pos, arrows_to_direction[arrow])

        # try fall down
        new_rock_pos = move(rock, rock_pos, (-1, 0))
        rock_stuck = rock_pos == new_rock_pos
        rock_pos = new_rock_pos

        if rock_stuck:
            print('rock %d stuck' % rock_idx)
            break

    # carry over rock to the chamber
    put_rock(rock, rock_pos)

    highest_rock_row = max(highest_rock_row, rock_pos[0])


print_chamber()
print('highest rock: %d' % (highest_rock_row + 1))
