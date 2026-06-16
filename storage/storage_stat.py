from models.stat import Stat
class Storage_Stat:
    __stats:list[Stat] = []

    def get_all_stats(self):
        return self.__stats
    
    def add_stat(self, stat:Stat):
        self.__stats.append(stat)

    def update_stat(self, stat:Stat):
        for a in self.__stats:
            if a.id == Stat.id:
                a = stat
                return a
        else:
            return None
        
    def delete_stat(self, id):
        for a in self.__stats:
            if a.id == id:
                self.__stats.remove(a)
                break