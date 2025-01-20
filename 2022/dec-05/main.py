import re

lines = []
stacks = []
moves = []

with open('data.txt', 'r') as file:
    # read stacks configuration first
    while True:
        line = file.readline()

        if line == '\n':
            break

        line = line
        lines.append(line)

    # recreate stacks
    lines.pop(-1)
    stacks_count = max(round(len(line) / 4) for line in lines)
    for stack_idx in range(stacks_count):
        stack = []
        for line in reversed(lines):
            idx = 1 + 4 * stack_idx
            if len(line) <= idx:
                continue
            if line[idx] != ' ':
                stack.append(line[idx])
        stacks.append(stack)

    # read moves
    while True:
        line = file.readline()

        if not line:
            break

        match = re.match('move ([0-9]+) from ([0-9]+) to ([0-9])', line.strip())

        assert match

        moves.append((
            int(match.group(1)),
            int(match.group(2)),
            int(match.group(3)),
        ))

# now just implement the moves
for count, from_idx, to_idx in moves:
    from_new, moving = stacks[from_idx - 1][:-count], stacks[from_idx - 1][-count:]
    stacks[to_idx - 1].extend(reversed(moving))
    stacks[from_idx - 1] = from_new

print(''.join(stack[-1] for stack in stacks))
