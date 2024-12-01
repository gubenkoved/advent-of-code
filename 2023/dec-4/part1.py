if __name__ == '__main__':
    result = 0

    with open('data.txt', 'r') as f:
        while True:
            line = f.readline()

            if not line:
                break

            card_head, card_all_numbers = line.split(':')
            win_numbers, card_numbers = card_all_numbers.split('|')

            win_numbers = win_numbers.strip().replace('  ', ' ').split(' ')
            card_numbers = card_numbers.strip().replace('  ', ' ').split(' ')

            matching_count = sum(1 for x in card_numbers if x in win_numbers)

            assert len(card_numbers) == len(set(card_numbers))
            assert len(win_numbers) == len(set(win_numbers))

            if matching_count > 0:
                result += 2 ** (matching_count - 1)

    print(result)
