# ============================================================================
# GAME_MACAU.PY - Main game logic
# ============================================================================
"""Module containing the main Macau game logic."""

from Deck import Card, Deck
from Player_Macau import Player


class Game_Macau:
    """Main game controller for Macau card game."""
    def __init__(self) -> None:
        new_deck = Deck()
        self.deck = new_deck.create_full_deck()
        self.active_cards = []
        self.draw_cards = []
        self.basic_cards = []
        self.Assign_Card_Groups()
        self.deck, self.hands = new_deck.spread_between(10)
        self.top_card = 0
        self.number_of_players = 2
        self.Assign_Card_Groups()
        self.card_sets = {
            "draw cards": self.draw_cards,
            "active cards": self.active_cards,
            "basic cards": self.basic_cards,
        }
        self.cards_on_table = [self.deck.pop(0)]
        self.game_state = {"draw": 0, "skip": 0, "demanded color": False}

        print("Welcome to the Game Macau!\n\n")

    def Start(self) -> None:
        players = [Player(self.hands[0], "Player"), Player(self.hands[1], "Bot", bot=True)]

        while True:
            for player in players:
                if player.bot:
                    new_card = player.Bot_Take_Turn(
                        self.deck, self.cards_on_table[-1], self.game_state, self.card_sets, self
                    )
                else:
                    new_card = player.Take_Turn(
                        self.deck, self.cards_on_table[-1], self.game_state, self.card_sets, self
                    )
                if new_card:
                    self.cards_on_table.append(new_card)  # type: ignore[arg-type]
                if not len(player.hand):
                    print(player.name, " wins!")
                    break
    """Check for cards' validity"""
    def Check(self, top_card: Card, chosen_card: Card, demand: int = 0) -> int:
        if self.game_state["draw"]:
            if top_card in self.draw_cards:
                if chosen_card not in self.draw_cards:
                    return 0
        if demand:
            if chosen_card.figure == demand:  # type: ignore[comparison-overlap]
                return 1
        elif top_card.color == chosen_card.color or top_card.figure == chosen_card.figure:
            return 1
        return 0

    """Assigns cards to classes based on their roles"""
    def Assign_Card_Groups(self) -> None:
        seen_basic_cards = set()
        for card in self.deck:
            if card.figure in ["2", "3"]:
                self.draw_cards.append(card)
            elif card.figure == "K":
                if card.color == "Hearts" or card.color == "Spades":
                    self.draw_cards.append(card)
                else:
                    self.basic_cards.append(card)
            elif card.figure in ["4", "A"]:
                self.active_cards.append(card)
            else:
                if card.figure not in seen_basic_cards:
                    seen_basic_cards.add(card.figure)
                    self.basic_cards.append(card)
