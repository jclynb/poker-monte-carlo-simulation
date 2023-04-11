from card import Card
from player import Player

class Deck:
    """ Initalizes 52 card deck. 
        Also creates a list of the 169 unique hole cards that a player can be dealt """
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