class Stat:
    def __init__(self, id, player, year, batting_average):
        self.__id = id
        self.player = player
        self.year = year
        self.batting_average = batting_average

    @property
    def id(self):
        return self.__id
    
    def __repr__(self):
        return self.player