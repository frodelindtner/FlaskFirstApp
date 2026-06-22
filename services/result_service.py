from storage.db_results import Storage_Result
from models.result import Result

class ResultService:
    def __init__(self):
        self.__storage = Storage_Result()
  
    def get_all_results(self):
        return self.__storage.get_all_results()

    def get_result_by_id(self, id):
        result = self.__storage.get_result_by_id(id)
        return result

    def get_result_by_teamid(self, teamid):
        result = self.__storage.get_result_by_teamid(teamid)
        return result        

    def create_result(self, teamid, wins, losses, nightwins):
        r = Result(teamid, wins, losses, nightwins)
        self.__storage.add_result(r)
        return r

    def update_result(self, id, teamid, wins, losses, nightwins):
        r = Result(teamid, wins, losses, nightwins)
        r.id = id
        self.__storage.update_result(r)
        return r

    def create_empty_result(self, teamid):
        self.create_result(teamid, 0, 0, 0)

    def create_some_objects(self):
        self.create_result(101101, 12, 12, 5)
        self.create_result(101102, 12, 12, 5)
        self.create_result(101103, 12, 12, 5)
        self.create_result(101104, 12, 12, 5)
        self.create_result(101105, 12, 12, 5)
        self.create_result(101106, 12, 12, 5)

 