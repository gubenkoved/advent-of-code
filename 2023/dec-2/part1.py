if __name__ == '__main__':
    limits = {
        'red': 12,
        'green': 13,
        'blue': 14,
    }
    result = 0
    with open('data.txt', 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            game_num = int(line.split(':')[0].replace('Game ', ''))
            draws = line.split(':', maxsplit=1)[1]
            possible = True
            for draw in draws.split(';'):
                draw = draw.strip()
                for ball in draw.split(','):
                    ball = ball.strip()
                    amount, color = ball.split(' ')
                    amount = int(amount)
                    if amount > limits[color]:
                        possible = False
            if possible:
                result += game_num
    print(result)
