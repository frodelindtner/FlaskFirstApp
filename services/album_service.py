from models.album import Album
from storage import storage

class Service:
    def __init__(self):
        self.__storage = storage.Storage()

    def get_all_album(self):
        return self.__storage.get_all_albums()
    
    def create_album(self, id, title, artist, release_year):
        a = Album(id, title, artist, release_year)
        self.__storage.add_album(a)
        return a
    


# -------------------------------------------------------

    def create_some_objects(self):
        self.create_album(1, 'Demon Days', 'Gorillaz', 2005)
        self.create_album(2, 'Automatic For The People', 'R.E.M.', 1992)
        self.create_album(3, 'Lost Isles', 'Oceans Ate Alaska', 2015)
        self.create_album(4, 'Operation Doomsday', 'MF DOOM', 1999)
        self.create_album(5, 'Punk in Drublic', 'NOFX', 1994)
        self.create_album(6, 'Get to Heaven', 'Everything Everything', 2014)