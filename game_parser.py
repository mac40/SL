"""
This file is meant to parse the output from the spider in order to prepare various dataset to be
analyzed with R
"""

import pandas as pd

def teams_to_list(games):
    """The first action 
    """

def duplicates_handler(games):
    """In order to avoid unwanted interpreations of data we wish to remove
    duplicate games, i.e. games gathered twice from two different player
    since they were involved in the same game
    :param games: the list of games
    """
    return games.drop_duplicates(subset="timestamp")


if __name__ == "__main__":
    # import games from games.csv
    games = pd.read_csv('lolgames/games.csv')
    
    # clear games from duplicates
    games = duplicates_handler(games)

    # games["team_1"] = games["team_1"].apply(lambda x: x.split(","))
