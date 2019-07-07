'''
Main project file
'''

import sys

import pandas as pd

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
    cfu.save_games(games, "./datasets/parsed_games.csv")


def role_winrate_vs(role):
    '''
    create a dataset with the winrate and the playrate vs the most frequent
    adversaries of the most played characters in the given role

    :param role: the role we want the dataset to focus on
    '''
    # retrieve parsed games
    games = cfu.get_games('./datasets/parsed_games.csv')

    # get the top ten characters for the lane
    top_played_char = du.get_top_ten(games, role)

    # get top chars info for the role
    win_vs_pr = pd.DataFrame()
    for char in top_played_char:
        # get lane adv of top played champions
        win_vs_pr = win_vs_pr.append(du.get_lane_adv(games, char, role))
    win_vs_pr = win_vs_pr.fillna(0)
    win_vs_pr = win_vs_pr.transpose()

    # get top adversaries winrate
    for char in win_vs_pr.index.values:
        for adv in win_vs_pr.columns.values:
            win_vs_pr[adv][char] = du.get_winrate_vs(games, char, role, adv)
    cfu.save_dataset(win_vs_pr, './datasets/{}_winrate_vs.csv'.format(role))


if __name__ == "__main__":

    try:
        if sys.argv[1] == "Parse":
            print("Executing basic_parser...")
            basic_parser()
        else:
            print("Command not recognized")
            print("Doing nothing...")
    except IndexError:
        pass

    role_winrate_vs('top')
    role_winrate_vs('jung')
    role_winrate_vs('mid')
    role_winrate_vs('adc')
    role_winrate_vs('supp')
