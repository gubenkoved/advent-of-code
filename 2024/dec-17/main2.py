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


for reg_a in range(10 ** 8, 10 ** 9):
    if reg_a % 10000 == 0:
        print(reg_a)

    if run(reg_a, reg_b, reg_c, instructions) == instructions:
        print('*** %s' % reg_a)
        break
