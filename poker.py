import random
import itertools
import pandas as pd
import numpy as np
from collections import defaultdict
import board

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def print_card(self):
        print(f'{self.rank}{self.suit}' )

class Player:
    def __init__(self, card1, card2):
        self.card1 = card1
        self.card2 = card2
        self.hand = None # 5 card hand from community cards + hole cards
        self.handrank = None
        self.holecard_type = None

    def get_cards(self):
        return self.card1, self.card2

    def get_holecard_type(self):
        if self.card1.rank == self.card2.rank:
            self.holecard_type = "pocket pair"
        elif self.card1.suit == self.card2.suit and (self.card1.rank == self.card2.rank + 1 or self.card1.rank == self.card2.rank - 1):
            self.holecard_type = "suited connector"
        elif self.card1.suit == self.card2.suit:
            self.holecard_type = "suited, not connected"
        elif self.card1.rank == self.card2.rank + 1 or self.card1.rank == self.card2.rank - 1:
            self.holecard_type = "offsuit connector"
        else:
            self.holecard_type = "offsuit, not connected, not paired"

class Deck:
    """ Initalizes 52 card deck. Also creates a list of the 169 unique hole cards/pocket cards that a player can be dealt """
    def __init__(self):
        self.suits = ["heart", "diamond", "spade", "club"]
        self.ranks = [num for num in range(2, 15)] # 14 = Ace, 13 = King
        self.deck = [Card(s, r) for s in self.suits for r in self.ranks]
        self.uniqueholecards = None

    def get_uniqueholecards(self):
        # Get list of unique hole cards. Don't want redundant values (ex: 2Heart 3Spade = 2Heart 3Club; both 2, 3 offsuit connector)
        # Want 78 offsuit, 78 same suit, 13 pairs (AA, KK, QQ, etc)
        hearts = [Card("heart", r) for r in self.ranks] # 13 hearts in deck
        spades = [Card("spade", r) for r in self.ranks] # 13 spades in deck
        offsuit = [Player(card1, card2) for i, card1 in enumerate(hearts) for card2 in spades[i:]] # 78 + 13 pairs offsuit combinations
        suited = [Player(card1, card2) for i, card1 in enumerate(hearts) for card2 in hearts[i+1:]] # 78 same suit combinations
        self.uniqueholecards = offsuit + suited

    def remove(self, card):
        for deckcard in self.deck:
            if deckcard.suit == card.suit and deckcard.rank == card.rank:
                del card 
                break

class PlayPokerRound:
    """ Plays a poker round to deal two cards from deck to num_players, and checks if player1 wins """
    def __init__(self, num_players, player1):
        self.num_players = num_players
        self.distinguishedplayer = player1
        self.players = []
        self.board = Board()


    def deal(self):
        # Deal two cards to each player then deal 5 cards to the board
        deck = Deck()
        self.players.append(self.distinguishedplayer)
        card1, card2 = self.distinguishedplayer.get_cards()
        deck.remove(card1)
        deck.remove(card2)

        # Deal pocket cards to the other players
        for player in range(1, self.num_players):
            card1 = random.choice(deck.deck)
            deck.remove(card1)
            card2 = random.choice(deck.deck)
            deck.remove(card2)
            self.players.append(Player(card1, card2))

        # Deal flop, turn, river
        burn1 = random.choice(deck.deck)
        deck.remove(burn1)

        for _ in range(3):
            flop = random.choice(deck.deck)
            self.board.deal_communitycard(flop) # Add card to board
            deck.remove(flop)

        burn2 = random.choice(deck.deck)
        deck.remove(burn2)

        turn = random.choice(deck.deck)
        self.board.deal_communitycard(turn)
        deck.remove(turn)

        burn3 = random.choice(deck.deck)
        deck.remove(burn3)

        river = random.choice(deck.deck)
        self.board.deal_communitycard(river)

    # Determine the value of each player's hand
    def get_handvalues(self):
        for player in self.players:
            self.board.check_straight(player)
            self.board.check_flush(player)
            if self.board.is_flush and self.board.is_straight:
                player.handrank = 9
            else:
                self.board.check_rank_counts(player)

            # Reset board for next player
            self.board.reset()

    def compare_hands(self, a, b):
        """ Breaks a tie between two hands `a` and `b` where each is of the same
       rank (four of a kind, full house, etc.) by seeing which hand has the
       higher valued cards. Returns -1 when `a` wins, 0 in the case of a true
       tie, and 1 when `b` wins. """
        for a_element, b_element in zip(a, b):
            if a_element > b_element:
                return -1
            elif a_element < b_element:
                return 1
        return 0

    def get_winner(self):
        """ Determines if player1 won the round. First checks if player1 has the highest rank,
        and if so the compares hands for top pair/high cards/kickers if one or more oppoents have the same rank.
        Returns True if player1 wins, or False if player1 lost or tied """

        self.players.sort(key=lambda x: x.handrank) # sort players by hand value

        if self.distinguishedplayer.handrank < self.players[0].handrank:
            return False

        # Check if opponents have the same type of hand
        player_rank = self.distinguishedplayer.handrank
        player_hand = self.distinguishedplayer.hand

        self.players.remove(self.distinguishedplayer)

        for opponent in self.players:
            if player_rank > opponent.handrank:
                continue
            else:
                cmp_val = self.compare_hands(opponent.hand, player_hand)

            if opponent.handrank == player_rank and cmp_val == 0:
                return False # Tie
            elif opponent.handrank == player_rank and cmp_val == -1:
                return False # Player1 lost

        return True

def main():
    """ Creates a pandas dataframe of the 169 hole card win percentages varying by number of players (2-10).
       Calculates percentages by playing a full round of poker 5000 times and counting how many times
       the holecards won the round. (all players play all the way through, no betting or folding) """

    deck = Deck()
    deck.get_uniqueholecards()
    num_simulations = 5

    wins_df = pd.DataFrame.from_dict({"Hole Cards": deck.uniqueholecards})
    for num_players in range (2,11):
        win_count = {key: 0 for key in deck.uniqueholecards}
        for holecards in deck.uniqueholecards:
            for _ in range(num_simulations):
                pokerround = PlayPokerRound(num_players, holecards)
                pokerround.deal()
                pokerround.get_handvalues()
                if pokerround.get_winner():
                    win_count[holecards] += 1

        win_probability = {key: value / num_simulations for key, value in win_count.items()}

        wins_df["Win % for " + str(num_players) + " players"] = wins_df["Hole Cards"].map(win_probability)
    print("done")
    return wins_df

if __name__ == "__main__":
    df = main()
