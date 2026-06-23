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
        t = Team(None, season, city, name, league, division)
        createdid = self.__storage.add_team(t)

        # Added result data
        result_service.create_empty_result(teamid=createdid)
        return t

    def update_team(self, id, season, city, name, league, division):
        t = Team(id, season, city, name, league, division)
        self.__storage.update_team(t)
        return t

    def delete_team(self, id):
        self.__storage.delete_team(id)

    def create_some_objects(self, result_service):
        self.create_team(2026, 'Hørsholm', 'Hurricanes', 'ØST', '1 division', result_service)
        self.create_team(2026, 'Kokkedal', 'Pirats', 'ØST', '1 division', result_service)
        self.create_team(2026, 'Lyngby', 'Jokers', 'ØST', '1 division', result_service)
        self.create_team(2026, 'Ballerup', 'Vandals', 'ØST', '1 division', result_service)
        self.create_team(2026, 'Aarhus', 'Royals', 'VEST', '1 division', result_service)
        self.create_team(2026, 'Odense', 'Wolwes', 'VEST', '1 division', result_service)
        self.create_team(2026, 'Herning', 'Trolls', 'VEST', '1 division', result_service)
        self.create_team(2026, 'Odense', 'Giants', 'VEST', '1 division', result_service)

 