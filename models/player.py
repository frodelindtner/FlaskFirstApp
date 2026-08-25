class Player:
    def __init__(self, id, team_id, first_name, last_name, position, jersey_number):
        self.__id = id
        self.__team_id = team_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__position = position
        self.__jersey_number = jersey_number

    @property
    def id(self):
        return self.__id

    @property
    def teamid(self):
        return self.__team_id

    @teamid.setter
    def teamid(self, new_team_id):
        self.__team_id = new_team_id

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, new_first_name):
        self.__first_name = new_first_name

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, new_last_name):
        self.__last_name = new_last_name

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, new_position):
        self.__position = new_position

    @property
    def jersey_number(self):
        return self.__jersey_number

    @jersey_number.setter
    def jersey_number(self, new_jersey_number):
        self.__jersey_number = new_jersey_number
