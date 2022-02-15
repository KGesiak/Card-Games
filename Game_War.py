from Deck import *

class Game_War:

    def Compare(self,Player_Card, Computer_Card):
        if (Player_Card.value > Computer_Card.value):
            return 1
        elif (Player_Card.value < Computer_Card.value):
            return 0
        else:
            return -1


    def Round(self,Player_Hand, Computer_Hand):
        Won_cards = []
        while (True):
            Player_Card = Player_Hand.pop(0)
            print(f"Player's card: ", end='')
            Player_Card.print_card()

            Computer_Card = Computer_Hand.pop(0)
            print(f"Computer's card: ", end='')
            Computer_Card.print_card()

            Won_cards.extend([Player_Card, Computer_Card])

            Round_Result = self.Compare(Player_Card, Computer_Card)

            if (Round_Result == 1):
                print("Player's card wins, both cards go to player's deck")
                Player_Hand.extend(Won_cards)
                break
            elif (Round_Result == 0):
                print("Computer's card wins, both cards go to computer's deck")
                Computer_Hand.extend(Won_cards)
                break
            else:
                print("\nWAR!!!")
                if (len(Player_Hand) <= 1):
                    print("Player does not have enough cards for war")
                    Computer_Hand.extend(Player_Hand)
                    Player_Hand.clear()
                    return
                elif (len(Computer_Hand) <= 1):
                    print("Computer does not have enough cards for war")
                    Player_Hand.extend(Computer_Hand)
                    Computer_Hand.clear()
                    return
                Won_cards.extend(
                    [Player_Hand.pop(0), Computer_Hand.pop(0)])
                print("Both player and computer put down reversed cards")
                print("Next cards will show the winner of current war: ")


    def Start(self):
        d = full_deck()
        d, h = spread_between(d, 2, int(len(d) / 2))
        counter = 0
        while (len(h[0]) and len(h[1])):
            print("\nPress enter to put down a card")

            x = input()
            self.Round(h[0], h[1])
            counter += 1
            print(f"Players deck: {len(h[0])}")
            print(f"Computers deck: {len(h[1])}")
        print("GAME OVER")
        print(counter)