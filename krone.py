import csv
from bl_data_loader import load_data
from bl_terminal_view import show_season_statistics, show_season_table
from bl_teams_sql import make_teams_sql_table
import argparse


def csv_to_list(file_path):

    season_data = []
    with open(file_path) as csvfile:
        d_reader = csv.DictReader(csvfile)

        # get fieldnames from DictReader object and store in list
        # headers = d_reader.fieldnames

        for line in d_reader:
            season_data.append(line)

    return season_data


def calculate_season_statistics(season_data):

    statistics = dict()

    statistics['total_games'] = sum(1 for line in season_data if line['FTHG'] and line['FTAG'])
    statistics['home_goals'] = sum(int(line['FTHG']) for line in season_data if line['FTHG'])
    statistics['away_goals'] = sum(int(line['FTAG']) for line in season_data if line['FTAG'])
    statistics['home_wins'] = sum(1 for line in season_data if int(line['FTHG']) > int(line['FTAG']))
    statistics['away_wins'] = sum(1 for line in season_data if int(line['FTHG']) < int(line['FTAG']))
    statistics['draws'] = sum(1 for line in season_data if int(line['FTHG']) == int(line['FTAG']))
    statistics['both_scored'] = sum(1 for line in season_data if int(line['FTHG']) > 0 and int(line['FTAG']))
    statistics['total15'] = sum(1 for line in season_data if int(line['FTHG']) + int(line['FTAG']) > 1)
    statistics['total25'] = sum(1 for line in season_data if int(line['FTHG']) + int(line['FTAG']) > 2)

    return statistics


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="krone project",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-l', '--loadData', required=False, help="Load data from Net", default=False)
    parser.add_argument('-db', '--buildDB', required=False, help="Create SQL database", default=True)

    args = parser.parse_args()

    if args.loadData:
        load_data()

    if args.buildDB:
        make_teams_sql_table(verbose=True)

# title = '2017/2018 B1'
# season_b1_17 = csv_to_list('./data/1718/D1.csv')
# stat = calculate_season_statistics(season_b1_17)
# show_season_statistics(title, stat)
# show_season_table(title, season_b1_17)

# print('________________________________________________________________________________________')
# print('________________________________________________________________________________________')
#
# title = '2016/2017 B1'
# season_b1_16 = csv_to_list('./data/1617/D1.csv')
# stat = calculate_season_statistics(season_b1_16)
# show_season_statistics(title, stat)
# show_season_table(title, season_b1_16)
#
# print('________________________________________________________________________________________')
# print('________________________________________________________________________________________')
#
# title = '2015/2016 B1'
# season_b1_15 = csv_to_list('./data/1516/D1.csv')
# stat = calculate_season_statistics(season_b1_15)
# show_season_statistics(title, stat)
# show_season_table(title, season_b1_15)
#
# print('________________________________________________________________________________________')
# print('________________________________________________________________________________________')
#
# title = '2017/2018 B2'
# season_b2_17 = csv_to_list('./data/1718/D2.csv')
# stat = calculate_season_statistics(season_b2_17)
# show_season_statistics(title, stat)
# show_season_table(title, season_b2_17)

# df = pd.read_csv('./data/D1.csv')
# df2 = df[['HomeTeam', 'AwayTeam']]
# print df2.head(10)
