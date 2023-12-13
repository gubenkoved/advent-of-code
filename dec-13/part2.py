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

    def col_mismatch_count(field, idx1, idx2):
        return sum(1 for row in range(len(field)) if field[row][idx1] != field[row][idx2])

    def row_mismatch_count(field, idx1, idx2):
        return sum(1 for col in range(len(field[0])) if field[idx1][col] != field[idx2][col])

    def print_field(field):
        for row in field:
            print(row)

    def solve(field):
        print('\nsolving for:')
        print_field(field)

        rows, cols = len(field), len(field[0])

        # check for vertical reflection
        for col_idx in range(1, cols):
            mismatch_count = 0
            for d in range(col_idx):
                if col_idx + d >= cols:
                    break
                mismatch_count += col_mismatch_count(field, col_idx - d - 1, col_idx + d)
            if mismatch_count == 1:
                return col_idx

        # check for horizontal reflections
        for row_idx in range(1, rows):
            mismatch_count = 0
            for d in range(row_idx):
                if row_idx + d >= rows:
                    break
                mismatch_count += row_mismatch_count(field, row_idx - d - 1, row_idx + d)
            if mismatch_count == 1:
                return 100 * row_idx

        assert 'not found!'

    result = sum(solve(field) for field in fields)
    print(result)
