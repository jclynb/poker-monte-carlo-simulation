import random
from deck import Deck 
from player import Player

class PlayPokerRound:
    """ Plays a poker round to deal two cards from deck to "num_players" and five cards to the "communitycards", 
        and checks if player1 wins """
    def __init__(self, num_players, player1):
        self.num_players = num_players
        self.player1 = player1
        self.players = []
        self.communitycards = []

    def deal_communitycard(self, card):
        self.communitycards.append(card)

    def deal(self):
        # Deal two cards to each player then deal 5 cards to communitycards
        # Remove dealt cards from deck
        # Add each player to list "self.players"
        deck = Deck()
        self.players.append(self.player1)
        card1, card2 = self.player1.get_cards()
        deck.remove(card1)
        deck.remove(card2)

        for player in range(1, self.num_players):
            card1 = random.choice(deck.deck)
            deck.remove(card1)
            card2 = random.choice(deck.deck)
            deck.remove(card2)
            self.players.append(Player(card1, card2))

        # Deal flop
        burn1 = random.choice(deck.deck)
        deck.remove(burn1)

        for _ in range(3):
            flop = random.choice(deck.deck)
            self.deal_communitycard(flop) # Add card to board
            deck.remove(flop)

        # Deal river and turn
        for _ in range(2):
            burncard = random.choice(deck.deck)
            deck.remove(burncard)

            turn_river = random.choice(deck.deck)
            self.deal_communitycard(turn_river)
            deck.remove(turn_river)

    def get_handvalues(self):
        # Determine the best 5 card hand and ranking of each player
        # updates (int) player.handrank and (list) player.hand
        for player in self.players:
            player.get_sevencards(self.communitycards) # list of 5 community cards + player's 2 hole cards
            player.get_best_poker_hand()

            """ debugging:
            player.card1.print_card()
            player.card2.print_card()
            print("hand: ", player.hand)
            print("rank: ", player.handrank)
            for card in self.communitycards:
                card.print_card()
            print("\n") """

    def get_winner(self):
        """ Determines if player1 won the round. First checks if player1 has the highest rank,
        and if so the compares hands for top pair/high cards/kickers if one or more oppoents have the same rank.
        Returns True if player1 wins, or False if player1 lost or tied """
        self.players.sort(key=lambda x: x.handrank) # sort players by hand value
 
        if self.player1.handrank < self.players[0].handrank:
            return False

        # Check if opponents have the same type of hand
        player1_rank = self.player1.handrank
        player1_hand = self.player1.hand
        self.players.remove(self.player1)

        for opponent in self.players:
            if player1_rank > opponent.handrank:
                continue
            else:
                cmp_val = opponent.compare_hands(player1_hand, opponent.hand)

            if opponent.handrank == player1_rank and cmp_val == 0:
                return False # Tie
            elif opponent.handrank == player1_rank and cmp_val == -1:
                return False # Player1 lost

        return True