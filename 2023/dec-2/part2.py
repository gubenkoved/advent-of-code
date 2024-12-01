if __name__ == '__main__':
    result = 0
    with open('data.txt', 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            game_num = int(line.split(':')[0].replace('Game ', ''))
            draws = line.split(':', maxsplit=1)[1]
            counts = {
                'red': 0,
                'green': 0,
                'blue': 0,
            }
            for draw in draws.split(';'):
                draw = draw.strip()
                for ball in draw.split(','):
                    ball = ball.strip()
                    amount, color = ball.split(' ')
                    amount = int(amount)
                    counts[color] = max(counts[color], amount)
            result += counts['red'] * counts['green'] * counts['blue']
    print(result)
