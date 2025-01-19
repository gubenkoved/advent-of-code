games = []

with open('data.txt', 'r') as file:
    while True:
        line = file.readline()

        if not line:
            break

        games.append(line.strip().split(' '))

# A for Rock, B for Paper, and C for Scissors. The second column--" Suddenly, the Elf is called away to help with someone's tent.
# The second column, you reason, must be what you should play in response: X for Rock, Y for Paper, and Z for Scissors. Winning every time would be suspicious, so the responses must have been carefully chosen.

m = {
    'A': {
        'X': None,
        'Y': True,
        'Z': False,
    },
    'B': {
        'X': False,
        'Y': None,
        'Z': True,
    },
    'C': {
        'X': True,
        'Y': False,
        'Z': None,
    }
}

# shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors)
m2 = {
    'X': 1,
    'Y': 2,
    'Z': 3,
}

total = 0
for a, b in games:
    is_won = m[a][b]
    if is_won is True:
        score = 6
    elif is_won is False:
        score = 0
    else:
        score = 3

    score += m2[b]
    total += score

print(total)
