file = open('data.txt', 'r')

rules = []
updates = []

while True:
    line = file.readline()
    if line == '\n':
        break
    x, y = (int(n) for n in line.strip().split('|'))
    rules.append((x, y))

while True:
    line = file.readline()
    if not line:
        break
    updates.append([int(n) for n in line.strip().split(',')])


def is_good_order(numbers):
    for idx in range(1, len(numbers)):
        for prev_idx in range(idx):
            cur, prev = numbers[idx], numbers[prev_idx]
            if (cur, prev) in rules:
                # print('(%d, %d) is a violation' % (prev, cur))
                return False
    return True


result = 0
for seq in updates:
    if is_good_order(seq):
        result += seq[len(seq) // 2]
print(result)


# part 2

def sort(seq):
    result = []
    filtered_rules = [rule for rule in rules if rule[0] in seq and rule[1] in seq]
    processed = set()

    def process(x):
        if x in processed:
            return
        processed.add(x)
        # process all the preceeding first
        for prev, cur in filtered_rules:
            if cur == x:
                process(prev)
        if x not in result:
            result.append(x)

    for x in seq:
        process(x)

    assert len(result) == len(seq)
    return result

result = 0
for seq in updates:
    if is_good_order(seq):
        continue
    seq2 = sort(seq)
    result += seq2[len(seq2) // 2]
print(result)
