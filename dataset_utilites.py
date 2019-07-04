'''
function for creating useful datasets
'''

def get_top_ten(games, role):
    '''
    get top 10 played champions per role

    :param games: dataframe with all games
    :param role: lane for which we want the top ten
    '''
    top_ten = (games["{}_1".format(role)].value_counts() +
               games["{}_2".format(role)].value_counts()).dropna()
    top_ten = top_ten.sort_values(ascending=False)
    return top_ten.head(10).index.tolist()

def get_lane_adv(games, character, role):
    '''
    return the % of games played against the top 10 adversaries
    given a character and the lane in which he was played

    :param games: dataframe with all games
    :param character: character played
    :param role: lane in which the character was played
    '''
    top_ten_adv = ((games[games["{}_1".format(role)] == character]["{}_2".format(role)].value_counts() +
                    games[games["{}_2".format(role)] == character]["{}_1".format(role)].value_counts()).dropna())
    top_ten_adv = (top_ten_adv/(games[games["{}_1".format(role)] == character].shape[0] +
                                games[games["{}_2".format(role)] == character].shape[0])
                  ).sort_values(ascending=False)
    top_ten_adv = top_ten_adv[:10]
    return top_ten_adv.rename(character)

def get_winrate(games, character, role):
    '''
    given a character and a lane get the winrate

    :param games: dataframe with all games
    :param character: character played
    :param role: lane in which the character was played
    '''
    games_played = (games[games["{}_1".format(role)] == character].shape[0] +
                    games[games["{}_2".format(role)] == character].shape[0])
    games_won = (len(games[(games["{}_1".format(role)] == character)
                           & (games["result"] == "Victory")]) +
                 len(games[(games["{}_2".format(role)] == character)
                           & (games["result"] == "Defeat")]))
    return games_won/games_played

if __name__ == "__main__":
    pass
