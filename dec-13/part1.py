if __name__ == '__main__':
    fields = []

    with open('data.txt', 'r') as f:
        line = None
        while True:
            field = []
            while True:
                line = f.readline()
                if not line or line == '\n':
                    break
                field.append(line.rstrip('\n'))
            fields.append(field)
            if not line:
                break

    def col_eq(field, idx1, idx2):
        for row in range(len(field)):
            if field[row][idx1] != field[row][idx2]:
                return False
        return True

    def row_eq(field, idx1, idx2):
        return field[idx1] == field[idx2]

    def print_field(field):
        for row in field:
            print(row)

    def solve(field):
        print('\nsolving for:')
        print_field(field)

        rows, cols = len(field), len(field[0])

        # check for vertical reflection
        for col_idx in range(1, cols):
            matched = True
            for d in range(col_idx):
                if col_idx + d >= cols:
                    break
                if not col_eq(field, col_idx - d - 1, col_idx + d):
                    matched = False
                    break
            if matched:
                return col_idx

        # check for horizontal reflections
        for row_idx in range(1, rows):
            matched = True
            for d in range(row_idx):
                if row_idx + d >= rows:
                    break
                if not row_eq(field, row_idx - d - 1, row_idx + d):
                    matched = False
                    break
            if matched:
                return 100 * row_idx

        assert 'not found!'

    result = sum(solve(field) for field in fields)
    print(result)
