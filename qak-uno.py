import random
import time
from colorama import init
from termcolor import colored
 
init()

#There are three types of cards: number, action, action_non_color
#Numbers go from 0 to 9
#Action card which have color are: DRAW_2, REVERSE, SKIP
#Action card without color are WILD and WILD DRAW_4

colors = ["RED", "GREEN", "BLUE", "YELLOW"]
values = ["0","1","2","3","4","5","6","7","8","9","DRAW_2","REVERSE","SKIP","WILD","WILD_DRAW_4"]
card_type = {"0":"number","1":"number","2":"number","3":"number","4":"number","5":"number","6":"number","7":"number","8":"number","9":"number","DRAW_2":"action","REVERSE":"action","SKIP":"action","WILD":"action_non_color","WILD_DRAW_4":"action_non_color"}

#Card class
class Card:

    def __init__(self, color, value):
        self.value = value
        if card_type[value] == "number":
            self.color = color
            self.card_type = "number"
        elif card_type[value] == "action":
            self.color = color
            self.card_type = "action"
        else:
            self.color = None
            self.card_type = "action_non_color"

    def __repr__(self):
        if self.color == None:
            return colored(self.value, "grey", "on_white")
        else:
            if self.color == "BLUE":
                # return colored(self.color, "blue") + " " + colored(self.value, "blue")
                return colored(f"{self.color} {self.value}", "blue")
            if self.color == "GREEN":
                return colored(f"{self.color} {self.value}", "green")
            if self.color == "YELLOW":
                return colored(f"{self.color} {self.value}", "yellow")
            if self.color == "RED":
                return colored(f"{self.color} {self.value}", "red")

#Deck of Cards (originally 108 cards) 
class Deck:

    def __init__(self):
        self.deck = [Card(color, value) for color in colors for value in values]
        for color in colors:
            for value in values[1:13]:
                self.deck.append(Card(color, value))

    # Showing how many cards are in Deck
    def count(self):    
        return len(self.deck)

    def __repr__(self):
        return f"Deck of {self.count()} cards"
        
    #Taking cards from top of the Deck
    def deal(self, amount):
        count = self.count()
        actual = min([count,amount])
        if count == 0:
            raise ValueError("Theres no cards left in Deck")
        taken_cards = self.deck[-actual:] 
        self.deck = self.deck[:-actual]
        return taken_cards

    def shuffle(self):
        return random.shuffle(self.deck)

#Hand class
class Hand:

    def __init__(self):
        self.cards = []

    def add_cards(self, cards):
        self.cards = cards
        return self.cards

    def draw(self, cards):
        self.cards += cards
        return self.cards
    
    def chosen_card(self, index):
        return self.cards[index-1]
    
    def remove_card(self, index):
        return self.cards.pop(index-1)

    def cards_in_hand(self):
        for i in range(len(self.cards)):
            print(f"{str(i+1)}. {str(self.cards[i])}")
    
    def amount_of_cards(self):
        return len(self.cards)

#Checking if player can play chosen card
def valid_card(top_card, card):
    if top_card.color == card.color or top_card.value == card.value or card.card_type == "action_non_color":
        return True
    else:
        return False

#Checking if someone win
def win_checking(hand):
    if hand == 0:
        return True
    else:
        return False

game = True

while game:
    
    deck = Deck()
    deck.shuffle()

    #Choosing how many players will be in the game (between 2 and 10)
    players_numbers = []
    num_of_players = input("How many players will play? (2-10)")
    while not 2 <= int(num_of_players) <= 10:
        num_of_players = input("Choose from 2-10: ") 
    for player in range(int(num_of_players)):
        players_numbers.append(player + 1)


    hands = []
    for i in range(len(players_numbers)):
        hands.append(Hand())

    players = zip(players_numbers, hands)
    players = dict(players)
   
    #Dealing 7 cards for each player
    for player in players:
        players[player].add_cards(deck.deal(7))

    #Dealing top card
    top_card = deck.deal(1)[0]
    if top_card.card_type == "number":
        print(f"Top card is {top_card}")
    else:
        while top_card.card_type != "number":
            print(f"{top_card} can't be starting top card")
            top_card = deck.deal(1)[0]
            print(f"Top card is {top_card}\n")
    

    playing = True
    turn = 1
    playing_direction = 1


    while playing:

        while turn < len(players) + 1:
            print("---------------")
            print(f"Player number is: {turn}")
            print("Your hand is:")
            players[turn].cards_in_hand()
            print("---------------")
            print(f"Top card is {top_card}")
            print("---------------")
            choice = input("\nPlay or Draw? (p/d)")
            if choice == "p":
                idx = input("\nChoose index of card:")
                while int(idx) > players[turn].amount_of_cards():
                    print("Index out of range!\n")
                    idx = input("Choose index again:")
                pending_card = players[turn].chosen_card(int(idx))
                print(pending_card)
                while not valid_card(top_card, pending_card):
                        print("You can't play this card")
                        idx = input("Choose index again:")
                        pending_card = players[turn].chosen_card(int(idx))
                if valid_card(top_card, pending_card):
                    if pending_card.card_type == "number":
                        top_card = players[turn].remove_card(int(idx))
                        print(f"Top card is {top_card}")
                    elif pending_card.value == "SKIP":
                        top_card = players[turn].remove_card(int(idx))
                        print(f"Top card is {top_card}")
                        if playing_direction == 1:
                            if turn == len(players):
                                turn = 1
                            else:
                                turn += 1
                        else:
                            if turn == 1:
                                turn = len(players)
                            else:
                                turn -= 1 
                    elif pending_card.value == "REVERSE":
                        if int(num_of_players) > 2:
                            top_card = players[turn].remove_card(int(idx))
                            print(f"Top card is {top_card}")
                            playing_direction = playing_direction*(-1)
                        else:
                            if turn == len(players):
                                turn = 1
                            else:
                                turn += 1
                    elif pending_card.value == "DRAW_2":
                        top_card = players[turn].remove_card(int(idx))
                        print(f"Top card is {top_card}")
                        if playing_direction == 1:
                            if turn == len(players):
                                players[1].draw(deck.deal(2))
                            else:
                                players[turn + 1].draw(deck.deal(2))
                            if turn == len(players):
                                turn = 1
                            else:
                                turn += 1
                        else:
                            if turn == 1:
                                players[len(players)].draw(deck.deal(2))
                            else:
                                players[turn - 1].draw(deck.deal(2))
                            if turn == 1:
                                turn = len(players)
                            else:
                                turn -= 1
                    elif pending_card.value == "WILD":
                        wild_color = input("Choose: RED, GREEN, BLUE, YELLOW? (r/g/b/y)")
                        top_card = players[turn].remove_card(int(idx))
                        if wild_color == "r":
                            top_card.color = "RED"
                        elif wild_color == "g":
                            top_card.color = "GREEN"
                        elif wild_color == "b":
                            top_card.color = "BLUE"
                        elif wild_color == "y":
                            top_card.color = "YELLOW"
                        print(f"Top card is {top_card}")
                    elif pending_card.value == "WILD_DRAW_4":
                        wild4_color = input("Choose: RED, GREEN, BLUE, YELLOW? (r/g/b/y)")
                        top_card = players[turn].remove_card(int(idx))
                        if wild4_color == "r":
                            top_card.color = "RED"
                        elif wild4_color == "g":
                            top_card.color = "GREEN"
                        elif wild4_color == "b":
                            top_card.color = "BLUE"
                        elif wild4_color == "y":
                            top_card.color = "YELLOW"
                        print(f"Top card is {top_card}")
                        if playing_direction == 1:
                            if turn == len(players):
                                players[1].draw(deck.deal(4))
                            else:
                                players[turn + 1].draw(deck.deal(4))
                            if turn == len(players):
                                turn = 1
                            else:
                                turn += 1
                        else:
                            if turn == 1:
                                players[len(players)].draw(deck.deal(4))
                            else:
                                players[turn - 1].draw(deck.deal(4))
                            if turn == 1:
                                turn = len(players)
                            else:
                                turn -= 1

                    
                else:
                    print("You can't play this card")

            elif choice == "d":
                pending_card = deck.deal(1)
                pending_card_keep = pending_card
                pending_card = pending_card[0]
                print(f"Drawn card is {pending_card}")
                if not valid_card(top_card, pending_card):
                    print("You can't play this card")
                    players[turn].draw(pending_card_keep)
                    time.sleep(2)
                else:
                    draw_choice = input("Do you want PLAY or KEEP drawn card? (p/k)")
                    if draw_choice == "p":
                        if valid_card(top_card, pending_card):
                            if pending_card.card_type == "number":
                                top_card = pending_card
                                print(f"Top card is {top_card}")
                            elif pending_card.value == "SKIP":
                                top_card = pending_card
                                print(f"Top card is {top_card}")
                                if playing_direction == 1:
                                    if turn == len(players):
                                        turn = 1
                                    else:
                                        turn += 1
                                else:
                                    if turn == 1:
                                        turn = len(players)
                                    else:
                                        turn -= 1 
                            elif pending_card.value == "REVERSE":
                                top_card = pending_card
                                print(f"Top card is {top_card}")
                                playing_direction = playing_direction*(-1)
                            elif pending_card.value == "DRAW_2":
                                top_card = pending_card
                                print(f"Top card is {top_card}")
                                if playing_direction == 1:
                                    if turn == len(players):
                                        players[1].draw(deck.deal(2))
                                    else:
                                        players[turn + 1].draw(deck.deal(2))
                                    if turn == len(players):
                                        turn = 1
                                    else:
                                        turn += 1
                                else:
                                    if turn == 1:
                                        players[len(players)].draw(deck.deal(2))
                                    else:
                                        players[turn - 1].draw(deck.deal(2))
                                    if turn == 1:
                                        turn = len(players)
                                    else:
                                        turn -= 1
                            elif pending_card.value == "WILD":
                                wild_color = input("Choose: RED, GREEN, BLUE, YELLOW? (r/g/b/y)")
                                top_card = pending_card
                                if wild_color == "r":
                                    top_card.color = "RED"
                                elif wild_color == "g":
                                    top_card.color = "GREEN"
                                elif wild_color == "b":
                                    top_card.color = "BLUE"
                                elif wild_color == "y":
                                    top_card.color = "YELLOW"
                                print(f"Top card is {top_card}")
                            elif pending_card.value == "WILD_DRAW_4":
                                wild4_color = input("Choose: RED, GREEN, BLUE, YELLOW? (r/g/b/y)")
                                top_card = pending_card
                                if wild4_color == "r":
                                    top_card.color = "RED"
                                elif wild4_color == "g":
                                    top_card.color = "GREEN"
                                elif wild4_color == "b":
                                    top_card.color = "BLUE"
                                elif wild4_color == "y":
                                    top_card.color = "YELLOW"
                                print(f"Top card is {top_card}")
                                if playing_direction == 1:
                                    if turn == len(players):
                                        players[1].draw(deck.deal(4))
                                    else:
                                        players[turn + 1].draw(deck.deal(4))
                                    if turn == len(players):
                                        turn = 1
                                    else:
                                        turn += 1
                                else:
                                    if turn == 1:
                                        players[len(players)].draw(deck.deal(4))
                                    else:
                                        players[turn - 1].draw(deck.deal(4))
                                    if turn == 1:
                                        turn = len(players)
                                    else:
                                        turn -= 1
                    elif draw_choice == "k":
                        players[turn].draw(pending_card_keep)
            
            if win_checking(players[turn].amount_of_cards()):
                print(f"Player {turn} won!")
                turn = len(players) + 2
            else:
                if playing_direction == 1:
                    if turn >= len(players):
                        turn = 1
                    else:
                        turn += 1
                else:
                    if turn <= 1:
                        turn = len(players)
                    else:
                        turn -= 1

        
        if turn == len(players) + 2:
            playing = False
            
    play_again = input("Do you want to play again? (y/n)")
    if play_again == "y":
        continue
    else:
        print("\nThanks for playing!")
        game = False        
            
      