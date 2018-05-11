from terminaltables import AsciiTable
from urllib.request import urlopen
import os
import csv
import pandas as pd


def loadfile(url):
    u = urlopen(url)

    data_directory = "./data/"
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    file_name = data_directory + url.split('/')[-1]

    try:
        file_size = os.path.getsize(file_name)
    except OSError:
        print ('Warning: {} data file is missing completely'.format(file_name))
        file_size = 0

    remote_file_size = int(u.getheader('Content-Length'))

    if file_size == remote_file_size:
        print('Data file {} is up to date'.format(file_name))

    else:
        f = open(file_name, 'wb')
        print("Downloading: {} Bytes: {}".format(file_name, remote_file_size))

        file_size_dl = 0
        block_sz = 8192
        while True:
            buff = u.read(block_sz)
            if not buff:
                break

            file_size_dl += len(buff)
            f.write(buff)

        f.close()

    return file_name


def csv_to_list(file_path):
    season_data = []
    with open(file_path) as csvfile:
        d_reader = csv.DictReader(csvfile)

        # get fieldnames from DictReader object and store in list
        # headers = d_reader.fieldnames

        for line in d_reader:
            season_data.append(line)

    return season_data


def print_season_statistics(header, season_data):

    statistics = {}

    statistics['total_games'] = sum(1 for line in season_data if line['FTHG'] and line['FTAG'])
    statistics['home_goals'] = sum(int(line['FTHG']) for line in season_data if line['FTHG'])
    statistics['away_goals'] = sum(int(line['FTAG']) for line in season_data if line['FTAG'])
    statistics['home_wins'] = sum(1 for line in season_data if int(line['FTHG']) > int(line['FTAG']))
    statistics['away_wins'] = sum(1 for line in season_data if int(line['FTHG']) < int(line['FTAG']))
    statistics['draws'] = sum(1 for line in season_data if int(line['FTHG']) == int(line['FTAG']))
    statistics['both_scored'] = sum(1 for line in season_data if int(line['FTHG']) > 0 and int(line['FTAG']))
    statistics['total15'] = sum(1 for line in season_data if int(line['FTHG']) + int(line['FTAG']) > 1)
    statistics['total25'] = sum(1 for line in season_data if int(line['FTHG']) + int(line['FTAG']) > 2)

    home_wins_pt = statistics['home_wins'] * 100 / statistics['total_games']
    draws_pt = statistics['draws'] * 100 / statistics['total_games']
    away_wins_pt = statistics['away_wins'] * 100 / statistics['total_games']
    results = '{}: {} matches, home wins: {:.1f}%, draws: {:.1f}%, away wins: {:.1f}%'.format(header, statistics['total_games'],
                                                                                              home_wins_pt, draws_pt,
                                                                                              away_wins_pt)

    goals_avg = float(statistics['home_goals'] + statistics['away_goals']) / statistics['total_games']
    both_scored_pt = statistics['both_scored'] * 100 / statistics['total_games']
    total15_pt = statistics['total15'] * 100 / statistics['total_games']
    total25_pt = statistics['total25'] * 100 / statistics['total_games']
    away_goals_avg = statistics['away_goals'] / statistics['total_games']
    home_goals_avg = statistics['home_goals'] / statistics['total_games']

    perform = '{:.1f} goals per game, both scored: {:.1f}%, '.format(goals_avg, both_scored_pt)

    totals = '1.5+:{:.1f}%, 2.5+:{:.1f}% hAvgGoals:{:.1f}, gAvgGoals:{:.1f}'.format(total15_pt, total25_pt,
                                                                                    home_goals_avg, away_goals_avg)

    print (results)
    print (perform + totals)
    print ('')


def print_season_table(title, season_data):
    table_data = []
    table_header = ['Platz', 'Club', 'Spiele', ' S ', ' U ', ' N ', 'Tore', 'TD', 'Punkte']

    teams = set()
    for game in season_data:
        teams.add(game['HomeTeam'])
        teams.add(game['AwayTeam'])

    for team in teams:
        home_team_games = [game for game in season_data if game['HomeTeam'] == team and game['FTHG'] and game['FTAG']]
        away_team_games = [game for game in season_data if game['AwayTeam'] == team and game['FTHG'] and game['FTAG']]

        scored, conceded = 0, 0
        win, draw, lose = 0, 0, 0

        win  += sum(1 for game in home_team_games if int(game['FTHG']) > int(game['FTAG']))
        lose += sum(1 for game in home_team_games if int(game['FTHG']) < int(game['FTAG']))
        draw += sum(1 for game in home_team_games if int(game['FTHG']) == int(game['FTAG']))
        scored += sum(int(game['FTHG']) for game in home_team_games)
        conceded += sum(int(game['FTAG']) for game in home_team_games)


        win  += sum(1 for game in away_team_games if int(game['FTHG']) < int(game['FTAG']))
        lose += sum(1 for game in away_team_games if int(game['FTHG']) > int(game['FTAG']))
        draw += sum(1 for game in away_team_games if int(game['FTHG']) == int(game['FTAG']))
        scored += sum(int(game['FTAG']) for game in away_team_games)
        conceded += sum(int(game['FTHG']) for game in away_team_games)

        table_row = [''] * len(table_header)
        table_row[table_header.index('Club')] = team
        table_row[table_header.index('Spiele')] = '  ' + str(len(home_team_games) + len(away_team_games)) + '  '
        table_row[table_header.index('Tore')] = ' ' + str(scored) + ' - ' + str(conceded) + ' '
        table_row[table_header.index('TD')] = ' ' + '{:>3}'.format(str(scored - conceded)) + '  '
        table_row[table_header.index(' S ')] = '{:>2}'.format(str(win))
        table_row[table_header.index(' U ')] = '{:>2}'.format(str(draw))
        table_row[table_header.index(' N ')] = '{:>2}'.format(str(lose))
        table_row[table_header.index('Punkte')] = ' ' + '{:>3}'.format(str(win * 3 + draw)) + '  '

        table_data.append(table_row)

    table_data.sort(key=lambda x: int(x[table_header.index('TD')]), reverse=True) # sort on secondary key
    table_data.sort(key = lambda x: x[table_header.index('Punkte')], reverse = True) # sort on primary key

    for idx, table_row in enumerate(table_data):
        table_row[table_header.index('Platz')] = ' ' + '{:>3}'.format(str(idx+1)) + '  '

    table_data.insert(0, table_header)
    table = AsciiTable(table_data, title)
    print (table.table)


loadfile("http://www.football-data.co.uk/mmz4281/1718/D1.csv")
loadfile("http://www.football-data.co.uk/mmz4281/1718/D2.csv")

season_b1_17 = csv_to_list('./data/D1.csv')
print_season_statistics('2017/2018 B1', season_b1_17)
print_season_table('2017/2018 B1', season_b1_17)

print ('________________________________________________________________________________________')
print ('________________________________________________________________________________________')

season_b2_17 = csv_to_list('./data/D2.csv')
print_season_statistics('2017/2018 B2', season_b2_17)
print_season_table('2017/2018 B2', season_b2_17)

#df = pd.read_csv('./data/D1.csv')
#df2 = df[['HomeTeam', 'AwayTeam']]
#print df2.head(10)
