file = open('data.txt', 'r')

reg_a = int(file.readline().split(':')[-1])
reg_b = int(file.readline().split(':')[-1])
reg_c = int(file.readline().split(':')[-1])

_ = file.readline()

instructions = tuple(int(x) for x in file.readline().split(':')[-1].strip().split(','))

def run(reg_a, reg_b, reg_c, instructions):
    output = []

    ptr = 0

    while True:
        if ptr >= len(instructions):
            break

        opcode = instructions[ptr]
        arg  = instructions[ptr+1]

        combo = None
        literal = arg

        if arg <= 3:
            combo = arg
        elif arg == 4:
            combo = reg_a
        elif arg == 5:
            combo = reg_b
        elif arg == 6:
            combo = reg_c
        else:
            assert False, 'reserved'

        if opcode == 0:
            reg_a = int(reg_a / (2 ** combo))
            ptr += 2
        elif opcode == 1:
            reg_b = reg_b ^ literal
            ptr += 2
        elif opcode == 2:
            reg_b = combo % 8
            ptr += 2
        elif opcode == 3:
            if reg_a == 0:
                # nothing
                ptr += 2
            else:
                # jump
                ptr = literal
        elif opcode == 4:
            reg_b = reg_b ^ reg_c
            ptr += 2
        elif opcode == 5:
            output.append(combo % 8)
            ptr += 2
        elif opcode == 6:
            reg_b = int(reg_a / (2 ** combo))
            ptr += 2
        elif opcode == 7:
            reg_c = int(reg_a / (2 ** combo))
            ptr += 2
        else:
            assert False, 'not supported'

    return tuple(output)


# converted program
def run_2(reg_a):
    output = []
    while True:
        reg_b = reg_a % 8
        reg_b = reg_b ^ 2
        reg_c = int(reg_a / (2 ** reg_b))
        reg_b = reg_b ^ reg_c
        reg_b = reg_b ^ 3
        output.append(reg_b % 8)
        reg_a = int(reg_a / 8)
        if reg_a == 0:
            break
    return tuple(output)


def run_3(reg_a):
    output = []
    while True:
        reg_b = (reg_a % 8) ^ 2
        reg_b = 3 ^ reg_b ^ int(reg_a / (2 ** reg_b))
        output.append(reg_b % 8)
        reg_a = int(reg_a / 8)
        if reg_a == 0:
            break
    return tuple(output)


def run_4(reg_a):
    output = []
    while True:
        reg_b = (reg_a % 8) ^ 2
        reg_b = 3 ^ reg_b ^ (reg_a >> reg_b)
        output.append(reg_b % 8)
        reg_a = reg_a >> 3
        if reg_a == 0:
            break
    return tuple(output)


def run_5(reg_a):
    output = []
    while True:
        reg_b = (reg_a % 8) ^ 2
        # reg_b is in [0, 7]
        reg_b ^= 3 ^ (reg_a >> reg_b)
        output.append(reg_b % 8)
        reg_a = reg_a >> 3
        if reg_a == 0:
            break
    return tuple(output)


for n in range(10 ** 10):
    reg_a = n

    if reg_a % 1000000 == 0:
        print(reg_a)

    # r1 = run(reg_a, reg_b, reg_c, instructions)
    # r2 = run_2(reg_a)
    # r3 = run_3(reg_a)
    # r4 = run_4(reg_a)
    r5 = run_5(reg_a)
    r = r5

    # if r5 != r4:
    #     assert False, 'wrong sim at %s' % reg_a

    if r == instructions:
        print('*** %s' % reg_a)
        break

    if r == instructions[:len(r)]:
        print('prefix match! %d: %s' % (reg_a, r))
