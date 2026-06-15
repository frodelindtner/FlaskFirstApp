class Album:
    def __init__(self, id, title, artist, release_year):
        self.__id = id
        self.title = title
        self.artist = artist
        self.release_year = release_year

    @property
    def id(self):
        return self.__id
    
    def __repr__(self):
        return self.title