from models.result import Result

class Storage_Result:
    __results:list[Result] = []
    __curid = 1000000

    def get_all_results(self):
        return self.__results
    
    def get_result_by_id(self, id):
        for r in self.__results:
            if r.id == id:
                return r
        else:
            return None

    def get_result_by_teamid(self, teamid):
        for r in self.__results:
            if r.teamid == teamid:
                return r
        else:
            return None

    def add_result(self, result:Result):
        # Id from sequens in SQL
        result.id = self.__curid
        self.__results.append(result)
        self.__curid = self.__curid + 1
        print(f'results id {self.__curid}')

    def update_result(self, result:Result):
        for r in self.__results:
            if r.id == result.id:
                r.losses = result.losses
                r.night_wins = result.night_wins
                r.wins = result.wins

                # print(f'deleting result {result.id}')
                # self.delete_result(result.id)
                # print(f'creating result {result.id}')
                # self.add_result(result)
                return r
        else:
            return None
    
    def delete_result(self, id):
        for r in self.__results:
            if r.id == id:
                self.__results.remove(r)
                break