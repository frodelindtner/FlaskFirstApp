import sqlite3
from models.tournament import Tournament
from models.tournament_team import TournamentTeam
from models.tournament_match import TournamentMatch


class Storage_Tournament:
    def __init__(self):
        self.__connection = sqlite3.connect("storage/database/StandingDB.db", check_same_thread=False)
        self.__create_tables()

    def __create_tables(self):
        cur = self.__connection.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS Tournaments(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name VARCHAR(100),
                Season INTEGER,
                Format VARCHAR(30)
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS TournamentTeams(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                TournamentId INTEGER NOT NULL,
                TeamId INTEGER NOT NULL,
                FOREIGN KEY (TournamentId) REFERENCES Tournaments(Id),
                FOREIGN KEY (TeamId) REFERENCES Teams(Id)
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS TournamentMatches(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                TournamentId INTEGER NOT NULL,
                RoundNumber INTEGER,
                HomeTeamId INTEGER,
                AwayTeamId INTEGER,
                HomeScore INTEGER DEFAULT 0,
                AwayScore INTEGER DEFAULT 0,
                MatchStatus VARCHAR(20) DEFAULT 'scheduled',
                FOREIGN KEY (TournamentId) REFERENCES Tournaments(Id),
                FOREIGN KEY (HomeTeamId) REFERENCES Teams(Id),
                FOREIGN KEY (AwayTeamId) REFERENCES Teams(Id)
            )
            """
        )
        self.__connection.commit()
        cur.close()

    def get_all_tournaments(self):
        cur = self.__connection.cursor()
        cur.execute("SELECT * FROM Tournaments ORDER BY Id DESC")
        tournaments = []
        for row in cur:
            tournaments.append(Tournament(*row))
        cur.close()
        return tournaments

    def get_tournament_by_id(self, id):
        cur = self.__connection.cursor()
        cur.execute("SELECT * FROM Tournaments WHERE Id = (?)", (id,))
        row = cur.fetchone()
        cur.close()
        if row is None:
            return None
        return Tournament(*row)

    def add_tournament(self, tournament: Tournament):
        cur = self.__connection.cursor()
        cur.execute(
            "INSERT INTO Tournaments(Name, Season, Format) VALUES(?, ?, ?)",
            (tournament.name, tournament.season, tournament.format),
        )
        self.__connection.commit()
        return cur.lastrowid

    def update_tournament(self, tournament: Tournament):
        cur = self.__connection.cursor()
        cur.execute(
            "UPDATE Tournaments SET Name = (?), Season = (?), Format = (?) WHERE Id = (?)",
            (tournament.name, tournament.season, tournament.format, tournament.id),
        )
        self.__connection.commit()
        cur.close()

    def delete_tournament(self, id):
        cur = self.__connection.cursor()
        cur.execute("DELETE FROM TournamentMatches WHERE TournamentId = (?)", (id,))
        cur.execute("DELETE FROM TournamentTeams WHERE TournamentId = (?)", (id,))
        cur.execute("DELETE FROM Tournaments WHERE Id = (?)", (id,))
        self.__connection.commit()
        cur.close()

    def get_tournament_teams(self, tournament_id):
        cur = self.__connection.cursor()
        cur.execute("SELECT * FROM TournamentTeams WHERE TournamentId = (?) ORDER BY Id ASC", (tournament_id,))
        teams = []
        for row in cur:
            teams.append(TournamentTeam(*row))
        cur.close()
        return teams

    def add_team_to_tournament(self, tournament_id, team_id):
        cur = self.__connection.cursor()
        cur.execute(
            "INSERT INTO TournamentTeams(TournamentId, TeamId) VALUES(?, ?)",
            (tournament_id, team_id),
        )
        self.__connection.commit()
        return cur.lastrowid

    def remove_team_from_tournament(self, tournament_id, team_id):
        cur = self.__connection.cursor()
        cur.execute("DELETE FROM TournamentTeams WHERE TournamentId = (?) AND TeamId = (?)", (tournament_id, team_id))
        self.__connection.commit()
        cur.close()

    def get_tournament_matches(self, tournament_id):
        cur = self.__connection.cursor()
        cur.execute("SELECT * FROM TournamentMatches WHERE TournamentId = (?) ORDER BY RoundNumber ASC, Id ASC", (tournament_id,))
        matches = []
        for row in cur:
            matches.append(TournamentMatch(*row))
        cur.close()
        return matches

    def add_match(self, tournament_id, round_number, home_team_id, away_team_id, home_score=0, away_score=0, match_status='scheduled'):
        cur = self.__connection.cursor()
        cur.execute(
            "INSERT INTO TournamentMatches(TournamentId, RoundNumber, HomeTeamId, AwayTeamId, HomeScore, AwayScore, MatchStatus) VALUES(?, ?, ?, ?, ?, ?, ?)",
            (tournament_id, round_number, home_team_id, away_team_id, home_score, away_score, match_status),
        )
        self.__connection.commit()
        return cur.lastrowid

    def update_match_score(self, match_id, home_score, away_score):
        cur = self.__connection.cursor()
        cur.execute(
            "UPDATE TournamentMatches SET HomeScore = (?), AwayScore = (?), MatchStatus = (?) WHERE Id = (?)",
            (home_score, away_score, 'finished', match_id),
        )
        self.__connection.commit()
        cur.close()

    def clear_matches(self, tournament_id):
        cur = self.__connection.cursor()
        cur.execute("DELETE FROM TournamentMatches WHERE TournamentId = (?)", (tournament_id,))
        self.__connection.commit()
        cur.close()
