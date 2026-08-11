import sqlite3
from models.result import Result

class Storage_Result:
    SELECT_ALL_SQL = "SELECT * FROM Results"
    SELECT_BY_ID_SQL = SELECT_ALL_SQL + " WHERE Id = (?)"
    SELECT_BY_TEAMID_SQL = SELECT_ALL_SQL + " WHERE TeamId = (?)"
    INSERT_SQL = "INSERT INTO Results(Id, TeamId, Wins, Losses) VALUES(?, ?, ?, ?)"
    UPDATE_SQL = "UPDATE Results SET TeamId = (?), Wins = (?), Losses = (?) WHERE Id = (?)"
    DELETE_SQL = "DELETE FROM Results WHERE Id = (?)"

    def __init__(self):
        self.__connection = sqlite3.connect("storage/database/StandingDB.db", check_same_thread=False)

    def get_all_results(self):
        cur = self.__connection.cursor()
        cur.execute(self.SELECT_ALL_SQL)
        results = []
        for row in cur:
            result_obj = Result(*row)
            results.append(result_obj)
        cur.close()
        return results
    
    def get_result_by_id(self, id):
        cur = self.__connection.cursor()
        cur.execute(self.SELECT_BY_ID_SQL, (id,))
        for row in cur:
            result = Result(*row)
        return result

    def get_result_by_teamid(self, teamid):
        cur = self.__connection.cursor()
        cur.execute(self.SELECT_BY_TEAMID_SQL, (teamid,))
        for row in cur:
            result = Result(*row)
        return result

    def add_result(self, result:Result):
        cur = self.__connection.cursor()
        cur.execute(self.INSERT_SQL,
                    (result.id, result.teamid, result.wins, result.losses))
        self.__connection.commit()
        return cur.lastrowid

    def update_result(self, result:Result):
        cur = self.__connection.cursor()
        cur.execute(self.UPDATE_SQL, 
                    (result.teamid, result.wins, result.losses, result.id))
        self.__connection.commit()

    
    def delete_result(self, id):
        cur = self.__connection.cursor()
        cur.execute(self.DELETE_SQL, (id,))
        self.__connection.commit()