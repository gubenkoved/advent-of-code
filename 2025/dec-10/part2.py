import sympy

def solve(switches: list[tuple[int]], targets: tuple[int]) -> int:
    n = len(switches)

    symbols = sympy.symbols(["x%d" % idx for idx in range(n)], integer=True)

    # compose equations
    equations = []

    for target_idx, target in enumerate(targets):
        exp = 0
        for switch_idx, switch in enumerate(switches):
            if target_idx in switch:
                exp += symbols[switch_idx]
        equations.append(
            sympy.Eq(exp, target)
        )

    solutions = sympy.solve(equations, dict=True)

    assert len(solutions) == 1

    solution = solutions[0]

    # find all free variables
    free = set()
    for symbol_expr in solution.values():
        free.update(symbol_expr.free_symbols)

    print(solution)
    print(f"  free symbols: {free}")

    best = None
    best_sum = None

    max_target = max(targets)

    def process_solution(solution):
        nonlocal best
        nonlocal best_sum

        cur_sum = sum(v for v in solution.values())
        if best_sum is None or cur_sum < best_sum:
            best_sum = cur_sum
            best = solution
            print(f"  better: {best} ({best_sum})")

    def is_definitely_bad(expr):
        if not expr.is_number:
            return False

        # skip invalid solutions
        if expr < 0:
            return True

        if not expr.is_integer:
            return True

        return False

    def resolve(solution, free):
        if not free:
            process_solution(solution)
            return

        # try all values for the variable
        var = next(iter(free))

        new_solution = {}

        for value in range(max_target + 1):
            new_solution[var] = sympy.Integer(value)

            is_bad_solution = False

            for symbol, symbol_expr in solution.items():
                new_symbol_expr = symbol_expr

                if not symbol_expr.is_number:
                    new_symbol_expr = symbol_expr.subs({var: value})

                new_solution[symbol] = new_symbol_expr

                if is_definitely_bad(new_symbol_expr):
                    is_bad_solution = True
                    break

            # check if any symbol will resolve to negative OR fractional
            # and skip it right away
            if is_bad_solution:
                continue

            resolve(new_solution, free - {var})

    resolve(solution, free)

    return best_sum

def parse(s: str) -> tuple[int]:
    return tuple(int(x) for x in s.strip("(){}").split(","))


# solving stuck at line 24 after yielding series of result of which 341 is the best
# if skipped manually and then adding 341 we get proper results of 15017...
if __name__ == '__main__':
    result = 0
    with open("data.txt", "r") as f:
        for line_idx, line in enumerate(f.read().splitlines(), 1):
            print(f"solving line #{line_idx}...")
            segments = line.split(" ")
            switches = [parse(x) for x in segments[1:-1]]
            targets = parse(segments[-1])

            cur = solve(switches, targets)
            print(f"  -> {cur}")
            result += cur
    print(f"answer: {result}")
