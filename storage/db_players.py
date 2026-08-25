import sqlite3
from models.player import Player


class Storage_Player:
    SELECT_ALL_SQL = "SELECT * FROM Players"
    SELECT_BY_ID_SQL = SELECT_ALL_SQL + " WHERE Id = (?)"
    SELECT_BY_TEAMID_SQL = SELECT_ALL_SQL + " WHERE TeamId = (?)"
    INSERT_SQL = "INSERT INTO Players(TeamId, FirstName, LastName, Position, JerseyNumber) VALUES(?, ?, ?, ?, ?)"
    UPDATE_SQL = "UPDATE Players SET TeamId = (?), FirstName = (?), LastName = (?), Position = (?), JerseyNumber = (?) WHERE Id = (?)"
    DELETE_SQL = "DELETE FROM Players WHERE Id = (?)"

    def __init__(self):
        self.__connection = sqlite3.connect("storage/database/StandingDB.db", check_same_thread=False)
        self.__create_table_if_missing()

    def __create_table_if_missing(self):
        cur = self.__connection.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS Players(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                TeamId INTEGER NOT NULL,
                FirstName VARCHAR(50),
                LastName VARCHAR(50),
                Position VARCHAR(30),
                JerseyNumber INTEGER,
                FOREIGN KEY (TeamId) REFERENCES Teams(Id)
            )
            """
        )
        self.__connection.commit()
        cur.close()

    def get_all_players(self):
        cur = self.__connection.cursor()
        cur.execute(self.SELECT_ALL_SQL)
        players = []
        for row in cur:
            players.append(Player(*row))
        cur.close()
        return players

    def get_player_by_id(self, id):
        cur = self.__connection.cursor()
        cur.execute(self.SELECT_BY_ID_SQL, (id,))
        for row in cur:
            player = Player(*row)
        cur.close()
        return player

    def get_players_by_teamid(self, teamid):
        cur = self.__connection.cursor()
        cur.execute(self.SELECT_BY_TEAMID_SQL, (teamid,))
        players = []
        for row in cur:
            players.append(Player(*row))
        cur.close()
        return players

    def add_player(self, player: Player):
        cur = self.__connection.cursor()
        cur.execute(
            self.INSERT_SQL,
            (player.teamid, player.first_name, player.last_name, player.position, player.jersey_number),
        )
        self.__connection.commit()
        return cur.lastrowid

    def update_player(self, player: Player):
        cur = self.__connection.cursor()
        cur.execute(
            self.UPDATE_SQL,
            (player.teamid, player.first_name, player.last_name, player.position, player.jersey_number, player.id),
        )
        self.__connection.commit()
        cur.close()

    def delete_player(self, id):
        cur = self.__connection.cursor()
        cur.execute(self.DELETE_SQL, (id,))
        self.__connection.commit()
        cur.close()
