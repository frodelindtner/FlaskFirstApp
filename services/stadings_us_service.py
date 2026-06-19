from models.standing_dto import StandingDto
from models.result import Result
from models.team import Team
import requests
import json

class StandingsServiceUS:
    def __init__(self):
        self.__sportsurl = 'https://api.sportsdata.io/v3/mlb/scores/json/Standings/2026?key=2fa1bf790451403ba1cb8303bb749b58'

    def get_stadings_dto(self) -> list[StandingDto]:
        req_sports = requests.get(self.__sportsurl)
        sports_data = json.loads(req_sports.text)
        standings_dto = []

        for sport_item in sports_data:
            standing_dto = StandingDto(sport_item['Season'],
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
    

    def get_standings_dto_filter_by_league(self, filter) -> list[StandingDto]:
        standings_dto = self.get_stadings_dto()
        filtered_list = []
        for standing_dto in standings_dto:
            if standing_dto.league == filter:
                filtered_list.append(standing_dto)

        return filtered_list

    def get_teams(self) -> list[Team]:
        standings_dto = self.get_stadings_dto()
        teams = []
        for standing_dto in standings_dto:
            team = Team(standing_dto.team_id,
                        standing_dto.season,
                        standing_dto.season_type,
                        standing_dto.city,
                        standing_dto.name,
                        standing_dto.league,
                        standing_dto.division)
            teams.append(team)
        return teams

    def get_results(self) -> list[Result]:
        standings_dto = self.get_stadings()
        results = []
        result_id = 10000
        for standing_dto in standings_dto:
            result = Result(result_id, 
                            standing_dto.team_id, 
                            standing_dto.wins, 
                            standing_dto.losses, 
                            standing_dto.night_wins )
            results.append(result)
            result_id += 1
        return results
 