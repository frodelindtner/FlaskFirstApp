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
            standings.sort(key=lambda x: int(x.wins), reverse=True)

        return standings

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
        standings_dto = self.get_stadings_us()
        filtered_list = []
        for standing_dto in standings_dto:
            if standing_dto.league == filter:
                filtered_list.append(standing_dto)

        return filtered_list
 