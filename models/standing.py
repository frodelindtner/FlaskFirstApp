from models.result import Result
from models.team import Team

# Multiple inheritance - Standing inherits from Team and Result
class Standing(Team, Result):
    def __init__(self, season, team_id, city, name, league, division, rteamid, wins, losses):
        Team.__init__(self, team_id, season, city, name, league, division)
        Result.__init__(self, rteamid, team_id, wins, losses)
        self.night_wins = 0
    
    def to_json(self):
        return {'season': self.season, 'season_type': self.season_type, 'team_id': self.team_id, 'city': self.city,
                'name': self.name, 'league': self.league, 'division': self.division, 'wins': self.wins, 'losses': self.losses,
                'night_wins': self.night_wins}
    

# Note could have used - Multiple level inheritance
# Team - Result inherits from Team, and Standing inherits form Result