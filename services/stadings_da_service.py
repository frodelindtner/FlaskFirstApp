from storage.db_teams import Storage_Team
from models.team import Team

class StandingsServiceLocal:
    def __init__(self):
        self.__storage = Storage_Team()
  
    def get_all_teams(self):
        return self.__storage.get_all_teams()

    def create_team(self, season, season_type, team_id, city, name, league, division):
        t = Team(season, season_type, team_id, city, name, league, division)
        self.__storage.add_team(t)
        return t

    def create_some_objects(self):
        self.create_team(2025, 1, 1, 'Horsholm', 'Hurricanes', 'ØST', 'The best')
        self.create_team(2025, 1, 2, 'Kokkedal', 'Klovns', 'ØST', 'The best')
        self.create_team(2025, 1, 3, 'Lyngby', 'Jokers', 'ØST', 'The best')
        self.create_team(2025, 1, 4, 'Ballerup', 'Vandals', 'ØST', 'The best')

 