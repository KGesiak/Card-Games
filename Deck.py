from numpy import random

class Card:
    def __init__(self, value, figure, color):
        self.value = value
        self.color = color
        self.figure = figure

    def print_card(self):
        print(f"{self.figure} {self.color}")


cards_set = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
cards_set_values = [i for i in range(13)]


def full_deck():
    colors = ["Diamonds", "Spades", "Hearts", "Clubs"]
    deck = []
    for color in colors:
        temp = [Card(value, figure, color) for value, figure in list(zip(cards_set_values, cards_set))]
        deck.extend(temp)
    return deck


def spread_between(deck, number_of_players, hand):  # deck jest shuffled
    hands = []
    # if na ilosc kart
    random.shuffle(deck)
    for i in range(number_of_players):
        hands.append(deck[:hand])
        deck = deck[hand:]
    return deck, hands


def print_deck(deck):
    for number, card in enumerate(deck):
        print(number, ":", sep='', end=' ')
        card.print_card()