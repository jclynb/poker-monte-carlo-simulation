import pandas as pd
from playpokerround import PlayPokerRound
from deck import Deck
import testcase

def main():
    """ Creates a pandas dataframe of the 169 hole card win percentages varying by number of players (2-10).
       Calculates percentages by playing a full round of poker num_simulation times and counting how many times
       the holecards won the round. (all players play all the way through, no betting or folding) """

    deck = Deck()
    deck.get_uniqueholecards()
    num_simulations = 5000

    wins_df = pd.DataFrame.from_dict({"Hole Cards": deck.uniqueholecards})
    for num_players in range (2,11):
        win_count = {key: 0 for key in deck.uniqueholecards}
        for holecards in deck.uniqueholecards:
            for _ in range(num_simulations):
                pokerround = PlayPokerRound(num_players, holecards)
                pokerround.deal() # Deal two cards to each player and five cards to the board
                pokerround.get_handvalues() # Determine the value of each hand (9 = straight flush, 1 = High card)
                if pokerround.get_winner(): # Return true if the player with "holecards" had the best hand
                    win_count[holecards] += 1

        win_probability = {key: value / num_simulations for key, value in win_count.items()}

        wins_df["Win % for " + str(num_players) + " players"] = wins_df["Hole Cards"].map(win_probability)
    print("done")
    return wins_df

if __name__ == "__main__":
    testcase.unittest.main()
    df = main()
    df.to_excel("poker_win_percentages.xlsx")
