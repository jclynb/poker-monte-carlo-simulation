from collections import defaultdict
import itertools
from card import Card

class Player:
    def __init__(self, card1, card2):
        self.card1 = card1
        self.card2 = card2
        self.holecard_type = None
        self.sevencards = [] # 5 card hand from community cards + hole cards
        self.hand = None  # Best 5 card hand
        self.handrank = -1 

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
    
    def get_sevencards(self, communitycards):
        card1, card2 = self.get_cards()
        self.sevencards.append(card1)
        self.sevencards.append(card2)
        self.sevencards.extend(communitycards)
    
    def compare_hands(self, a, b):
        """ Breaks a tie between two hands `a` and `b` where each is of the same
       rank (four of a kind, full house, etc.) by seeing which hand has the
       higher valued cards. Returns 1 when `a` wins, 0 in the case of a true
       tie, and -1 when `b` wins. """
        for a_element, b_element in zip(a, b):
            if a_element > b_element:
                return 1
            elif a_element < b_element:
                return -1
        return 0
    
    def get_best_poker_hand(self):
        # Updates self.hand and self.handrank with the highest ranking 5 card hand combination from sevencards
        for combination in itertools.combinations(self.sevencards, 5): # 7 choose 5 combinations
            ranks = [card.rank for card in combination]
            suits = [card.suit for card in combination]
            
            # Check for royal flush
            if set(ranks) == {14, 13, 12, 11, 10} and len(set(suits)) == 1:
                ranking = 9 
            # Check for straight flush
            elif len(set(suits)) == 1 and max(ranks) - min(ranks) == 4 and len(set(ranks)) == 5:
                ranking = 8
            # Check for four of a kind
            elif len(set(ranks)) == 2 and (ranks.count(ranks[0]) == 1 or ranks.count(ranks[0]) == 4):
                ranking = 7
            # Check for full house
            elif len(set(ranks)) == 2:
                ranking = 6 
            # Check for flush
            elif len(set(suits)) == 1:
                if set(ranks) == {14, 2, 3, 4, 5}: # special case wheel (ace is low)
                    ranking = 8
                    for i in range(len(ranks)):
                        if ranks[i] == 14:
                            ranks[i] = 1
                else:
                    ranking = 5
            # Check for straight
            elif (max(ranks) - min(ranks) == 4) and len(set(ranks)) == 5:
                ranking = 4 
            # Check for wheel (ace is low)
            elif set(ranks) == {14, 2, 3, 4, 5}:
                ranking = 4
                for i in range(len(ranks)):
                    if ranks[i] == 14:
                        ranks[i] = 1
            # Check for three of a kind
            elif any(ranks.count(rank) == 3 for rank in set(ranks)):
                ranking = 3
            # Check for two pair (ex: [5 5 6 6 8] -> set(5 6 8))
            elif len(set(ranks)) == 3:
                ranking = 2
            # Check for one pair
            elif len(set(ranks)) == 4:
                ranking = 1
            # Else high card
            else:
                ranking = 0
            
            if ranking > self.handrank:
                self.handrank = ranking
                self.hand = sorted(ranks, reverse=True)
            
            # If the current combination has the same ranking as the current best handrank, 
            # sort the combination then compare the two hands
            elif ranking == self.handrank:
                curr_hand = sorted(ranks, reverse=True)
                cmp = self.compare_hands(curr_hand, self.hand)
                if cmp == 1:
                    self.hand = curr_hand