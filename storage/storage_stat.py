from models.yearstat import Year_Stat
class Storage_Stat:
    __stats:list[Year_Stat] = []

    def get_all_stats(self):
        return self.__stats
    
    def add_stat(self, stat:Year_Stat):
        self.__stats.append(stat)

    def update_stat(self, stat:Year_Stat):
        for a in self.__stats:
            if a.id == Year_Stat.id:
                a = stat
                return a
        else:
            return None
        
    def delete_stat(self, id):
        for a in self.__stats:
            if a.id == id:
                self.__stats.remove(a)
                break