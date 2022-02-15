from Player_Macau import *

class Game_Macau:

        #NO END GAME MECHANIC YET

    def __init__(self,number_of_players,number_of_bots):
        self.deck = full_deck()
        self.active_cards = []
        self.draw_cards = []
        self.Assign_Card_Groups()
        self.deck, self.hands = spread_between(self.deck, number_of_players + number_of_bots, 10) #zwraca deck bez kart ktore sa przydzielone w liscie rak (dla mnei ma sens)
        self.top_card = 0
        self.Assign_Card_Groups()
        self.card_sets = {"draw cards": self.draw_cards , "active cards": self.active_cards, "basic cards": ["5","6","7","8","9","10","Q"]}
        self.cards_on_table = [self.deck.pop(0)]
        self.game_state = {"draw": 0, "skip": 0, "demand": 0, "demanded card": False, "demanded color": False, "number of players": number_of_players}
        self.Start(number_of_players,number_of_bots)

    def Start(self,number_of_players,number_of_bots):

        players = []
        for i in range(number_of_players):
            players.append(Player(self.hands[i],"Player " + str(i+1)))
        for i in range(number_of_players,number_of_bots + number_of_players):
            players.append(Player(self.hands[i],"Bot " + str(i - number_of_players+1),bot=True))
        end = 0
        while not end:
            for player in players:
                if player.bot:
                    new_card = player.Bot_Take_Turn(self.deck, self.cards_on_table[-1], self.game_state,self.card_sets,self) #jezeli self wysylam to nic innego nie trzeba w sumie
                else:
                    new_card = player.Take_Turn(self.deck, self.cards_on_table[-1], self.game_state,self.card_sets,self)
                if new_card:
                    self.cards_on_table.append(new_card)
                if not len(player.hand): #jezeli reka jest 0
                    print(player.name," wins!")
                    end = 1
                    break


    def Check(self,top_card, chosen_card, demand=0):
        if self.game_state["draw"]:
            if top_card in self.draw_cards: #tutaj chodzi o to ze na karte ktora dobiera mozna tylko rzucic inna karte ktora dobiera
                if not chosen_card in self.draw_cards:
                    return 0
        if demand:
            if (chosen_card.figure == demand):
                #zmienic ilosc razy ile demand wyskakuje
                return 1
        elif (top_card.color == chosen_card.color or top_card.figure == chosen_card.figure):
            return 1
        return 0

    def Assign_Card_Groups(self):
        for card in self.deck:
            if (card.figure in ["2","3"]):
                self.draw_cards.append(card)
            elif (card.figure == "K"):
                if (card.color == "Kier" or card.color == "Pik"):
                    self.draw_cards.append(card)
            elif (card.figure in ["4", "J","A"]):
                self.active_cards.append(card)
