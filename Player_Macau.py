# ============================================================================
# PLAYER_MACAU.PY - Player logic for Macau game
# ============================================================================
"""Module containing player logic for the Macau card game."""

from numpy import random

from Deck import Card, print_cards

"""Represents a player in the Macau card game."""
class Player:
    def __init__(self, hand: list[Card], name: str, bot: bool = False) -> None:
        self.colors = ["Diamonds", "Spades", "Hearts", "Clubs"]
        self.hand = hand
        self.Sort_Hand()
        self.skip = 0
        self.bot = bot
        self.name = name
        self.top_card: Card = Card(0, "", "")
        self.game_state: dict = {}

    """Sort the player's hand by suit and then by value."""
    def Sort_Hand(self) -> None:
        sorted_hand = []
        for color in self.colors:
            sorted_hand.extend(
                sorted([card for card in self.hand if card.color == color], key=lambda x: x.value)
            )
        self.hand = sorted_hand

    def get_input_int_or_x(self, prompt: str) -> str | int:
        while True:
            user_input = input(prompt).strip().lower()

            if user_input == "x":
                return "x"

            try:
                return int(user_input)
            except ValueError:
                print("Please enter an integer or 'x'!")

    """Check if a card can be played given the current game state."""
    def Check_Game_State(self, game, choice: int) -> Card | None:  # type: ignore[no-untyped-def]
        if self.game_state["demanded color"]:
            if self.top_card.figure == "A" and self.hand[choice].figure == "A":
                return self.hand.pop(choice)
            if self.hand[choice].color == self.game_state["demanded color"]:
                self.game_state["demanded color"] = False
                return self.hand.pop(choice)
        elif self.game_state["skip"]:
            if game.Check(self.top_card, self.hand[choice], "4"):
                return self.hand.pop(choice)
        elif game.Check(self.top_card, self.hand[choice]):
            return self.hand.pop(choice)
        return None


    """
    Choose a card to play from hand (human player).

    Args:
        top_card: Current top card
        game_state: Current game state
        game: Game instance

    Returns:
        Chosen card or None if drawing/skipping
    """
    def Choose_From_Hand(self, game) -> Card | None | bool:  # type: ignore[no-untyped-def]
        if self.game_state["draw"]:
            print("Cards to draw: ", self.game_state["draw"])
        if self.game_state["demanded color"]:
            print("Demanded color: ", self.game_state["demanded color"])
        print("\nYour hand:")
        print_cards(self.hand)

        while True:
            choice = (
                self.get_input_int_or_x("Choose a card or draw (x):")
                if not self.game_state["skip"]
                else self.get_input_int_or_x("Put down 4 or skip turn (x): ")
            )

            if choice == "x":
                if self.game_state["skip"]:
                    pass
                elif not self.game_state["draw"]:
                    self.game_state["draw"] += 1
                return False

            if choice in range(len(self.hand)):
                result = self.Check_Game_State(game, choice)  # type: ignore[arg-type]
                if result:
                    return result
                else:
                    print("Please choose a card that can be played!")
            else:
                print("Please choose a card in your hand!")

    def Take_Turn(
        self, deck: list[Card], top_card: Card, game_state: dict, card_sets: dict, game
    ) -> Card | bool:  # type: ignore[no-untyped-def]
        self.top_card = top_card
        self.game_state = game_state
        print("------------------")
        print("Turn: ", self.name)
        if self.game_state["skip"]:
            print("You're skipping your turn")
            print("Turns left to skip: ", self.game_state["skip"])
            self.game_state["skip"] -= 1
            input("Click enter")
            return False

        print("Card on the table: ", self.top_card)

        chosen_card = self.Choose_From_Hand(game)

        self.Sort_Hand()

        if chosen_card:
            if chosen_card in card_sets["draw cards"]:
                if chosen_card.figure == "2":
                    self.game_state["draw"] += 2
                elif chosen_card.figure == "3":
                    self.game_state["draw"] += 3
                elif chosen_card.figure == "K":
                    self.game_state["draw"] += 5
            elif chosen_card.figure == "4":
                self.game_state["skip"] += 1
            elif chosen_card.figure == "A":
                for color in self.colors:
                    print(color.center(10), end="")
                print()
                for i in range(len(self.colors)):
                    print(str(i).center(10), end="")
                print()
                while True:
                    choice = int(input("Choose a color to demand: "))
                    if choice in range(len(self.colors)):
                        break
                self.game_state["demanded color"] = self.colors[choice]
                return chosen_card
            return chosen_card

        else:
            if self.game_state["draw"]:
                if len(deck) == 0:
                    print("No cards remaining in the deck")
                    self.game_state["draw"] = 0
                else:
                    for i in range(self.game_state["draw"]):
                        self.hand.append(deck.pop(0))
                    self.game_state["draw"] = 0
            elif self.game_state["skip"]:
                self.skip = self.game_state["skip"]
                self.game_state["skip"] = 0
            return False


    """
    Choose a card to play (bot player).

    Args:
        top_card: Current top card
        game_state: Current game state
        game: Game instance

    Returns:
        Chosen card or None if drawing/skipping
    """
    def Bot_Choose_From_Hand(self, game) -> Card | bool:  # type: ignore[no-untyped-def]
        for index, card in enumerate(self.hand):
            choice = index
            result = self.Check_Game_State(game, choice)
            if result:
                return result

        if self.game_state["skip"]:
            pass
        elif not self.game_state["draw"]:
            self.game_state["draw"] += 1
        return False

    def Bot_Take_Turn(
        self, deck: list[Card], top_card: Card, game_state: dict, card_sets: dict, game
    ) -> Card | bool:  # type: ignore[no-untyped-def]
        self.top_card = top_card
        self.game_state = game_state
        print("------------------")
        print("Turn: ", self.name)
        print("Bot has ", len(self.hand), " cards remaining.")
        if self.game_state["skip"]:
            print("Bot skips turn")
            self.game_state["skip"] -= 1
            return False

        chosen_card = self.Bot_Choose_From_Hand(game)

        if chosen_card:
            print("\nBot plays", chosen_card)
            if chosen_card in card_sets["draw cards"]:
                if chosen_card.figure == "2":
                    game_state["draw"] += 2
                elif chosen_card.figure == "3":
                    game_state["draw"] += 3
                elif chosen_card.figure == "K":
                    game_state["draw"] += 5
            elif chosen_card.figure == "4":
                game_state["skip"] += 1
            elif chosen_card.figure == "A":
                colors = ["Diamonds", "Spades", "Hearts", "Clubs"]
                game_state["demanded color"] = colors[random.randint(0, 4)]
                return chosen_card
            return chosen_card

        else:
            if game_state["draw"]:
                if len(deck) == 0:
                    print("No cards remaining in the deck, Bot draws nothing.")
                    self.game_state["draw"] = 0
                else:
                    print("Bot draws ", game_state["draw"], " cards")
                    for i in range(game_state["draw"]):
                        self.hand.append(deck.pop(0))
                    game_state["draw"] = 0
            elif game_state["skip"]:
                print("Bot skips turn")
                self.skip = game_state["skip"]
                game_state["skip"] = 0
            return False
