defs = {}

with open('data.txt', 'r') as f:
    while True:
        line = f.readline()

        if not line:
            break

        line = line.strip()

        var, expr = line.split(':')

        try:
            val = int(expr)
            defs[var] = ('const', val)
        except ValueError:
            arg1, op, arg2 = expr.strip().split(' ')
            defs[var] = ('expr', arg1, op, arg2)


cache = {}


def my_eval(var):
    if var in cache:
        return cache[var]
    assert var in defs

    definition = defs[var]

    if definition[0] == 'const':
        return definition[1]
    else:
        _, arg1, op, arg2 = definition

        if op == '+':
            result = my_eval(arg1) + my_eval(arg2)
        elif op == '-':
            result = my_eval(arg1) - my_eval(arg2)
        elif op == '*':
            result = my_eval(arg1) * my_eval(arg2)
        elif op == '/':
            result = my_eval(arg1) / my_eval(arg2)
        else:
            assert False, 'what?'

    cache[var] = result
    return result


root_arg1 = defs['root'][1]
root_arg2 = defs['root'][3]


def try_humn(val):
    defs['humn'] = ('const', val)

    cache.clear()

    r1 = my_eval(root_arg1)
    r2 = my_eval(root_arg2)

    # print('r1 is %s and r2 is %s' % (r1, r2))

    if r1 > r2:
        return +1
    elif r1 < r2:
        return -1
    else:
        return 0


# looks like the end result is monotonic, so just big search it
left_incl = 0
right_excl = 10000000000000

assert try_humn(left_incl) == +1
assert try_humn(right_excl) == -1

while left_incl < right_excl:
    mid = (left_incl + right_excl) // 2

    result = try_humn(mid)
    print('checking %s result is %s' % (mid, result))

    if result == +1:
        left_incl = mid + 1
    elif result == -1:
        right_excl = mid
    else:
        print('found!')
        break
