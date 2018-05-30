
import sqlite3
from bl_data_loader import csv_to_list


def all_teams(verbose=False):
    teams = set()
    years = list(range(93, 100)) + list(range(0, 19))
    files = list()
    prev_year = 0
    for year in years:
        if not prev_year:
            prev_year = year
            continue
        files.append('./data/{0:02d}{1:02d}/D1.csv'.format(prev_year, year))
        files.append('./data/{0:02d}{1:02d}/D2.csv'.format(prev_year, year))
        prev_year = year

    if verbose:
        print('Files to scan: {0}'.format(len(files)))

    for file in files:
        season = csv_to_list(file)
        for game in season:
            teams.add(game['HomeTeam'])
            teams.add(game['AwayTeam'])

    # clean-up empty string
    teams = filter(None, teams)

    return list(teams)


def create_teams_table(teams):
    connection = sqlite3.connect("bundesliga.db")
    cursor = connection.cursor()

    # delete
    cursor.execute("""DROP TABLE teams;""")

    create_table_command = ("        CREATE TABLE teams ( \n"
                            "        id INTEGER PRIMARY KEY, \n"
                            "        name VARCHAR(30),\n"
                            "        full_name VARCHAR(70),\n"
                            "        short_name VARCHAR(3));")

    cursor.execute(create_table_command)

    for team in teams:
        sql_command = """INSERT INTO teams (id, name, full_name, short_name) VALUES (NULL, "{name}", "{full_name}", "{short_name}"); """\
            .format(name=team[0], full_name=team[1], short_name=team[2])
        cursor.execute(sql_command)

    connection.commit()
    connection.close()


def make_games_sql_table(verbose=False):
    teams = all_teams(verbose)

    if verbose:
        print('Total number of teams: {0}'.format(len(teams)))
        print(" \n".join(teams))

    updated_teams = add_manual_data(teams)
    create_teams_table(updated_teams)