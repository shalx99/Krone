
import sqlite3
from bl_data_loader import csv_to_list, data_files
from bl_teams_sql import team_id


def all_games(verbose=False):

    games = list()
    files = data_files()

    if verbose:
        print(len(files))
        print(" \n".join(files))

    for file in files:
        season = csv_to_list(file)
        for game in season:
            home_shots = ''
            away_shots = ''
            home_shots_target = ''
            away_shots_target = ''
            if 'HS' in game: home_shots = game['HS']
            if 'AS' in game: away_shots = game['AS']
            if 'HST' in game: home_shots_target = game['HST']
            if 'AST' in game: away_shots_target = game['AST']
            games.append((game['Div'], game['Date'], team_id(game['HomeTeam']), team_id(game['AwayTeam']),
                          game['FTHG'], game['FTAG'], game['FTR'], home_shots, away_shots, home_shots_target, away_shots_target))

    # clean-up empty string
    games = [game for game in games if game[0]]

    return games


def create_games_table(games):

    print ('total games number: {}'.format(len(games)) )
    connection = sqlite3.connect("bundesliga.db")
    cursor = connection.cursor()

    for game in games:
        sql_command = """INSERT INTO games (id, div, date, home_team, away_team, home_team_goals, away_team_goals, full_time_result, ht_shots, at_shots, ht_shots_target, at_shots_target) 
            VALUES (NULL, "{div}", "{date}", "{home_team}", "{away_team}", {home_team_goals}, {away_team_goals}, "{full_time_result}", "{home_s}", "{away_s}","{hst}","{ast}"); """\
            .format(div=game[0], date=game[1], home_team=game[2], away_team=game[3], home_team_goals=int(game[4]), away_team_goals=int(game[5]), full_time_result=game[6],
                    home_s=game[7], away_s=game[8], hst=game[9], ast=game[10])

        cursor.execute(sql_command)

    connection.commit()
    connection.close()


def make_games_sql_table(verbose=False):
    games = all_games(verbose=False)
    create_games_table(games)