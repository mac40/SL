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
    win_vs = pd.DataFrame()
    for char in top_played_char:
        # get lane adv of top played champions
        win_vs = win_vs.append(du.get_lane_adv(games, char, role))
    win_vs = win_vs.fillna(0)
    win_vs = win_vs.transpose()

    # get top adversaries winrate
    for char in win_vs.index.values:
        for adv in win_vs.columns.values:
            win_vs[adv][char] = du.get_winrate_vs(games, char, role, adv)
    cfu.save_dataset(win_vs, './datasets/{}_winrate_vs.csv'.format(role))


def jungle_influence(char, role):
    '''
    create a dataset for a char in a role different from jungle
    in which every entry shows which jungler was played in that game
    and the result of the game

    :param char: name of the character in question
    :param role: name of the role in which the char was played different from jung
    '''
    if role == 'jung':
        print('Cannot create jungle influence for junglers')
        return

    # retrieve parsed games
    games = cfu.get_games('./datasets/parsed_games.csv')

    jung_inf_1 = games[games['{}_1'.format(role)] == char][[
        'jung_1', 'result']]
    jung_inf_1 = jung_inf_1.rename(
        index=str, columns={'jung_1': 'jung', 'result': 'result'})
    jung_inf_2 = games[games['{}_2'.format(role)] == char][[
        'jung_2', 'result']]
    jung_inf_2['result'] = jung_inf_2['result'].apply(
        lambda x: 'Defeat' if x == 'Victory' else 'Victory')
    jung_inf_2 = jung_inf_2.rename(
        index=str, columns={'jung_2': 'jung', 'result': 'result'})
    jung_inf_merged = pd.concat([jung_inf_1, jung_inf_2], ignore_index=True)
    jung_inf_merged['result'] = jung_inf_merged['result'].apply(
        lambda x: 1 if x == 'Victory' else 0)
    cfu.save_dataset(
        jung_inf_merged, './datasets/{}_{}_jung_inf.csv'.format(char, role))


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

    for role in ['top', 'jung', 'mid', 'adc', 'supp']:
        role_winrate_vs(role)

    GAMES = cfu.get_games('./datasets/parsed_games.csv')

    for role in ['top', 'mid', 'adc', 'supp']:
        top_char = du.get_top_ten(GAMES, role)
        for char in top_char:
            jungle_influence(char, role)
