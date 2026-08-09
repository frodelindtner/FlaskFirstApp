from storage.db_results import Storage_Result
from models.result import Result

class ResultService:
    def __init__(self):
        self.__storage = Storage_Result()
  
    def get_all_results(self):
        """
        Getting all results from storage
        """
        return self.__storage.get_all_results()

    def get_result_by_id(self, id):
        """
        Getting result by id from storage
        """
        result = self.__storage.get_result_by_id(id)
        return result

    def get_result_by_teamid(self, teamid):
        """
        Getting result by team id from storage
        """
        result = self.__storage.get_result_by_teamid(teamid)
        return result        

    def add_win_team(self, teamid):
        """
        Adding win to team by team id
        """
        result_row = self.get_result_by_teamid(teamid)
        result_row.wins = result_row.wins + 1
        self.__storage.update_result(result_row)

    def create_result(self, teamid, wins, losses):
        """
        Creating result and adding to storage
        """
        r = Result(None, teamid, wins, losses)
        self.__storage.add_result(r)
        return r

    def update_result(self, id, teamid, wins, losses):
        """
        Updating result in storage
        """
        r = Result(id, teamid, wins, losses)
        self.__storage.update_result(r)
        return r

    def delete_result_by_teamid(self, teamid):
        """
        Deleting result by team id from storage
        """
        result = self.get_result_by_teamid(teamid)
        self.delete_result(result.id)

    def delete_result(self, id):
        """
        Deleting result from storage
        """
        self.__storage.delete_result(id)

    def create_empty_result(self, teamid):
        """
        Creating empty result for team"""
        self.create_result(teamid, 0, 0)