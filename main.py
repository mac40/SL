'''
Main project file
'''

import pandas as pd

import csv_format_functions as cff


if __name__ == "__main__":
    # import games from games.csv
    GAMES = pd.read_csv('lolgames/games.csv')

    # clear games from duplicates
    GAMES = cff.duplicates_handler(GAMES)

    # reformat teams
    GAMES = cff.teams_to_list(GAMES)

    # reformat dates
    GAMES = cff.change_date_format(GAMES)

    # save reformatted database
    GAMES.to_csv("parsed_games.csv", index=False)
