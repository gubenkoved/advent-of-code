if __name__ == '__main__':
    field = []
    with open('data.txt', 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            field.append(line.strip())

    result = 0

    def get(r, c):
        if r >= 0 and r < len(field) and c >= 0 and c < len(field[r]):
            return field[r][c]
        return '.'

    # process single part number
    def process(r, c):
        global result

        coordinates = set()
        coordinates.add((r, c))
        part_num = get(r, c)

        while get(r, c + 1).isdigit():
            c += 1
            coordinates.add((r, c))
            part_num += get(r, c)

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

        is_symbol = False
        for r, c in adjacent:
            if (r, c) in coordinates:
                # does not really matter for us
                continue
            char = get(r, c)
            is_symbol = not char.isdigit() and char != '.'

            if is_symbol:
                break

        if is_symbol:
            result += int(part_num)

    # process the field line by line
    for row in range(len(field)):
        for col in range(len(field[row])):
            if field[row][col].isdigit() and not get(row, col - 1).isdigit():
                # process every first digit to avoid double count
                process(row, col)

    print(result)
