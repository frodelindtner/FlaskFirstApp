from models.player import Player
from storage.db_players import Storage_Player


class PlayerService:
    def __init__(self):
        self.__storage = Storage_Player()

    def get_all_players(self):
        """
        Getting all players from storage
        """
        return self.__storage.get_all_players()

    def get_player_by_id(self, id):
        """
        Getting player by id from storage
        """
        return self.__storage.get_player_by_id(id)

    def get_players_by_teamid(self, teamid):
        """
        Getting all players for a team
        """
        return self.__storage.get_players_by_teamid(teamid)

    def create_player(self, teamid, first_name, last_name, position, jersey_number):
        """
        Creating player and adding to storage
        """
        player = Player(None, teamid, first_name, last_name, position, jersey_number)
        created_id = self.__storage.add_player(player)
        return Player(created_id, teamid, first_name, last_name, position, jersey_number)

    def update_player(self, id, teamid, first_name, last_name, position, jersey_number):
        """
        Updating player in storage
        """
        player = Player(id, teamid, first_name, last_name, position, jersey_number)
        self.__storage.update_player(player)
        return player

    def delete_player(self, id):
        """
        Deleting player from storage
        """
        self.__storage.delete_player(id)

    def create_some_players(self):
        """
        Creating some example players for testing
        """
        self.create_player(1, 'John', 'Smith', 'Pitcher', 15)
        self.create_player(1, 'Mike', 'Johnson', 'Catcher', 12)
        self.create_player(2, 'Anna', 'Brown', 'Shortstop', 7)
        self.create_player(2, 'Chris', 'Miller', 'Center fielder', 22)
