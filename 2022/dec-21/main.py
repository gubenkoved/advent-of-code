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

print(my_eval('root'))
