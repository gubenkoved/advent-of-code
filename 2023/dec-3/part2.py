import collections

if __name__ == '__main__':
    field = []
    with open('data.txt', 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            field.append(line.strip())

    def get(r, c):
        if r >= 0 and r < len(field) and c >= 0 and c < len(field[r]):
            return field[r][c]
        return '.'

    # map from symbol coordinates to adjacent part numbers
    symbol_to_part_numbers = collections.defaultdict(list)

    # process single part number
    def process(r, c):
        coordinates = set()
        coordinates.add((r, c))
        part_num = get(r, c)

        while get(r, c + 1).isdigit():
            c += 1
            coordinates.add((r, c))
            part_num += get(r, c)

        part_num = int(part_num)

        # now we have all part number coordinates, check adjacent
        adjacent = set()

        for r, c in coordinates:
            adjacent.add((r - 1, c - 1))
            adjacent.add((r - 1, c))
            adjacent.add((r - 1, c + 1))

            adjacent.add((r, c - 1))
            adjacent.add((r, c))
            adjacent.add((r, c + 1))

            adjacent.add((r + 1, c - 1))
            adjacent.add((r + 1, c))
            adjacent.add((r + 1, c + 1))

        for r, c in adjacent:
            if (r, c) in coordinates:
                # does not really matter for us
                continue
            char = get(r, c)

            if not char.isdigit() and char != '.':
                symbol_to_part_numbers[(r, c)].append(part_num)


    # process the field line by line
    for row in range(len(field)):
        for col in range(len(field[row])):
            if field[row][col].isdigit() and not get(row, col - 1).isdigit():
                # process every first digit to avoid double count
                process(row, col)

    # find gears
    result = 0
    for _, part_numbers in symbol_to_part_numbers.items():
        if len(part_numbers) == 2:
            result += part_numbers[0] * part_numbers[1]
    print(result)
