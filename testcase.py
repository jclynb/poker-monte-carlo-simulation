import unittest
from card import Card
from player import Player
from playpokerround import PlayPokerRound

class TestBoardFunctions(unittest.TestCase):

    def test_flush(self):
        communitycards = [Card("heart", 2), Card("heart", 4), Card("heart", 6), Card("spade", 6), Card("spade", 14)]
        card1 = Card("heart", 10)
        card2 = Card("heart", 3)

        player = Player(card1, card2)
        player.get_sevencards(communitycards) 
        player.get_best_poker_hand()
        self.assertEqual(player.handrank, 5)
        self.assertEqual(player.hand, [10, 6, 4, 3, 2])
        
    def test_straight(self):
        communitycards = [Card("heart", 2), Card("heart", 4), Card("heart", 6), Card("spade", 5), Card("spade", 11)]
        card1 = Card("club", 14)
        card2 = Card("heart", 3)

        player = Player(card1, card2)
        player.get_sevencards(communitycards) 
        player.get_best_poker_hand()
        self.assertEqual(player.handrank, 4)
        self.assertEqual(player.hand, [6, 5, 4, 3, 2])

    def test_wheel(self):
        communitycards = [Card("heart", 2), Card("heart", 4), Card("heart", 3), Card("spade", 12), Card("spade", 7)]
        card1 = Card("club", 14)
        card2 = Card("heart", 5)

        player = Player(card1, card2)
        player.get_sevencards(communitycards)
        player.get_best_poker_hand()
        
        self.assertEqual(player.handrank, 4)
        self.assertEqual(player.hand, [5, 4, 3, 2, 1])
    

    def test_straight_flush(self):
        communitycards = [Card("heart", 7), Card("heart", 6), Card("heart", 5), Card("spade", 12), Card("spade", 7)]
        card1 = Card("heart", 4)
        card2 = Card("heart", 8)

        player = Player(card1, card2)
        player.get_sevencards(communitycards)
        player.get_best_poker_hand()
        
        self.assertEqual(player.handrank, 8)
        self.assertEqual(player.hand, [8, 7, 6, 5, 4])

    def test_wheel_straight_flush(self):
        communitycards = [Card("heart", 2), Card("heart", 4), Card("heart", 3), Card("spade", 12), Card("spade", 7)]
        card1 = Card("heart", 14)
        card2 = Card("heart", 5)

        player = Player(card1, card2)
        player.get_sevencards(communitycards)
        player.get_best_poker_hand()
        
        self.assertEqual(player.hand, [5, 4, 3, 2, 1])
        self.assertEqual(player.handrank, 8)


class TestPokerRound(unittest.TestCase):
    def test_round1(self):
        card1 = Card("spade", 14)    
        card2 = Card("club", 9)
        player1 = Player(card1, card2)

        card1 = Card("club", 9)    
        card2 = Card("diamond", 7)
        player2 = Player(card1, card2)

        card1 = Card("diamond", 13)    
        card2 = Card("club", 2)
        player3 = Player(card1, card2)

        pokerround = PlayPokerRound(3, player1)
        pokerround.players.append(player1)
        pokerround.players.append(player2)
        pokerround.players.append(player3)

        communitycards = [Card("diamond", 2), Card("heart", 4), Card("spade", 7), Card("heart", 10), Card("heart", 6)]
        for card in communitycards:
            pokerround.deal_communitycard(card)

        pokerround.get_handvalues() # Determine the value of each hand (9 = straight flush, 1 = High card)
        self.assertEqual(player1.handrank, 0)
        self.assertEqual(player1.hand, [14, 10, 9, 7, 6])

        self.assertEqual(player2.handrank, 1)
        self.assertEqual(player2.hand, [7, 7, 10, 9, 6])

        self.assertEqual(player3.handrank, 1)
        self.assertEqual(player3.hand, [2, 2, 13, 10, 7])

        self.assertFalse(pokerround.get_winner())

    def test_round2(self):
        card1 = Card("spade", 14)    
        card2 = Card("club", 9)
        player1 = Player(card1, card2)

        card1 = Card("diamond", 7)    
        card2 = Card("club", 2)
        player2 = Player(card1, card2)

        card1 = Card("diamond", 11)    
        card2 = Card("spade", 7)
        player3 = Player(card1, card2)

        card1 = Card("spade", 13)    
        card2 = Card("spade", 3)
        player4 = Player(card1, card2)

        pokerround = PlayPokerRound(4, player1)
        pokerround.players.append(player1)
        pokerround.players.append(player2)
        pokerround.players.append(player3)
        pokerround.players.append(player4)

        communitycards = [Card("diamond", 13), Card("heart", 5), Card("club", 14), Card("diamond", 14), Card("diamond", 3)]
        for card in communitycards:
            pokerround.deal_communitycard(card)

        pokerround.get_handvalues() # Determine the value of each hand (9 = straight flush, 1 = High card)
        self.assertEqual(player1.handrank, 3)
        self.assertEqual(player1.hand, [14, 14, 14, 13, 9])

        self.assertEqual(player2.handrank, 1)
        self.assertEqual(player2.hand, [14, 14, 13, 7, 5])

        self.assertEqual(player3.handrank, 1)
        self.assertEqual(player3.hand, [14, 14, 13, 11, 7])

        self.assertEqual(player4.handrank, 2)
        self.assertEqual(player4.hand, [14, 14, 13, 13, 5])

        self.assertTrue(pokerround.get_winner())

    def test_round3(self):
        card1 = Card("club", 4)    
        card2 = Card("spade", 7)
        player1 = Player(card1, card2)

        card1 = Card("heart", 6)    
        card2 = Card("club", 12)
        player2 = Player(card1, card2)

        card1 = Card("diamond", 12)    
        card2 = Card("diamond", 5)
        player3 = Player(card1, card2)

        pokerround = PlayPokerRound(3, player1)
        pokerround.players.append(player1)
        pokerround.players.append(player2)
        pokerround.players.append(player3)

        communitycards = [Card("club", 4), Card("heart", 2), Card("spade", 12), Card("heart", 4), Card("heart", 5)]
        for card in communitycards:
            pokerround.deal_communitycard(card)

        pokerround.get_handvalues() # Determine the value of each hand (9 = straight flush, 1 = High card)
        self.assertEqual(player1.handrank, 3)
        self.assertEqual(player1.hand, [4, 4, 4, 12, 7])

        self.assertEqual(player2.handrank, 1)
        self.assertEqual(player2.hand, [12, 12, 6, 5, 4])

        self.assertEqual(player3.handrank, 2)
        self.assertEqual(player3.hand, [12, 12, 5, 5, 4])

        self.assertTrue(pokerround.get_winner())
    
    def test_round4(self):
        card1 = Card("spade", 4)    
        card2 = Card("spade", 7)
        player1 = Player(card1, card2)

        card1 = Card("spade", 6)    
        card2 = Card("spade", 12)
        player2 = Player(card1, card2)

        card1 = Card("diamond", 12)    
        card2 = Card("diamond", 5)
        player3 = Player(card1, card2)

        pokerround = PlayPokerRound(3, player1)
        pokerround.players.append(player1)
        pokerround.players.append(player2)
        pokerround.players.append(player3)

        communitycards = [Card("club", 4), Card("spade", 2), Card("spade", 12), Card("spade", 4), Card("heart", 5)]
        for card in communitycards:
            pokerround.deal_communitycard(card)

        pokerround.get_handvalues() # Determine the value of each hand (9 = straight flush, 1 = High card)
        self.assertEqual(player1.handrank, 5)
        self.assertEqual(player1.hand, [12, 7, 4, 4, 2])

        self.assertEqual(player2.handrank, 5)
        self.assertEqual(player2.hand, [12, 12, 6, 4, 2])

        self.assertEqual(player3.handrank, 2)
        self.assertEqual(player3.hand, [12, 12, 5, 5, 4])

        self.assertFalse(pokerround.get_winner())