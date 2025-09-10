# ============================================================================
# DECK.PY - Reusable Card System
# ============================================================================
# This module provides a flexible card system that can be used for any card game.

from numpy import random

"""Represents a single playing card with value, figure (rank), and color."""
class Card:
    def __init__(self, value: int, figure: str, color: str):
        self.value = value
        self.color = color
        self.figure = figure

    def __str__(self) -> str:
        return f"{self.figure} of {self.color}"

"""Manages a standard deck of playing cards."""
class Deck:
    def __init__(self) -> None:
        self.number_of_players = 2
        self.cards_set = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.cards_set_values = [i for i in range(13)]
        self.full_deck: list[Card] = []
        self.colors = ["Diamonds", "Spades", "Hearts", "Clubs"]

    def create_full_deck(self) -> list[Card]:
        for color in self.colors:
            temp = [
                Card(value, figure, color)
                for value, figure in list(zip(self.cards_set_values, self.cards_set))
            ]
            self.full_deck.extend(temp)
        return self.full_deck

    """
            Shuffle the deck in place.

            Returns:
                The shuffled deck
    """
    def shuffle_deck(self) -> list[Card]:
        random.shuffle(self.full_deck)  # type: ignore[arg-type]
        return self.full_deck

    """
    Deals cards to all the players and returns the rest of the deck.
    """
    def spread_between(self, number_of_cards_in_hand: int) -> tuple[list[Card], list[list[Card]]]:
        hands = []
        self.shuffle_deck()
        rest_of_the_deck = self.full_deck[number_of_cards_in_hand:]
        for i in range(self.number_of_players):
            hands.append(rest_of_the_deck[:number_of_cards_in_hand])
            rest_of_the_deck = rest_of_the_deck[number_of_cards_in_hand:]
        return rest_of_the_deck, hands


def print_cards(deck: list[Card]) -> None:
    for number, card in enumerate(deck):
        print(number, ": ", card, sep="")
