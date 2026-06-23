import sqlite3
from models.result import Result

class Storage_Result:
    def __init__(self):
        self.__connection = sqlite3.connect("storage/database/StandingDB.db", check_same_thread=False)

    def get_all_results(self):
        cur = self.__connection.cursor()
        cur.execute("SELECT * FROM Results")
        results = []
        for row in cur:
            result_obj = Result(*row)
            results.append(result_obj)
        cur.close()
        return results
    
    def get_result_by_id(self, id):
        cur = self.__connection.cursor()
        cur.execute("SELECT * FROM Results WHERE Id = (?)", (id,))
        for row in cur:
            result = Result(*row)
        return result

    def get_result_by_teamid(self, teamid):
        cur = self.__connection.cursor()
        cur.execute("SELECT * FROM Results WHERE TeamId = (?)", (teamid,))
        for row in cur:
            result = Result(*row)
        return result

    def add_result(self, result:Result):
        cur = self.__connection.cursor()
        cur.execute(f"INSERT INTO Results(Id, TeamId, Wins, Losses) VALUES(?, ?, ?, ?)"
                    ,(result.id, result.teamid, result.wins, result.losses))
        self.__connection.commit()
        return cur.lastrowid

    def update_result(self, result:Result):
        cur = self.__connection.cursor()
        cur.execute(f"UPDATE Results SET TeamId = (?), Wins = (?), Losses = (?) WHERE Id = (?)", 
                    (result.teamid, result.wins, result.losses, result.id))
        self.__connection.commit()

    
    def delete_result(self, id):
        cur = self.__connection.cursor()
        cur.execute(f"DELETE FROM Results WHERE Id = (?)", (id,))
        self.__connection.commit()