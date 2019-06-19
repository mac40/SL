"""
This file is meant to parse the output from the spider in order to prepare various dataset to be
analyzed with R
"""

import pandas as pd


def duplicates_handler(games):
    """In order to avoid unwanted interpreations of data we wish to remove
    duplicate games, i.e. games gathered twice from two different player
    since they were involved in the same game
    :param games: the list of games
    """
    return games.drop_duplicates(subset="timestamp")


def teams_to_list(games):
    """ In order to work more easily with teamcomps we will change their
    field from a csv style into a python list
    :param games: the list of games
    """
    games["team_1"] = games["team_1"].apply(lambda x: x.split(","))
    games["team_2"] = games["team_2"].apply(lambda x: x.split(","))
    return games

if __name__ == "__main__":
    # import games from games.csv
    games = pd.read_csv('lolgames/games.csv')
    
    # clear games from duplicates
    games = duplicates_handler(games)

    # reformat teams
    games = teams_to_list(games)

    print(games.head())