from storage.db_teams import Storage_Team
from models.team import Team

class TeamService:
    def __init__(self):
        self.__storage = Storage_Team()
  
    def get_all_teams(self):
        return self.__storage.get_all_teams()

    def get_team_by_id(self, id):
        teams = self.__storage.get_all_teams()
        for team in teams:
            if team.id == id:
                return team
        else:
            return None


    def create_team(self, id, season, city, name, league, division):
        t = Team(id, season, city, name, league, division)
        self.__storage.add_team(t)
        return t

    def create_some_objects(self):
        self.create_team(10001, 2026, 'Horsholm', 'Hurricanes', 'ØST', '1 division')
        self.create_team(10002, 2026, 'Kokkedal', 'Klovns', 'ØST', '1 division')
        self.create_team(10003, 2026, 'Lyngby', 'Jokers', 'ØST', '1 division')
        self.create_team(10004, 2026, 'Ballerup', 'Vandals', 'ØST', '1 division')

 