file = open('data.txt', 'r')

data = [line.split(' ') for line in file.read().splitlines()]
data = [(int(t[0]), int(t[-1])) for t in data]

l1 = [t[0] for t in data]
l2 = [t[1] for t in data]

l1s = sorted(l1)
l2s = sorted(l2)

# part1
print(sum(abs(n1 - n2) for n1, n2 in zip(l1s, l2s)))

l2freq = {}
for n in l2:
    if n not in l2freq:
        l2freq[n] = 0
    l2freq[n] += 1

sim_score = 0
for n in l1:
    sim_score += n * l2freq.get(n, 0)
print(sim_score)
