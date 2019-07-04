'''
Main project file
'''

# import pandas as pd

import csv_format_utilities as cfu
import dataset_utilites as du

def basic_parser():
    '''
    basic parsing of scraped games
    '''
    # import games from games.csv
    games = cfu.get_games('lolgames/games.csv')

    # clear games from duplicates
    games = cfu.duplicates_handler(games)

    # reformat teams
    games = cfu.teams_to_list(games)

    # reformat dates
    games = cfu.change_date_format(games)

    # remove grandmaster games
    games = cfu.remove_rows(games, 'mmr', 'Grandmaster')

    # save reformatted database
    cfu.save_games(games, "parsed_games.csv")


if __name__ == "__main__":

    basic_parser()

    GAMES = cfu.get_games('parsed_games.csv')

    TOP_TOP = du.get_top_ten(GAMES, 'top')
    for val in TOP_TOP:
        print(du.get_lane_adv(GAMES, val, 'top'))
