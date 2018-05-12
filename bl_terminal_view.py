from terminaltables import AsciiTable

def show_season_statistics(header, statistics):

    home_wins_pt = statistics['home_wins'] * 100 / statistics['total_games']
    draws_pt = statistics['draws'] * 100 / statistics['total_games']
    away_wins_pt = statistics['away_wins'] * 100 / statistics['total_games']
    results = '{}: {} matches, home wins: {:.1f}%, draws: {:.1f}%, away wins: {:.1f}%'.format(header,
                                                                                              statistics['total_games'],
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

    print(results)
    print(perform + totals)
    print('')

def calculate_season_outcomes(team, season_data):
    ''' returns team season results in form WWLDW '''
    outcomes = ''
    all_team_games = [game for game in season_data if game['HomeTeam'] == team or game['AwayTeam'] == team and game['FTAG']]

    for game in all_team_games:
        if game['HomeTeam'] == team:
            if int(game['FTHG']) > int(game['FTAG']):
                outcomes += 'W'
            elif int(game['FTHG']) < int(game['FTAG']):
                outcomes += 'L'
            else:
                outcomes += 'D'

        if game['AwayTeam'] == team:
            if int(game['FTHG']) > int(game['FTAG']):
                outcomes += 'L'
            elif int(game['FTHG']) < int(game['FTAG']):
                outcomes += 'W'
            else:
                outcomes += 'D'

    return outcomes

def show_season_table(title, season_data):
    table_data = []
    table_header = ['Platz', 'Club', 'Spiele', ' S ', ' U ', ' N ', 'Tore', 'TD', 'Punkte', 'Form']

    teams = set()
    for game in season_data:
        teams.add(game['HomeTeam'])
        teams.add(game['AwayTeam'])

    for team in teams:
        home_team_games = [game for game in season_data if game['HomeTeam'] == team and game['FTHG'] and game['FTAG']]
        away_team_games = [game for game in season_data if game['AwayTeam'] == team and game['FTHG'] and game['FTAG']]
        all_team_games = [game for game in season_data if game['HomeTeam'] == team or game['AwayTeam'] == team and game['FTAG']]

        #home games
        win  = sum(1 for game in home_team_games if int(game['FTHG']) > int(game['FTAG']))
        lose = sum(1 for game in home_team_games if int(game['FTHG']) < int(game['FTAG']))
        draw = sum(1 for game in home_team_games if int(game['FTHG']) == int(game['FTAG']))
        scored = sum(int(game['FTHG']) for game in home_team_games)
        conceded = sum(int(game['FTAG']) for game in home_team_games)
        form = calculate_season_outcomes(team, season_data)

        #away games
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
        table_row[table_header.index('Form')] = ' ' + form[-6:] + '  '

        table_data.append(table_row)

    table_data.sort(key=lambda x: int(x[table_header.index('TD')]), reverse=True) # sort on secondary key
    table_data.sort(key=lambda x: x[table_header.index('Punkte')], reverse = True) # sort on primary key

    for idx, table_row in enumerate(table_data):
        table_row[table_header.index('Platz')] = ' ' + '{:>3}'.format(str(idx+1)) + '  '

    table_data.insert(0, table_header)
    table = AsciiTable(table_data, title)
    print (table.table)