class TournamentTeam:
    def __init__(self, id, tournament_id, team_id):
        self.__id = id
        self.__tournament_id = tournament_id
        self.__team_id = team_id

    @property
    def id(self):
        return self.__id

    @property
    def tournament_id(self):
        return self.__tournament_id

    @property
    def team_id(self):
        return self.__team_id
