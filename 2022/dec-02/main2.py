games = []

with open('data.txt', 'r') as file:
    while True:
        line = file.readline()

        if not line:
            break

        games.append(line.strip().split(' '))

# A for Rock, B for Paper, and C for Scissors. The second column--" Suddenly, the Elf is called away to help with someone's tent.
# The Elf finishes helping with the tent and sneaks back over to you. "Anyway, the second column says how the round needs to end:
# X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win. Good luck!"

m = {
    'A': {
        'X': 'C',
        'Y': 'A',
        'Z': 'B',
    },
    'B': {
        'X': 'A',
        'Y': 'B',
        'Z': 'C',
    },
    'C': {
        'X': 'B',
        'Y': 'C',
        'Z': 'A',
    }
}

m2 = {
    'A': {
        'A': None,
        'B': True,
        'C': False,
    },
    'B': {
        'A': False,
        'B': None,
        'C': True,
    },
    'C': {
        'A': True,
        'B': False,
        'C': None,
    }
}

# shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors)
m3 = {
    'A': 1,
    'B': 2,
    'C': 3,
}

total = 0
for a, outcome in games:
    b = m[a][outcome]

    is_won = m2[a][b]
    if is_won is True:
        score = 6
    elif is_won is False:
        score = 0
    else:
        score = 3

    score += m3[b]
    total += score

print(total)
