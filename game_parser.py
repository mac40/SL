'''
This file is meant to parse the output from the spider in order to prepare various dataset to be
analyzed with R
'''

import pandas as pd


if __name__ == "__main__":
    # import games from games.csv
    games = pd.read_csv('lolgames/games.csv')