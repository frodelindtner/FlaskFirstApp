from models.standing import Standing
import requests
import json

class StandingsService:
    def __init__(self):
        self.__sportsurl = 'https://api.sportsdata.io/v3/mlb/scores/json/Standings/2026?key=2fa1bf790451403ba1cb8303bb749b58'

    def get_stadings_local(self, team_service, result_service) -> list[Standing]:
        """ 
        Getting local standings
        """
        standings = []        
        teams = team_service.get_all_teams()
        for team in teams:
            result = result_service.get_result_by_teamid(team.id)
            standing = Standing(team.season, 'N/A', team.id, team.city, team.name, team.league, team.division, 
                                   result.wins, result.losses,'N/A')
            standings.append(standing)
            # sort - no new copy
            # sorted - creates copy
            # standings.sort(key=lambda x: int(x.wins), reverse=True)
            # with accounted for losses
            standings.sort(key=lambda x: (int(x.wins), int(-x.losses)), reverse=True)

        return standings
    
    def get_standing_local_filter_by_league(self, team_service, result_service, filter) -> list[Standing]:
        """
        Filter local standing with league
        """
        standings = self.get_stadings_local(team_service, result_service)
        return self.filter_standings(standings, filter)

    def get_stadings_us(self) -> list[Standing]:
        """
        Getting USA standings by API
        """
        req_sports = requests.get(self.__sportsurl)
        sports_data = json.loads(req_sports.text)
        standings_dto = []

        for sport_item in sports_data:
            standing_dto = Standing(sport_item['Season'],
                sport_item['SeasonType'],
                sport_item['TeamID'],
                sport_item['City'],
                sport_item['Name'],
                sport_item['League'],
                sport_item['Division'],
                sport_item['Wins'],
                sport_item['Losses'],
                sport_item['NightWins'])
            standings_dto.append(standing_dto)
        return standings_dto
    
    def get_standings_us_filter_by_league(self, filter) -> list[Standing]:
        """
        Filter USA API data
        """
        standings = self.get_stadings_us()
        return self.filter_standings(standings, filter)
 
    def filter_standings(self, standings, filter_value):
        f_standings = []
        for standing in standings:
            if standing.league == filter_value:
                f_standings.append(standing)

        return f_standings

 # ----------------- JSON ---------------

    def get_all_local_standings_json(self, team_service, result_service):
        standings = self.get_stadings_local(team_service, result_service)
        json_res = []
        for standing in standings:
            json_res.append(standing.to_json())
        return json_res