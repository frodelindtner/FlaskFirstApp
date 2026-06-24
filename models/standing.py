class Standing:
    def __init__(self, season, season_type, team_id, city, name, league, division, wins, losses, night_wins):
        self.season = season
        self.season_type = season_type
        self.team_id = team_id
        self.city = city
        self.name = name
        self.league = league
        self.division = division
        self.wins = wins
        self.losses = losses
        self.night_wins = night_wins
    
    def to_json(self):
        return {'season': self.season, 'season_type': self.season_type, 'team_id': self.team_id, 'city': self.city,
                'name': self.name, 'league': self.league, 'division': self.division, 'wins': self.wins, 'losses': self.losses,
                'night_wins': self.night_wins}