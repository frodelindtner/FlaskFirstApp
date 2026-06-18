import requests
import json

class Minitest_team:
    def __init__(self, season, division, name):
        self.season = season
        self.division = division
        self.name = name

test_jsonstring = '[{"Season":2026,"SeasonType":1,"Division":"Central", "Name":"White Sox"},' \
'               {"Season":2026,"SeasonType":1,"Division":"Central", "Name":"Black Sox"}]'
sports_test = json.loads(test_jsonstring)
print(f"Number of teams: {len(sports_test)}")

for sportteam in sports_test:
    testminie = Minitest_team(sportteam['Season'], sportteam['Division'], sportteam['Name'])
    print(f'{testminie.name} - {testminie.season} - {testminie.division}')

# avc = [{"Season":2026,"SeasonType":1,"TeamID":16,"Key":"CHW","City":"Chicago",
#   "Name":"White Sox","League":"AL","Division":"Central","Wins":38,"Losses":33,
#   "Percentage":0.5352112676056338028169014085,"DivisionWins":12,"DivisionLosses":5,
#   "GamesBehind":0.00,"LastTenGamesWins":6,"LastTenGamesLosses":4,"Streak":"L1",
#   "LeagueRank":4,"DivisionRank":2,"WildCardRank":2,"WildCardGamesBehind":-2.50,"HomeWins":24,
#   "HomeLosses":12,"AwayWins":14,"AwayLosses":21,"DayWins":16,"DayLosses":17,"NightWins":22,
#   "NightLosses":16,"RunsScored":335,"RunsAgainst":333,"GlobalTeamID":10000016,
#   "ClinchedBestLeagueRecord":false,"ClinchedWildCard":false,"ClinchedDivision":false,
#   "EliminatedFromPlayoffContention":false}]


# sports_url = 'https://api.sportsdata.io/v3/mlb/scores/json/Standings/2026?key=2fa1bf790451403ba1cb8303bb749b58'
# req_sports = requests.get(sports_url)
# sports_data = json.loads(req_sports.text)

# print(f"Number of teams: {len(sports_data)}")

# for sport_team in sports_data:
#     cur_team = team.Team(sport_team['Season'],
#                 sport_team['SeasonType'],
#                 sport_team['TeamID'],
#                 sport_team['City'],
#                 sport_team['Name'],
#                 sport_team['League'],
#                 sport_team['Division'],
#                 sport_team['Wins'],
#                 sport_team['Losses'],
#                 sport_team['NightWins'])
#     print(f'{cur_team.name} - {cur_team.season} - {cur_team.division} - night wins: {cur_team.night_wins}')
