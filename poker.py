import random
import itertools
import pandas as pd
import numpy as np
"""
This program simulates rounds of poker to calculate probabilities of winning for 169 pocket cards.
The order goes as:
First deal cards to players and board (number of players in poker is usually between 2 to 10)
Use check_straight, check_flush, and check_num_counts to decide the Rank of each player's hand. (9 = straight flush -> 1 = high card)
Decide who wins by looking at the Rank values, and compare_hands if the ranks are equal.
"""

suits = np.array(["heart", "diamond", "spade", "club"])
numbers = np.array(range(2, 15, 1))
hearts = list(itertools.product(["heart"], numbers)) #13 hearts in deck
spades = list(itertools.product(["spade"], numbers)) #13 spades in deck

offsuit = [(card1, card2) for i, card1 in enumerate(hearts) for card2 in spades[i:]]
paired = [(card1, card2) for i, card1 in enumerate(hearts) for card2 in hearts[i+1:]]

pocketcards = offsuit + paired

deck = list(itertools.product(suits,numbers)) #list of 52 deck of cards
#pocketcards = list(itertools.combinations(itertools.product(suits_onlytwo, numbers), 2))  #list of 52 C 2 pocket cards

def check_straight(sevencards):
    wheel = {14, 2, 3, 4, 5} #special hand called "the wheel", ace can be low for straights
    card_values = [num[1] for num in sevencards]
    if wheel.issubset(set(sevencards)):
        return True, list(wheel)
    else:
        # O(<=N)
        for key, group in itertools.groupby(sorted(card_values), lambda i, j=itertools.count(): next(j)-i): #get groups of conescutive cards
            groups = list(group)
            if len(groups) >= 5: #5 consecutives cards is a straight
                return True, groups
            else:
                return False, None

def check_flush(sevencards): #checks if 5 cards are the same suit, returns cards in reverse order (highest card first)
    flush_heart = []
    flush_diamond = []
    flush_spade = []
    flush_club = []
    # O(n)
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

def check_num_counts(sevencards): #checks for pairs, full house
    card_values = sorted([num[1] for num in sevencards])
    val_counts = dict((val, card_values.count(val)) for val in set(card_values)) # FIXME? maybe expensive? unclear

    four = 4
    three = 3
    two = 2

    #sorts card_values (the player's hand) first by highest count then by card value, takes top 5 cards
    five_card_sorted_hand = sorted(card_values, key=lambda val: (val_counts[val], val), reverse=True)[0:5]

    if four in val_counts.values(): #four of a kind
        return 8, five_card_sorted_hand
    elif three in val_counts.values() and two in val_counts.values(): #full house
        return 7, five_card_sorted_hand
    elif three in val_counts.values(): #three of a kind
        return 4, five_card_sorted_hand
    elif len([key for key, val in val_counts.items() if val == 2]) >= 2: #finds length of card value list for pairs only, Two Pair
        return 3, five_card_sorted_hand
    elif two in val_counts.values(): #one pair
        return 2, five_card_sorted_hand
    else:                              #high card
        return 1, sorted(card_values, reverse=True)[0:5]

def compare_hands(a, b): #used for when players have the same type of hand, compares each list element to see who has the better hand (ex: the higher pair, high card, etc)
    for a_element, b_element in zip(a, b): #Returns 1 (a winds), 0 (equal), -1 (a loses)
        if a_element > b_element:
            return 1
        elif a_element < b_element:
            return -1
        else:
            return 0

def decide_winner(hand_ranks):
    hand_ranks = dict(sorted(hand_ranks.items(), key=lambda rank: rank[1][1])) #sort dict of hand_ranks by ranks
    pocket_cards = [values[0] for index, values in enumerate(hand_ranks.values())]

    """
    declare_winner assumes the player sorted "last" in hand ranks dict  won the round. Other players could have the same rank though.
    By rank I mean if player A has a flush, player B has a flush, and player C has two pair. A and B have the same rank, but could either tie
    or one player could have the larger high card. The next few lines create a new dict results and sets the sorted-last-player as "win".
    We compare hands after to possibly change this data.
    """

    highest_rank = list(hand_ranks.items())[-1][1][1] #get highest rank
    highest_rank_hand = list(hand_ranks.items())[-1][1][2] #get hand with highest rank (might not be best hand, just sorted last)
    highest_key = list(hand_ranks.items())[-1][0] #get player with highest rank
    highest_pocket_cards = list(hand_ranks.items())[-1][1][0]

    results = {key: None for key in pocket_cards}
    results[highest_pocket_cards] = "win"
    hand_ranks.pop(highest_key) #remove from dict

    #Compare the hands to make sure we have the real highest_rank_hand
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
        card1  = random.choice(round_deck) #randomly pick a card
        round_deck.remove(card1) #remove from deck
        card2 = random.choice(round_deck) #randomly pick a second card
        round_deck.remove(card2) #remove from deck
        hands[player] = (card1, card2)

    #Deal flop, turn, river
    board = []

    burn1 = random.choice(round_deck)
    round_deck.remove(burn1)

    flop1 = random.choice(round_deck)
    board.append(flop1)
    round_deck.remove(flop1)
    flop2 = random.choice(round_deck)
    board.append(flop2)
    round_deck.remove(flop2)
    flop3 = random.choice(round_deck)
    board.append(flop3)
    round_deck.remove(flop3)

    burn2 = random.choice(round_deck)
    round_deck.remove(burn2)

    turn = random.choice(round_deck)
    board.append(turn)
    round_deck.remove(turn)

    burn3 = random.choice(round_deck)
    round_deck.remove(burn3)

    river = random.choice(round_deck)
    board.append(river)



#    print("board: ", board)

    hand_ranks = {}
    for player, cards in enumerate(hands.values()):
        sevencards = list(cards) + board #player's pocket cards + board
        straight_bool, straight_hand = check_straight(sevencards)
        flush_bool, flush_hand = check_flush(sevencards)
        if straight_bool  and flush_bool and straight_hand == flush_hand: #straight flush
            hand_ranks["player_{}".format(player)] = (cards, 9, straight_hand)
        elif flush_bool:
            hand_ranks["player_{}".format(player)] = (cards, 6, flush_hand)
        elif straight_bool:
            hand_ranks["player_{}".format(player)] = (cards, 5, straight_hand)
        else:
            val, pairs_hand = check_num_counts(sevencards)
            hand_ranks["player_{}".format(player)] = (cards, val, pairs_hand)

    results_dict = decide_winner(hand_ranks)
    #print(results_dict)
    return results_dict

def simulate_poker(num_simulations):
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

    #wins_df = pd.DataFrame(win_probability.items(), columns = ["Cards", "Proability"])
    return(wins_df)
