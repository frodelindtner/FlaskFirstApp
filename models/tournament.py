class Tournament:
    def __init__(self, id, name, season, format):
        self.__id = id
        self.__name = name
        self.__season = season
        self.__format = format

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        self.__name = new_name

    @property
    def season(self):
        return self.__season

    @season.setter
    def season(self, new_season):
        self.__season = new_season

    @property
    def format(self):
        return self.__format

    @format.setter
    def format(self, new_format):
        self.__format = new_format
