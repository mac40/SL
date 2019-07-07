'''
Main project file
'''

import sys

import pandas as pd

import csv_format_utilities as cfu
import dataset_utilites as du

from constants import DAMAGE, TANK, RANGED

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
    cfu.save_dataset(win_vs, './datasets/winrate/{}_winrate_vs.csv'.format(role))


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
    cfu.save_games(
        jung_inf_merged, './datasets/jung_inf/{}/{}_jung_inf.csv'.format(role, char))


def stat_dataset():
    '''
    generic statistics dataset
    '''

    games = cfu.get_games('./datasets/parsed_games.csv')

    dataset = pd.DataFrame(columns=[
        'damage_1', 'tank_1', 'range_1', 'damage_2', 'tank_2', 'range_2', 'result'])

    for game in games.iterrows():
        row = pd.Series([0, 0, 0, 0, 0, 0, 'Victory'], index=[
                        'damage_1', 'tank_1', 'range_1', 'damage_2', 'tank_2', 'range_2', 'result'])
        for role in ['top', 'jung', 'mid', 'adc', 'supp']:
            if DAMAGE[game[1]['{}_1'.format(role)]] == 'AD':
                row['damage_1'] += 1
            if TANK[game[1]['{}_1'.format(role)]] == 'YES':
                row['tank_1'] += 1
            if RANGED[game[1]['{}_1'.format(role)]] == 'YES':
                row['range_1'] += 1
            if DAMAGE[game[1]['{}_2'.format(role)]] == 'AD':
                row['damage_2'] += 1
            if TANK[game[1]['{}_2'.format(role)]] == 'YES':
                row['tank_2'] += 1
            if RANGED[game[1]['{}_2'.format(role)]] == 'YES':
                row['range_2'] += 1
        for index in ['damage_1', 'tank_1', 'range_1', 'damage_2', 'tank_2', 'range_2']:
            row[index] = row[index]/5
        row['result'] = game[1]['result']
        dataset = dataset.append(row, ignore_index=True)
    cfu.save_games(dataset, './datasets/stats.csv')

def train_test():
    '''
    create train and test datasets
    '''
    games = cfu.get_games('./datasets/stats.csv')

    train = pd.DataFrame(columns=[
        'damage_1', 'tank_1', 'range_1', 'damage_2', 'tank_2', 'range_2', 'result'])

    victory = 0
    defeat = 0
    for game in games.iterrows():
        row = pd.Series(data=[game[1]['damage_1'], game[1]['tank_1'], game[1]['range_1'],
                              game[1]['damage_2'], game[1]['tank_2'], game[1]['range_2'], game[1]['result']], index=[
                                  'damage_1', 'tank_1', 'range_1', 'damage_2', 'tank_2', 'range_2', 'result'])
        if game[1]['result'] == 'Victory' and victory < 500:
            victory += 1
            train = train.append(row, ignore_index=True)
        if game[1]['result'] == 'Defeat' and defeat < 500:
            defeat += 1
            train = train.append(row, ignore_index=True)
        if victory == 500 and defeat == 500:
            break
    print(train)
    cfu.save_games(train, './datasets/train.csv')


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

    for ROLE in ['top', 'jung', 'mid', 'adc', 'supp']:
        role_winrate_vs(ROLE)

    # GAMES = cfu.get_games('./datasets/parsed_games.csv')

    # for ROLE in ['top', 'mid', 'adc', 'supp']:
    #     top_char = du.get_top_ten(GAMES, ROLE)
    #     for CHAR in top_char:
    #         jungle_influence(CHAR, ROLE)


    # stat_dataset()

    train_test()
