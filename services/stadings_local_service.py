from models.standing_dto import StandingDto
from models.result import Result
from models.team import Team

class StandingsServiceLocal:
    def __init__(self):
        pass

    def get_stadings(self, team_service, result_service) -> list[StandingDto]:
        standings = []        
        teams = team_service.get_all_teams()
        for team in teams:
            result = result_service.get_result_by_teamid(team.id)
            standing = StandingDto(team.season, 'N/A', team.id, team.city, team.name, team.league, team.division, 
                                   result.wins, result.losses,'N/A')
            standings.append(standing)
        return standings