# Five of a kind, where all five cards have the same label: AAAAA
# Four of a kind, where four cards have the same label and one card has a different label: AA8AA
# Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
# Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
# Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
# One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
# High card, where all cards' labels are distinct: 23456


CARD_ORDER = '23456789TJQKA'


class Hand:
    def __init__(self, s):
        self.cards = list(s)
        self._rank_tuple = self.rank_tuple()

    def rank_tuple(self):
        return (
            self.is_five_of_kind(),
            self.is_four_of_kind(),
            self.is_full_house(),
            self.is_three_of_kind(),
            self.is_two_pairs(),
            self.is_one_pair(),
            self.card_strengths(),
        )

    def __repr__(self):
        return 'Hand(%r)' % self.cards

    def __lt__(self, other):
        return self._rank_tuple < other._rank_tuple

    def card_counts(self):
        counts = {}
        for card in self.cards:
            if card not in counts:
                counts[card] = 0
            counts[card] += 1
        return counts

    def is_five_of_kind(self):
        return max(self.card_counts().values()) == 5

    def is_four_of_kind(self):
        return max(self.card_counts().values()) == 4

    def is_full_house(self):
        counts = self.card_counts()

        return len(counts) == 2 and set(counts.values()) == {2, 3}

    def is_three_of_kind(self):
        return max(self.card_counts().values()) == 3

    def is_two_pairs(self):
        counts = self.card_counts()
        return len(counts) == 3 and set(counts.values()) == {2, 2, 1}

    def is_one_pair(self):
        counts = self.card_counts()
        return len(counts) == 4 and set(counts.values()) == {2, 1, 1, 1}

    def card_strengths(self):
        # return tuple(sorted([CARD_ORDER.index(c) for c in self.cards], reverse=True))
        return tuple(CARD_ORDER.index(c) for c in self.cards)


if __name__ == '__main__':
    hands = []
    with open('data.txt', 'r') as f:
        while True:
            line = f.readline()

            if not line:
                break

            hand, bid = line.split(' ')

            hands.append(
                (Hand(hand), int(bid))
            )

    # weakest first
    sorted_hands = sorted(hands, key=lambda t: t[0])

    result = 0
    for rank, hand in enumerate(sorted_hands, start=1):
        result += rank * hand[1]
    print(result)
