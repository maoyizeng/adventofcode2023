from enum import Enum

# a list for each hand type
all_hands = [[] for _ in range(7)]

class HandType(Enum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6

Card = {
    'A' : 14,
    'K' : 13,
    'Q' : 12,
    'J' : 11,
    'T' : 10,
    '9' : 9,
    '8' : 8,
    '7' : 7,
    '6' : 6,
    '5' : 5,
    '4' : 4,
    '3' : 3,
    '2' : 2,
}

class Hand(object):
    def __init__(self, string):
        temp_cards = string.split()[0]
        self.bid = int(string.split()[1])

        # convert the strength comparison of each card into an integer
        self.strength = Card[temp_cards[0]] * 15 * 15 * 15 * 15 + Card[temp_cards[1]] * 15 * 15 * 15 + Card[temp_cards[2]] * 15 * 15 + Card[temp_cards[3]] * 15 + Card[temp_cards[4]]

        # a dict as {'card': count}
        self.cards = {}
        for c in temp_cards:
            v = self.cards.get(c)
            if v:
                self.cards[c] = v + 1
            else:
                self.cards[c] = 1

def main():
    with open('hands.txt', 'r') as file:
        for line in file:
            temp_hand = Hand(line)
            l = len(temp_hand.cards)
            if l == 5:
                # a hand with 5 distinguish cards must be a high card
                all_hands[HandType.HIGH_CARD.value].append(temp_hand)
            elif l == 4:
                all_hands[HandType.ONE_PAIR.value].append(temp_hand)
            elif l == 3:
                # if there's a card with count of 3, it is a three of a kind
                if 3 in temp_hand.cards.values():
                    all_hands[HandType.THREE_OF_A_KIND.value].append(temp_hand)
                else:
                    all_hands[HandType.TWO_PAIR.value].append(temp_hand)
            elif l == 2:
                if 4 in temp_hand.cards.vaules():
                    all_hands[HandType.FOUR_OF_A_KIND.value].append(temp_hand)
                else:
                    all_hands[HandType.FULL_HOUSE.value].append(temp_hand)
            else:
                all_hands[HandType.FIVE_OF_A_KIND.value].append(temp_hand)

    # combine the 7 lists of hand type into 1
    final_hands = []
    for i in range(7):
        all_hands[i].sort(key = lambda hand:hand.strength)
        final_hands = final_hands + all_hands[i]

    # the full list is sorted, add the result with weight
    result = 0
    for i in range(len(final_hands)):
        result = result + (i + 1) * final_hands[i].bid
    print(result)

if __name__=='__main__':
    main()
