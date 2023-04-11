# ♣️♦️ Poker Monte Carlo Simulation ♥️♠️
## [Monte carlo simulation](https://en.wikipedia.org/wiki/Monte_Carlo_method) of Texas Hold'em.
Want a stochastic algorithm to help decide when to call, raise, or fold 'em before the flop?

This program runs 5000 poker rounds for 169 non-equivalent starting [hole cards](https://en.wikipedia.org/wiki/Texas_hold_%27em_starting_hands) from a range of 2 players to 10 players. The win percentages are tracked in dictionary win_count.

The results can then be used to analyze the probability of having the best hand pre-flop given two cards and the number of opponents. 

This program stores the results in a pandas dataframe to use for further analysis, and also exports these results to an excel file.


## Run Locally

Clone the project

```bash
  git clone git@github.com:jclynb/poker-monte-carlo-simulation.git
```

Go to the project directory

```bash
  cd poker-monte-carlo-simulation
```

Install dependencies

```bash
  pip install pandas
```

Run the program

```bash
  python3 main.py
```


## Running Tests

To run tests, run the following command

```bash
  python -m unittest testcase.py
```

