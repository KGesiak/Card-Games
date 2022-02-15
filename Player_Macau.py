from Deck import *

test=0

class Player:
    def __init__(self, hand,name,bot=False):
        self.hand = hand
        self.Sort_Hand()
        self.skip = 0
        self.bot = bot
        self.name = name
        #dodac self.name zeby jak bedzie weicej graczy to bylo wiadomo co i jak

    def Sort_Hand(self):
        colors = ["Diamonds", "Spades", "Hearts", "Clubs"]
        sorted_hand = []
        for color in colors:
            temp = []
            for index,card in enumerate(self.hand):
                if card.color == color:
                    temp.append(self.hand[index]) #z pop by bylo szybciej ale wtedy kolejka sie zmienia i sa problemy wiec zmienic pozniej
            sorted_hand.extend(sorted(temp,key=lambda x: x.value))
        self.hand = sorted_hand



    def Choose_From_Hand(self, top_card, game_state,game):


        if game_state["draw"]: print("Cards to draw: ", game_state["draw"])
        if game_state["demand"]: print("Demanded card: ", game_state["demanded card"])
        if game_state["demanded color"]: print("Demanded color: ", game_state["demanded color"])
        print_deck(self.hand)
        while True:
            choice = input("Choose a card or draw (x):") if not game_state["skip"] else input("Put down 4 or skip turn (x): ")
            if (choice == "x"):
                if game_state["skip"]:
                    pass
                elif not game_state["draw"]:
                    game_state["draw"]+=1
                return False
            choice = int(choice) #zmienic bo wybucha przy nie intach
            if choice in range(len(self.hand)):
                if test: #do testowania mozna usunac
                    return self.hand.pop(choice)
                if game_state["demanded color"]:
                    if top_card.figure == "A" and self.hand[choice].figure == "A":
                        return self.hand.pop(choice)
                    if self.hand[choice].color == game_state["demanded color"]:
                        game_state["demanded color"] = False
                        return self.hand.pop(choice)
                elif game_state["skip"]:
                    if game.Check(top_card, self.hand[choice], "4"):
                         return self.hand.pop(choice)
                elif game_state["demand"]:
                    if top_card.figure == "J" and self.hand[choice].figure == "J":
                        return self.hand.pop(choice)
                    if game.Check(top_card,self.hand[choice],game_state["demanded card"]):
                        return self.hand.pop(choice)
                elif (game.Check(top_card, self.hand[choice])):
                    return self.hand.pop(choice)


    def Take_Turn(self, deck, top_card, game_state,card_sets,game):

        # if game_state["demand"]:
        #     top_card = game_state["demand"] ZLE BO NIE O TO CHODZI W DEMAND

        #tutaj trzeba zrobic ifa zaleznego od demand
        #CHOCIAZ jak jest J to mozna rzucic na J'a

        #BTW nie ma mechanizmu skipa
        print("Turn: ",self.name)
        if self.skip:
            print("You're skipping your turn")
            print("Turns left to skip: ",self.skip)
            self.skip-=1
            input("Click enter")
            return False

        print("Card on the table: ", end='')
        top_card.print_card()

        chosen_card = self.Choose_From_Hand(top_card,game_state,game) #Wybieranie karty

        self.Sort_Hand()

        if game_state["demand"]:
            game_state["demand"] -= 1
        if chosen_card:
            if (chosen_card in card_sets["draw cards"]):
                if (chosen_card.figure == "2"):
                    game_state["draw"] += 2
                elif (chosen_card.figure == '3'):
                    game_state["draw"] += 3
                elif (chosen_card.figure == 'K'):
                    game_state["draw"] += 5
            elif (chosen_card.figure == '4'):
                game_state["skip"] += 1
            elif (chosen_card.figure == "A"):
                colors = ["Diamonds", "Spades", "Hearts", "Clubs"]
                for color in colors:
                    print(color.center(5), end='')
                print()
                for i in range(len(colors)):
                    i = str(i)
                    print(i.center(5), end='')
                print()
                while True:
                    choice = int(input("Choose a color to demand: "))
                    if (choice in range(len(colors))):
                        break
                game_state["demanded color"] = colors[choice]
                return chosen_card
            elif (chosen_card.figure == "J"):
                for figure in card_sets["basic cards"]:
                    print(figure.center(5),end='') #zmien to na normalna liste z nazwami kart
                print()
                for i in range(len(card_sets["basic cards"])):
                    i = str(i)
                    print(i.center(5),end='')
                print()
                while True:
                   choice = int(input("Choose a card to demand: ")) #przetestowac z botem
                   if( choice in range(len(card_sets["basic cards"]))):
                        break
                game_state["demanded card"] = card_sets["basic cards"][choice]
                game_state["demand"] = game_state["number of players"]
            return chosen_card

        else:
            if game_state["draw"]:
                for i in range(game_state["draw"]):
                    self.hand.append(deck.pop(0))
                game_state["draw"] = 0
            elif game_state["skip"]:
                self.skip = game_state["skip"]
                game_state["skip"] = 0
            return 0

    def Bot_Choose_From_Hand(self, top_card, game_state,game):

        for index,card in enumerate(self.hand):
            choice = index

            if game_state["demanded color"]:
                if top_card.figure == "A" and self.hand[choice].figure == "A":
                    return self.hand.pop(choice)
                if self.hand[choice].color == game_state["demanded color"]:
                    game_state["demanded color"] = False
                    return self.hand.pop(choice)
            elif game_state["skip"]:
                if game.Check(top_card, self.hand[choice], "4"):
                     return self.hand.pop(choice)
            elif game_state["demand"]:
                if top_card.figure == "J" and self.hand[choice].figure == "J":
                    return self.hand.pop(choice)
                if game.Check(top_card,self.hand[choice],game_state["demanded card"]):
                    return self.hand.pop(choice)
            elif (game.Check(top_card, self.hand[choice])):
                return self.hand.pop(choice)

        if game_state["skip"]:
            pass
        elif not game_state["draw"]:
            game_state["draw"]+=1
        return False
    def Bot_Take_Turn(self, deck, top_card, game_state,card_sets,game):

        # if game_state["demand"]:
        #     top_card = game_state["demand"]

        #tutaj trzeba zrobic ifa zaleznego od demand
        #CHOCIAZ jak jest J to mozna rzucic na J'a

        #BTW nie ma mechanizmu skipa

        if self.skip:
            print("Bot skips turn")
            return False

        chosen_card = self.Bot_Choose_From_Hand(top_card,game_state,game) #Wybieranie karty

        if game_state["demand"]:
            game_state["demand"] -= 1
        if chosen_card:
            if (chosen_card in card_sets["draw cards"]):
                if (chosen_card.figure == "2"):
                    game_state["draw"] += 2
                elif (chosen_card.figure == '3'):
                    game_state["draw"] += 3
                elif (chosen_card.figure == 'K'):
                    game_state["draw"] += 5
            elif (chosen_card.figure == '4'):
                game_state["skip"] += 1
            elif (chosen_card.figure == "A"):
                colors = ["Diamonds", "Spades", "Hearts", "Clubs"]
                game_state["demanded color"] = colors[random.randint(0,4)]
                return chosen_card
            elif (chosen_card.figure == "J"):
                choice = random.randint(0,range(len(card_sets["basic cards"])))
                game_state["demanded card"] = card_sets["basic cards"][choice]
                game_state["demand"] = game_state["number of players"]
            return chosen_card

        else:
            if game_state["draw"]:
                print("Bot draws ",game_state["draw"]," cards")
                for i in range(game_state["draw"]):
                    self.hand.append(deck.pop(0))
                game_state["draw"] = 0
            elif game_state["skip"]:
                print("Bot skips turn")
                self.skip = game_state["skip"]
                game_state["skip"] = 0
            return 0
