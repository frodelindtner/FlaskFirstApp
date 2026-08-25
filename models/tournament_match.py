class TournamentMatch:
    def __init__(self, id, tournament_id, round_number, home_team_id, away_team_id, home_score=0, away_score=0, match_status='scheduled'):
        self.__id = id
        self.__tournament_id = tournament_id
        self.__round_number = round_number
        self.__home_team_id = home_team_id
        self.__away_team_id = away_team_id
        self.__home_score = home_score
        self.__away_score = away_score
        self.__match_status = match_status

    @property
    def id(self):
        return self.__id

    @property
    def tournament_id(self):
        return self.__tournament_id

    @property
    def round_number(self):
        return self.__round_number

    @property
    def home_team_id(self):
        return self.__home_team_id

    @property
    def away_team_id(self):
        return self.__away_team_id

    @property
    def home_score(self):
        return self.__home_score

    @home_score.setter
    def home_score(self, new_home_score):
        self.__home_score = new_home_score

    @property
    def away_score(self):
        return self.__away_score

    @away_score.setter
    def away_score(self, new_away_score):
        self.__away_score = new_away_score

    @property
    def match_status(self):
        return self.__match_status

    @match_status.setter
    def match_status(self, new_match_status):
        self.__match_status = new_match_status
