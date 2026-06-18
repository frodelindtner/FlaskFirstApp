from models.team import Team
class Storage_Team:
    __teams:list[Team] = []

    def get_all_teams(self):
        return self.__teams
    
    def add_team(self, team:Team):
        self.__teams.append(team)

    def update_team(self, team:Team):
        for t in self.__teams:
            if t.id == team.id:
                t = team
                return t
        else:
            return None
    
    def delete_team(self, id):
        for t in self.__teams:
            if t.id == id:
                self.__team.remove(t)
                break