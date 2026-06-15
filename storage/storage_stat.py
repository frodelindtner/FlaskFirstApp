from models.yearstat import Year_Stat
class Storage_Stat:
    __stats:list[Year_Stat] = []

    def get_all_stats(self):
        return self.__stats
    
    def add_stat(self, stat:Year_Stat):
        self.__stats.append(stat)