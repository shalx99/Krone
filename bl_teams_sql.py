
import sqlite3
from bl_data_loader import csv_to_list, data_files


def team_id(team):
    return team.strip().lower()


def all_teams(verbose=False):

    teams = set()
    files = data_files()
    for file in files:
        season = csv_to_list(file)
        teams = teams.union( set([team_id(game['HomeTeam']) for game in season]))

    # clean-up empty string
    teams = filter(None, teams)
    teams = sorted(teams)

    return list(teams)


def create_teams_table(teams):
    connection = sqlite3.connect("bundesliga.db")
    cursor = connection.cursor()

    for team in teams:
        sql_command = """INSERT INTO teams (id, name, full_name, short_name) VALUES (NULL, "{name}", "{full_name}", "{short_name}"); """\
            .format(name=team[0], full_name=team[1], short_name=team[2])
        cursor.execute(sql_command)

    connection.commit()
    connection.close()


def add_manual_data(teams):
    updated_teams = list()
    for team in teams:
        if team =='dortmund': team_data=(team, 'Borussia Dortmund', 'BVB')
        elif team == 'leverkusen': team_data=(team, 'Bayer Leverkusen', 'B04')
        elif team == 'schalke': team_data=(team, 'Schalke 04','S04')
        elif team == 'hertha': team_data=(team, 'Hertha BSC','BSC')
        elif team == 'werder': team_data=(team, 'Werder Bremen',"SVW")
        elif team == 'bayern': team_data=(team,  'Bayern Munich',"FCB")
        elif team == 'wolfsburg': team_data=(team,  'VfL Wolfsburg', "WOB")
        elif team == 'hoffenheim': team_data=(team,  '1899 Hoffenheim', "TSG")
        elif team == 'hamburg': team_data=(team,  'Hamburger SV', "HSV")
        elif team == 'darmstadt': team_data=(team,  '', "D98")
        elif team == 'leipzig': team_data=(team,  'RB Leipzig', "RBL")
        elif team == 'ingolstadt': team_data=(team,  '', "FCI")
        elif team == "m'gladbach": team_data=(team,  'Borussia Mönchengladbach', "BMG")
        elif team == 'freiburg': team_data=(team,  'SC Freiburg', "SCF")
        elif team == 'frankfurt': team_data=(team,  'Eintracht Frankfurt', "SGE")
        elif team == 'augsburg': team_data=(team,  'FC Augsburg', "FCA")
        elif team == 'koln': team_data=(team,  '1. FC Köln', "KOE")
        elif team == 'mainz': team_data=(team,  'Mainz 05', "M05")
        elif team == 'stuttgart': team_data = (team, 'VfB Stuttgart', "VFB")
        elif team == 'hannover': team_data = (team, 'Hannover 96', "H96")

        else: team_data = (team, '', '')

        updated_teams.append(team_data)

    return updated_teams


def make_teams_sql_table(verbose=False):
    teams = all_teams(verbose)

    if verbose:
        print('Total number of teams: {0}'.format(len(teams)))
        print(" \n".join(teams))

    updated_teams = add_manual_data(teams)
    create_teams_table(updated_teams)