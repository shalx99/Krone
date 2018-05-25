import csv


def csv_to_list(file_path):

    season_data = list()
    with open(file_path, encoding='iso-8859-15') as f:
        reader = csv.DictReader(f)

        for line in reader:
            season_data.append(line)

    return season_data


def all_teams():
    teams = set()
    years = list(range(93, 100)) + list(range(0, 19))
    files = list()
    prev_year = ''
    for year in years:
        if not prev_year:
            prev_year = year
            continue
        files.append('./data/{0:02d}{1:02d}/D1.csv'.format(prev_year, year))
        prev_year = year

    for file in files:
        season = csv_to_list(file)
        for game in season:
            teams.add(game['HomeTeam'])
            teams.add(game['AwayTeam'])

    return list(teams)


