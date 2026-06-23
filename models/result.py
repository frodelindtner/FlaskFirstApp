class Result:
    def __init__(self, id, team_id, wins, losses):
        self.__id = id
        self.__team_id = team_id
        self.__wins = wins
        self.__losses = losses
    
    @property
    def id(self):
        return self.__id

    @property
    def teamid(self):
        return self.__team_id

    @teamid.setter
    def teamid(self, new_team_id):
        self.__team_id = new_team_id

    @property
    def wins(self):
        return self.__wins

    @wins.setter
    def wins(self, new_wins):
        self.__wins = new_wins


    @property
    def losses(self):
        return self.__losses

    @losses.setter
    def losses(self, new_losses):
        self.__losses = new_losses
