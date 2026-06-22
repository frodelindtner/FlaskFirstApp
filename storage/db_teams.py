from models.team import Team

class Storage_Team:
    __teams:list[Team] = []
    __curid = 10

    def get_all_teams(self):
        return self.__teams
    
    def get_team_by_id(self, id):
        for t in self.__teams:
            if t.id == id:
                return t
        else:
            return None

    def add_team(self, team:Team):
        # Id from sequens in SQL
        team.id = self.__curid
        self.__teams.append(team)
        self.__curid += 1
        return team.id

    def update_team(self, team:Team):
        print(f'in storage: {team.id}')
        for t in self.__teams:
            if t.id == team.id:
                t = team
                self.delete_team(team.id)
                self.add_team(team)
                return t
        else:
            return None
    
    def delete_team(self, id):
        for t in self.__teams:
            if t.id == id:
                self.__teams.remove(t)
                break