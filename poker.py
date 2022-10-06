import random
import itertools
import pandas as pd
import numpy as np

#Create 52 card deck to deal from
suits = np.array(["heart", "diamond", "spade", "club"])
numbers = np.array(range(2, 15))
deck = list(itertools.product(suits,numbers))

#Get list of pocket cards. Don't want redundant values (ex: 2Heart 3Spade = 2Heart 3Club)
#Want 78 offsuit, 78 same suit, 13 pairs (AA, KK, QQ, etc)
hearts = list(itertools.product(["heart"], numbers)) # 13 hearts in deck
spades = list(itertools.product(["spade"], numbers)) # 13 spades in deck
offsuit = [(card1, card2) for i, card1 in enumerate(hearts) for card2 in spades[i:]] #78 + 13 pairs offsuit combinations
samesuit = [(card1, card2) for i, card1 in enumerate(hearts) for card2 in hearts[i+1:]] #78 same suit combinations

pocketcards = offsuit + samesuit #169 distinct value pocket cards


def check_straight(sevencards):
    """Checks if 5 of the sevencards (player's pocketcards + 5 cards on the board) are consecutive
       Checks special case when Ace is low"""
    wheel = {14, 2, 3, 4, 5} # special hand called "the wheel", ace (14 in this program) can be low for straights
    card_values = [num[1] for num in sevencards]
    if wheel.issubset(set(sevencards)):
        return True, list(wheel)
    else:
        for key, group in itertools.groupby(sorted(card_values), lambda i, j=itertools.count(): next(j)-i): #get groups of conescutive cards
            groups = list(group)
            if len(groups) >= 5: # 5 consecutives cards is a straight
                return True, groups
            else:
                return False, None

def check_flush(sevencards):
    """Checks if 5 of the sevencards are the same suit, returns the cards
       comprising the flush in reverse order (highest card first) if so."""
    flush_heart = []
    flush_diamond = []
    flush_spade = []
    flush_club = []
    for card in sevencards:
        if card[0] == 'heart':
            flush_heart.append(card[1])
        elif card[0] == 'diamond':
            flush_diamond.append(card[1])
        elif card[0] == 'spade':
            flush_spade.append(card[1])
        elif card[0] == 'club':
            flush_club.append(card[1])
    if len(flush_heart) >= 5:
        return True, sorted(flush_heart, reverse=True)
    elif len(flush_diamond) >= 5:
        return True, sorted(flush_diamond, reverse=True)
    elif len(flush_spade) >= 5:
        return True, sorted(flush_spade, reverse=True)
    elif len(flush_club) >= 5:
        return True, sorted(flush_club, reverse=True)
    else:
        return False, None

def check_num_counts(sevencards): 
    """Determines the best subset of cards in a hand (four of a kind,
       full house, three of a kind, two pair, one pair, or high card) and
       returns an int encoding the rank of the card set as well as """
    card_values = sorted([num[1] for num in sevencards]) #sorted list of the seven card values, ignore suits
    val_counts = dict((val, card_values.count(val)) for val in set(card_values))

    # sorts card_values first by highest count then by card value, takes top 5 cards
    # Ex: seven card list of [14, 4, 2, 9, 2, 3, 14] would be sorted as [14, 14, 2, 2, 9]
    five_card_sorted_hand = sorted(card_values, key=lambda val: (val_counts[val], val), reverse=True)[0:5]

    if 4 in val_counts.values(): # four of a kind
        return 8, five_card_sorted_hand
    elif 3 in val_counts.values() and 2 in val_counts.values(): # full house
        return 7, five_card_sorted_hand
    elif 3 in val_counts.values(): # three of a kind
        return 4, five_card_sorted_hand
    elif len([key for key, val in val_counts.items() if val == 2]) >= 2: # two pair
        return 3, five_card_sorted_hand
    elif 2 in val_counts.values(): # one pair
        return 2, five_card_sorted_hand
    else: # high card
        return 1, five_card_sorted_hand

def compare_hands(a, b): 
    """Breaks a tie between two hands `a` and `b` where each is of the same
       rank (four of a kind, full house, etc.) by seeing which hand has the
       higher valued cards. Returns 1 when `a` wins, 0 in the case of a true
       tie, and -1 when `b` wins."""    
    for a_element, b_element in zip(a, b):
        if a_element > b_element:
            return 1
        elif a_element < b_element:
            return -1
        else:
            return 0

def decide_winner(hand_ranks):
    """Decides the winner of the poker round. First checks for the highest rank,
       then compares hands for top pair/high cards/kickers if more than one player has the highest rank.
       Returns "results" dict with players' pocket cards + win, lose, or tie """
    hand_ranks = dict(sorted(hand_ranks.items(), key=lambda rank: rank[1][1])) #"sorts" dict by ordering the items by rank
    pocket_cards = [values[0] for index, values in enumerate(hand_ranks.values())]

    highest_rank = list(hand_ranks.items())[-1][1][1]
    highest_rank_hand = list(hand_ranks.items())[-1][1][2]
    highest_player = list(hand_ranks.items())[-1][0]
    highest_pocket_cards = list(hand_ranks.items())[-1][1][0]

    #start with the assumption that the last item in the dict is the winner (next step checks if other player's have the same type of hand)
    results = {key: None for key in pocket_cards}
    results[highest_pocket_cards] = "win"
    hand_ranks.pop(highest_player)

    # Compare the hands to make sure we have the real highest_rank_hand
    for index, (cards, rank, hand) in enumerate(hand_ranks.values()):
        if rank < highest_rank:
            results[cards] = "lose"
            continue
        else:
            cmp_val = compare_hands(hand, highest_rank_hand)
        if rank == highest_rank and cmp_val == 0:
            results[cards] = "tie"
            results[highest_pocket_cards] = "tie"
        elif rank == highest_rank and cmp_val == 1:
                results[cards] = "win"
                results[highest_pocket_cards] = "lose"
                highest_rank_hand = hand
                highest_pocket_cards = cards
        else:
            results[cards] = "lose"
    return results

def play_poker_round(num_players, pocketcards):
    """Plays a poker round with `num_players` players and with `pocketcards` (a tuple of 
       two cards) as the pocket cards of the distinguished player"""
    round_deck = deck.copy()
    hands = {key: None for key in range(num_players)}
    hands[0] = pocketcards # the distinguished player's pocket cards
    for player in range(1, num_players):
        card1  = random.choice(round_deck)
        round_deck.remove(card1)
        card2 = random.choice(round_deck)
        round_deck.remove(card2)
        hands[player] = (card1, card2)

    # Deal flop, turn, river
    board = []

    burn1 = random.choice(round_deck)
    round_deck.remove(burn1)

    for _ in range(3):
        flop = random.choice(round_deck)
        board.append(flop)
        round_deck.remove(flop)

    burn2 = random.choice(round_deck)
    round_deck.remove(burn2)

    turn = random.choice(round_deck)
    board.append(turn)
    round_deck.remove(turn)

    burn3 = random.choice(round_deck)
    round_deck.remove(burn3)

    river = random.choice(round_deck)
    board.append(river)

    # Determine the winner
    hand_ranks = {}
    for player, cards in enumerate(hands.values()):
        sevencards = list(cards) + board
        straight, straight_hand = check_straight(sevencards)
        flush, flush_hand = check_flush(sevencards)
        if straight and flush and straight_hand == flush_hand: # straight flush
            hand_ranks["player_{}".format(player)] = (cards, 9, straight_hand)
        elif flush:
            hand_ranks["player_{}".format(player)] = (cards, 6, flush_hand) #flush
        elif straight:
            hand_ranks["player_{}".format(player)] = (cards, 5, straight_hand) #straight
        else:
            val, pairs_hand = check_num_counts(sevencards)  #four of a kind, full house, three pair, two pair, one pair, high card
            hand_ranks["player_{}".format(player)] = (cards, val, pairs_hand)

    results_dict = decide_winner(hand_ranks)
    return results_dict

def simulate_poker(num_simulations):
    """Creates a pandas dataframe of the 169 pocket card win percentages varying by number of players (2-10).
       Calculates percentages by playing play_poker_round "num_simulations" times and counting how many times
       the pocketcard won the round."""
    wins_df = pd.DataFrame.from_dict({"Pocket Cards": pocketcards})
    for n in range (2,11):
        win_count = {key: 0 for key in pocketcards}
        for pocketcard in pocketcards:
            for i in range(num_simulations):
                results = play_poker_round(n, pocketcard)
                if results[pocketcard] == 'win':
                    win_count[pocketcard] += 1
        win_probability = {key: value / num_simulations for key, value in win_count.items()}

        wins_df["Win % for " + str(n) + " players"] = wins_df["Pocket Cards"].map(win_probability)

    return(wins_df)
