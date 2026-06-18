from models import team
import requests
import json

class StandingsService:
    def __init__(self):
        self.__sportsurl = 'https://api.sportsdata.io/v3/mlb/scores/json/Standings/2026?key=2fa1bf790451403ba1cb8303bb749b58'
    
    def get_stadings(self):
        req_sports = requests.get(self.__sportsurl)
        sports_data = json.loads(req_sports.text)
        teams = []

        for sport_team in sports_data:
            cur_team = team.Team(sport_team['Season'],
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
    
