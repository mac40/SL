"""
This file is meant to parse the output from the spider in order to prepare various dataset to be
analyzed with R
"""

import pandas as pd


def get_games(file_name):
    """
    get games from csv and return them in a pandas dataframe
    :param file_name: name of the csv file containing the games
    """
    return pd.read_csv(file_name)


def save_games(dataframe, file_name):
    """
    save games in a csv from a pandas df
    :param dataframe: pandas dataframe containing games
    :param file_name: destination file .csv
    """
    dataframe.to_csv(file_name, index=False)


def duplicates_handler(games):
    """
    In order to avoid unwanted interpreations of data we wish to remove
    duplicate games, i.e. games gathered twice from two different player
    since they were involved in the same game

    :param games: the list of games
    """
    return games.drop_duplicates(subset="timestamp")


def teams_to_list(games):
    """
    In order to work more easily with teamcomps we will change their
    field from a csv style into a python list

    :param games: the list of games
    """
    games["team_1"] = games["team_1"].apply(lambda x: x.split(","))
    games[["top_1", "jung_1", "mid_1", "adc_1", "supp_1"]] = pd.DataFrame(
        games.team_1.values.tolist(), index=games.index)
    games = games.drop(columns="team_1")
    games["team_2"] = games["team_2"].apply(lambda x: x.split(","))
    games[["top_2", "jung_2", "mid_2", "adc_2", "supp_2"]] = pd.DataFrame(
        games.team_2.values.tolist(), index=games.index)
    games = games.drop(columns="team_2")
    return games


def change_date_format(games):
    """
    To allow time operations in R we need to change date format

    :param games: the list of games
    """
    games["timestamp"] = games["timestamp"].apply(lambda x: x[:10])
    games["timestamp"] = pd.to_datetime(games["timestamp"])
    return games


if __name__ == "__main__":
    pass
