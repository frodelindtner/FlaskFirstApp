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

    def create_filters(self):
        """
        Creating filter on the data in teams - league
        """
        created_teams = self.get_all_teams()
        leagues = []
        for team in created_teams:
            leagues.append(team.league)

        league_unique = list(set(leagues))        
        return league_unique

    def create_some_objects(self, result_service):
        self.create_team(2026, 'Hørsholm', 'Hurricanes', 'Øst', '1 division', result_service)
        self.create_team(2026, 'Kokkedal', 'Pirats', 'Øst', '1 division', result_service)
        self.create_team(2026, 'Lyngby', 'Jokers', 'Øst', '1 division', result_service)
        self.create_team(2026, 'Ballerup', 'Vandals', 'Øst', '1 division', result_service)
        self.create_team(2026, 'Odense', 'Wolwes', 'Central', '1 division', result_service)
        self.create_team(2026, 'Odense', 'Giants', 'Central', '1 division', result_service)
        self.create_team(2026, 'Øksendrup', 'Oysters', 'Central', '1 division', result_service)
        self.create_team(2026, 'Aarhus', 'Royals', 'Vest', '1 division', result_service)
        self.create_team(2026, 'Herning', 'Trolls', 'Vest', '1 division', result_service)

 