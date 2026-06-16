from models.yearstat import Year_Stat
from storage.storage_stat import Storage_Stat

class Stat_Service:
    def __init__(self):
        self.__storage_stat = Storage_Stat()

    def get_all_stats(self):
        return self.__storage_stat.get_all_stats()
    
    def create_stat(self, id, player, year, batting_average):
        stat = Year_Stat(id, player, year, batting_average)
        self.__storage_stat.add_stat(stat)
        return stat
    
    def find_stat_by_id(self, id):
        for s in self.get_all_stats():
            if s.id == id:
                return s

    def update_stat(self, stat:Year_Stat):
        return self.__storage_stat.update_stat(stat)
    
    def delete_stat(self, stat_id):
        self.__storage.delete_album(stat_id)

    # -------------------------------------------------------

    def create_some_objects(self):
        self.create_stat(10001, 'frode', '2021', '125')
        self.create_stat(10002, 'frode', '2020', '250')
        self.create_stat(10003, 'frode', '2019', '325')
        self.create_stat(10004, 'frode', '2018', '225')

