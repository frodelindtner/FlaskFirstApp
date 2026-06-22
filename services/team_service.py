from storage.db_teams import Storage_Team
from models.team import Team

class TeamService:
    def __init__(self):
        self.__storage = Storage_Team()
  
    def get_all_teams(self):
        return self.__storage.get_all_teams()

    def get_team_by_id(self, id):
        team = self.__storage.get_team_by_id(id)
        return team

    def create_team(self, season, city, name, league, division, result_service):
        t = Team(season, city, name, league, division)
        createdid = self.__storage.add_team(t)

        print(createdid)
        # Added result data
        result_service.create_empty_result(teamid=createdid)
        return t

    def update_team(self, id, season, city, name, league, division):
        t = Team(season, city, name, league, division)
        t.id = id
        self.__storage.update_team(t)
        return t

    def create_some_objects(self, result_service):
        self.create_team(2026, 'Horsholm', 'Hurricanes', 'ØST', '1 division', result_service)
        self.create_team(2026, 'Kokkedal', 'Klovns', 'ØST', '1 division', result_service)
        self.create_team(2026, 'Lyngby', 'Jokers', 'ØST', '1 division', result_service)
        self.create_team(2026, 'Ballerup', 'Vandals', 'ØST', '1 division', result_service)

 