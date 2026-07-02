import sqlite3
from models.standing import Standing

class Storage_Result:
    def __init__(self):
        self.__connection = sqlite3.connect("storage/database/StandingDB.db", check_same_thread=False)

    def get_standing_local(self):
        cur = self.__connection.cursor()
        cur.execute("select * from StandingLocal")
        standings = []
        for row in cur:
            # Season, Name, League, Division, Wins, Losses
            standing_obj = Standing(row[0], 'N/A', 1, ))
            standings.append(standing_obj)
        cur.close()
        return standings