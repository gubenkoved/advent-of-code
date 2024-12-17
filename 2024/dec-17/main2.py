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


def seeds(bit_len):
    for num in range(2 ** bit_len):
        result = run(num, 0, 0, instructions)
        if result and result[0] == instructions[0]:
            yield num


def solver(prefix_len):
    if prefix_len == 1:
        yield from seeds(bit_len=10)
        return

    bit_offset = 10 + 3 * (prefix_len - 2)
    bit_step = 3

    # recursion step
    for num in solver(prefix_len - 1):
        for delta in range(2 ** bit_step):
            new_num = num + (delta << bit_offset)
            result = run(new_num, 0, 0, instructions)
            if result and result[:prefix_len] == instructions[:prefix_len]:
                yield new_num

# for num in range(2 ** 19):
#     res = run_5(num)
#     if len(res) >= 4 and res[:4] == instructions[:4]:
#         print('%r, %r' % (num, res))

for num in solver(len(instructions)):
    print(num)

print(min(solver(len(instructions))))
