from models.team_result import TeamResult
from models.result import Result
from models.team import Team
import requests
import json

class StandingsServiceUS:
    def __init__(self):
        self.__sportsurl = 'https://api.sportsdata.io/v3/mlb/scores/json/Standings/2026?key=2fa1bf790451403ba1cb8303bb749b58'

    def get_stadings(self) -> list[TeamResult]:
        req_sports = requests.get(self.__sportsurl)
        sports_data = json.loads(req_sports.text)
        teams = []

        for sport_team in sports_data:
            cur_team = TeamResult(sport_team['Season'],
                sport_team['SeasonType'],
                sport_team['TeamID'],
                sport_team['City'],
                sport_team['Name'],
                sport_team['League'],
                sport_team['Division'],
                sport_team['Wins'],
                sport_team['Losses'],
                sport_team['NightWins'])
            teams.append(cur_team)
        return teams
    
    def get_team(self) -> list[Team]:
        req_sports = requests.get(self.__sportsurl)
        sports_data = json.loads(req_sports.text)
        teams = []

        for sport_team in sports_data:
            cur_team = TeamResult(sport_team['Season'],
                sport_team['SeasonType'],
                sport_team['TeamID'],
                sport_team['City'],
                sport_team['Name'],
                sport_team['League'],
                sport_team['Division'])
            teams.append(cur_team)
        return teams

    def get_result(self, id) -> list[Result]:
        req_sports = requests.get(self.__sportsurl)
        sports_data = json.loads(req_sports.text)
        results = []

        for sport_team in sports_data:
            cur_result = TeamResult(sport_team['TeamID'],
                sport_team['Wins'],
                sport_team['Losses'],
                sport_team['NightWins'])
            results.append(cur_result)
        return results
 