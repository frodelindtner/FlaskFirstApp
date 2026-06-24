from models.team import Team
import sqlite3

class Storage_Team:
    def __init__(self):
        self.__connection = sqlite3.connect("storage/database/StandingDB.db", check_same_thread=False)

    def get_all_teams(self) -> list[Team]:
        cur = self.__connection.cursor()
        cur.execute("SELECT * FROM Teams")
        teams = []
        for row in cur:
            # print(f'Debug: The teams id values: {row[0]}')
            team_obj = Team(*row)
            teams.append(team_obj)
        cur.close()
        return teams
    
    def get_team_by_id(self, id):
        cur = self.__connection.cursor()
        cur.execute("SELECT * FROM Teams WHERE Id = (?)", (id,))
        for row in cur:
            team = Team(*row)
        return team
    
    def add_team(self, team:Team):
        cur = self.__connection.cursor()
        cur.execute(f"INSERT INTO Teams(Season, City, Name, League, Division) VALUES(?, ?, ?, ?, ?)"
                    ,(team.season, team.city, team.name, team.league, team.division))
        self.__connection.commit()
        return cur.lastrowid

    def update_team(self, team:Team):
        cur = self.__connection.cursor()
        cur.execute(f"UPDATE Teams SET Season = (?), City = (?), Name = (?), League = (?), Division = (?) WHERE Id = (?)", 
                    (team.season, team.city, team.name, team.league, team.division, team.id))
        self.__connection.commit()
    
    def delete_team(self, id):
        cur = self.__connection.cursor()
        cur.execute(f"DELETE FROM Teams WHERE Id = (?)", (id,))
        self.__connection.commit()