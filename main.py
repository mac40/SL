'''
Main project file
'''

import csv_format_utilities as cfu


if __name__ == "__main__":
    # import games from games.csv
    GAMES = cfu.get_games('lolgames/games.csv')

    # clear games from duplicates
    GAMES = cfu.duplicates_handler(GAMES)

    # reformat teams
    GAMES = cfu.teams_to_list(GAMES)

    # reformat dates
    GAMES = cfu.change_date_format(GAMES)

    # save reformatted database
    cfu.save_games(GAMES, "parsed_games.csv")
