class Team:
    def __init__(self, id, season, city, name, league, division):
        self.__id = id
        self.__season = season
        self.__city = city
        self.__name = name
        self.__league = league
        self.__division = division

    @property
    def id(self):
        return self.__id

    @property
    def season(self):
        return self.__season
    
    @season.setter
    def season(self, new_season):
        self.__season = new_season

    @property
    def city(self):
        return self.__city
    
    @city.setter
    def city(self, new_city):
        self.__city = new_city

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, new_name):
        self.__name = new_name    
    
    @property
    def league(self):
        return self.__league
    
    @league.setter
    def league(self, new_league):
        self.__league = new_league

    @property
    def division(self):
        return self.__division
    
    @division.setter
    def division(self, new_division):
        self.__division = new_division