if __name__ == '__main__':

    # list of matching counts on each card
    card_match_counts = []

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
            card_match_counts.append(matching_count)

    n = len(card_match_counts)
    multipliers = [1] * n

    for idx in range(len(card_match_counts)):
        cur_count = card_match_counts[idx]

        # update multipliers
        for next_idx in range(idx + 1, idx + 1 + cur_count):
            if next_idx < n:
                multipliers[next_idx] += multipliers[idx]

    print(sum(multipliers))  # 18572
